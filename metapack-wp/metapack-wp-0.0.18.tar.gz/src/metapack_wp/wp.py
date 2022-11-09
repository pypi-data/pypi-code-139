# Copyright (c) 2019 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

"""
CLI program for managing packages
"""

import json
from functools import lru_cache
from textwrap import dedent
from xmlrpc.client import Fault

from slugify import slugify
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost

from metapack import Downloader
from metapack.cli.core import (MetapackCliMemo, err, warn, get_config, prt)
from metapack.html import display_context, jsonld
from metapack_build.build import find_csv_packages, find_fs_package_from_dir
from rowgenerators import parse_app_url
from time import sleep

downloader = Downloader.get_instance()

import collections

try:
    # Seems to be a change in python 3.10
    collections.Iterable
except AttributeError:
    collections.Iterable = collections.abc.Iterable



def wp(subparsers):
    parser = subparsers.add_parser(
        'wp',
        help='Publish a data package to Wordpress ',
        description="""
        Write a notebook or package to Wordpress.

        If the source argument is a data package, (Metatab format Metapack package, CSV or ZIP ) package information will be 
        submitted to the Wordpress blog as a blog post, formatted similarly to the package html documentation file.

        If the source is a Metatab file and the ``--references`` option is set, the references References section of the 
        file are URLs for the packages that should be published. The ``--group`` and ``--tag`` options are used
        for publishing each of the references. 
        
        If the source argument is a Jupyter notebook, the notebook is written as a blog post. See
        http://insights.civicknowledge.com for examples.

        """,
        epilog='Cache dir: {}\n'.format(str(downloader.cache.getsyspath('/'))))

    parser.set_defaults(run_command=run_wp)

    parser.add_argument('-g', '--group', nargs='?', action='append', help="Assign an additional group. Can be used "
                                                                          "multiple times, or once with values "
                                                                          "separated by commas")

    parser.add_argument('-t', '--tag', nargs='?', action='append', help="Assign an additional tag. Can be used "
                                                                        "multiple times, or once with values "
                                                                        "separated by commas")

    parser.add_argument('-H', '--header', help='Dump YAML of notebook header', action='store_true')

    parser.add_argument('-G', '--get', help='Get and dump the post, rather that update it', action='store_true')

    parser.add_argument('-P', '--profile', help="Name of a BOTO or AWS credentails profile", required=False)

    parser.add_argument('-p', '--publish', help='Set the post state to published, rather than draft',
                        action='store_true')

    parser.add_argument('-U', '--upload', help='Upload the data to Wordpress', action='store_true')

    parser.add_argument('-r', '--result', action='store_true', default=False,
                        help="If mp -q flag set, still report results")

    parser.add_argument('-j', '--json', help="Dump the JSON that is used to generate the HTML from tempaltes",
                        action='store_true')

    parser.add_argument('-d', '--dump', help="Dump the HTML. Default if site_name is not specified",
                        action='store_true')

    parser.add_argument('-s', '--site_name', help="Site name, in the .metapack.yaml configuration file")

    parser.add_argument('-T', '--template', help="Name of Jinja2 template", default='wordpress.html')

    parser.add_argument('-n', '--no-op', help='Do everything but submit the post', action='store_true')

    parser.add_argument('source', nargs='?', help="Path to a notebook file or a Metapack package")


def split_groups_tags(v):
    if not v:
        return

    for g in v:
        if ',' in g:
            for g_ in g.split(','):
                yield g_
        else:
            yield g


def run_wp(args):
    if not args.source:
        args.source = '.'

    u = parse_app_url(args.source)

    args.metatabfile = args.source
    m = MetapackCliMemo(args, downloader)

    if args.json:
        context = display_context(m.doc)
        print(json.dumps(context, indent=4))

    elif args.dump or not args.site_name:
        doc = get_doc(m)
        content = html(doc, m.template)
        print(content)
    elif args.get:
        run_get_post(m)
    elif args.site_name:

        run_package(m)
        if args.result:
            print(f"✅ Published {str(m.doc.name)} to {args.site_name}", )
        else:
            prt(f"Published {str(m.doc.name)} to {args.site_name}", str(u))


def get_site_config(site_name):
    config = get_config()

    if config is None:
        err("No metatab configuration found. Can't get Wordpress credentials. Maybe create '~/.metapack.yaml'")

    site_config = config.get('wordpress', {}).get(site_name, {})

    if not site_config:
        err("In config file '{}', expected 'wordpress.{}' section for site config"
            .format(config['_loaded_from'], site_name))

    if 'url' not in site_config or 'user' not in site_config or 'password' not in site_config:
        err(dedent(
            """
            Incomplete configuration. Expected:
                wordpress.{site_name}.url
                wordpress.{site_name}.user
                wordpress.{site_name}.password
            In configuration file '{cfg_file}'
            """.format(site_name=site_name, cfg_file=config['_loaded_from'])
        ))

    return site_config['url'], site_config['user'], site_config['password']


def cust_field_dict(post):
    try:
        return dict((e['key'], e['value']) for e in post.custom_fields)
    except (KeyError, AttributeError):
        return {}


@lru_cache()
def get_posts(wp):
    """Get and memoize all posts"""
    from wordpress_xmlrpc.methods.posts import GetPosts

    all_posts = []

    offset = 0
    increment = 20
    while True:
        posts = wp.call(GetPosts({'number': increment, 'offset': offset, 'post_type': 'post'}))
        if len(posts) == 0:
            break  # no more posts returned
        for post in posts:
            all_posts.append(post)

        offset = offset + increment

    return all_posts




def set_custom_field(post, key, value):
    if not hasattr(post, 'custom_fields') or not key in [e['key'] for e in post.custom_fields]:

        if not hasattr(post, 'custom_fields'):
            post.custom_fields = []

        post.custom_fields.append({'key': key, 'value': value})


def html(doc, template):
    from markdown import markdown as convert_markdown
    from bs4 import BeautifulSoup
    from jinja2 import Environment, PackageLoader

    context = display_context(doc)

    if 'inline_doc' in context:
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.admonition'
        ]

        inline_doc = convert_markdown(context['inline_doc'], extensions=extensions)

        tag_map = {
            'p': 'wp:paragraph',
            'ul': 'wp:list',
            'pre': 'wp:code',
            'h1': 'wp:heading',
            'h2': 'wp:heading',
            'h3': 'wp:heading',
            'h4': 'wp:heading',
            'h5': 'wp:heading',
            'h6': 'wp:heading',
        }

        nodes = BeautifulSoup(inline_doc, features="html.parser").find_all(recursive=False)

        context['inline_doc_parts'] = \
            [(tag_map.get(n.name, 'wp:html'), str(n)) for n in nodes]

    else:
        context['inline_doc_parts'] = []

    context['jsonld'] = json.dumps(jsonld(doc), indent=4)

    # print(json.dumps(context, indent=4))

    env = Environment(
        loader=PackageLoader('metapack_wp', 'support/templates')
        # autoescape=select_autoescape(['html', 'xml'])
    )

    return env.get_template(template).render(**context)


def get_doc(m):
    """
    :param m: Locate the package document. If --upload is specified, look for

    :type m:
    :return:
    :rtype:
    """
    if m.args.upload:
        doc = find_fs_package_from_dir(m.args.source)
    else:
        doc = find_csv_package(m)

    return doc


def find_csv_package(m):
    if not m.doc.find('Root.Distribution'):

        doc = find_csv_packages(m, downloader)
        if not doc:
            err('Package has no Root.Distribution, and no CSV package found')
            doc = m.doc
        else:
            prt("Using CSV package: ", doc.ref)
    else:
        doc = m.doc

    return doc

def get_wp(m):
    url, user, password = get_site_config(m.args.site_name)
    wp = Client(url, user, password)
    return wp

def find_post(wp, identifier):
    for _post in get_posts(wp):
        if cust_field_dict(_post).get('identifier') == identifier:
            return _post
    return None

def run_get_post(m):
    """Get the post if it iexists and print out its data"""

    doc = get_doc(m)
    assert doc is not None

    wp = get_wp(m)

    post = find_post(wp, doc.identifier)

    if post:
        post.content = "…content elided…"
        from pprint import pprint
        pprint(post.struct)
        return
    else:
        warn(f"Didn't find post for identifier {doc.identifier}")
        return


def get_or_new_post(m, wp, doc):
    """Create a stub post, if a post with the correct identifier does not exist"""

    post = find_post(wp, doc.identifier)

    if post:
        action = lambda post: EditPost(post.id, post)
    else:
        prt(f"Creating new post; could not find identifier '{doc.identifier}' ")
        action = lambda post: NewPost(post)
        post = WordPressPost()

    set_custom_field(post, 'identifier', doc.identifier)
    set_custom_field(post, 'name', doc.name)
    set_custom_field(post, 'nvname', doc.nonver_name)

    if not m.args.no_op:

        r = wp.call(action(post))
        wp = get_wp(m)
        for i in range(4):
            post = find_post(wp, doc.identifier)

            if post is not None:
                break
            print("HERE!", post)
            sleep(1)
        else:
            err("Could not find post after creating it", r,  post)

    return post

def upload_to_wordpress(wp, post, pkg):
    """Upload CSV resources to Wordpress"""
    from wordpress_xmlrpc.compat import xmlrpc_client
    from wordpress_xmlrpc.methods import media

    r = wp.call(media.GetMediaLibrary({'parent_id': post.id, 'mime_type': 'text/csv'}))

    extant = {e.title: e for e in r}

    for r in pkg.resources():
        url = r.resolved_url
        if r.qualified_name in extant:
            print('👌', r.qualified_name, 'Not uploading; already exist. ')
            r.value = extant[r.qualified_name].link

        else:

            d = {
                'name': r.qualified_name,
                'type': 'text/csv',
                'bits': xmlrpc_client.Binary(url.fspath.read_bytes()),
                'post_id': post.id
            }

            try:
                rsp = wp.call(media.UploadFile(d))
                prt('✅', r.qualified_name, 'Uploaded to ', rsp['url'])
                r.value = rsp['url']
            except Exception as e:
                err(r.qualified_name, 'Upload failed: ', e)
                raise



def run_package(m):
    """Publish documentation for a package as a post"""

    if m.args.upload:
        doc = find_fs_package_from_dir(m.args.source)
    else:
        doc = find_csv_package(m)

    url, user, password = get_site_config(m.args.site_name)
    wp = Client(url, user, password)

    post = get_or_new_post(m, wp, doc)

    assert post is not None

    if m.args.upload:
        upload_to_wordpress(wp, post, doc)

    content = html(doc, m.args.template)

    post.excerpt = doc['Root'].get_value('Root.Description') or content[:200]

    post_tags = list(set(
        [t.value for t in doc['Root'].find('Root.Tag')] +
        [t.value for t in doc['Root'].find('Root.Group')] +
        [doc['Root'].get_value('Root.Origin')] +
        list(split_groups_tags(m.args.group)) +
        list(split_groups_tags(m.args.tag))
    ))

    post.terms_names = {
        'post_tag': post_tags,
        'category': ['Dataset'] + list(split_groups_tags(m.args.group))
    }

    post.title = doc.get_value('Root.Title')
    post.slug = slugify(doc.nonver_name)
    post.content = content

    if m.args.publish:
        post.post_status = 'publish'

    try:
        if m.args.no_op:
            r = {}
        else:
            r = wp.call(EditPost(post.id, post))
    except Fault as e:

        if 'taxonomies' in e.faultString:
            err(("User {} does not have permissions to add terms to taxonomies. "
                 "Terms are: {}").format(user, post.terms_names))

        raise

    return r
