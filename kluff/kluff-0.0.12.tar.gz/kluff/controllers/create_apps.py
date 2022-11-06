import os
import sys
import shutil
from cement.utils.version import get_version_banner
from ..core.version import get_version
from cement import Controller, ex
from ..utils.utils import CommandError

VERSION_BANNER = """
Build and Deploy with Kluff %s
%s
""" % (get_version(), get_version_banner())


class AppSetup(Controller):
    plugin_name = ''
    container_registry = 'localhost:5001'
    backend_path = ''
    frontend_path = ''
    class Meta:
        label = 'items'
        stacked_type = 'embedded'
        stacked_on = 'base'

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help='create plugin',
        arguments=[
            (['plugin_name'], 
                            {'help': 'plugin name'}
            ),

            ( ['--language'],
                            {'help': 'Backend language i.e Python, Go, Javascript'}
            ),
        ],
    )
    def create(self):
        plugin_name = self.app.pargs.plugin_name
        language = self.app.pargs.language or 'python'
        self.app.log.info(f'creating plugin {plugin_name} using language {language}')
        try:
            self.plugin_name = plugin_name
            templates = self.app.config.get('kluff', 'templates')
            backend_template = os.path.join(templates, language)
            frontend_template = os.path.join(templates, 'react')
            target_backend_app = os.path.join(os.getcwd(), plugin_name, 'backend')
            target_frontend_app = os.path.join(os.getcwd(), plugin_name, 'frontend')
            shutil.copytree(backend_template, target_backend_app, dirs_exist_ok=True)
            shutil.copytree(frontend_template, target_frontend_app, dirs_exist_ok=True)
        except OSError as e:
            raise CommandError(e)


    @ex(
        help='run plugin',
        )
    def run(self):
        try:
            plugin_name = os.path.basename(os.getcwd())

            self.app.log.info(f'running plugin: {plugin_name}')

            self.backend_path = os.path.join(os.getcwd(), 'backend')
            self.frontend_path = os.path.join(os.getcwd(), 'frontend')

            if not os.path.exists(self.backend_path):
                print('Unable to find backend dir. Are you running kluff from inside your plugin dir?')
                sys.exit()

            if not os.path.exists(self.frontend_path):
                print('Unable to find frontend dir. Are you running kluff from inside your plugin dir?')
                sys.exit()

            backend_image_tag = f'{plugin_name}:backend'
            frontend_image_tag = f'{plugin_name}:frontend'

            os.system(f'cd {self.backend_path} && docker build -t {backend_image_tag} .')
            os.system(f'docker run -it -p 5000:5000 -d {backend_image_tag}')

            os.system(f'cd {self.frontend_path} && docker build -t {frontend_image_tag} .')
            os.system(f'docker run -it -p 3000:3000 -d {frontend_image_tag}')

        except OSError as e:
            raise CommandError(e)
    
    @ex(
        help='deploy plugin',
        )
    def deploy(self):
        self.app.log.info(f'deploying plugin')
        try:
            backend_image_tag = f'{self.plugin_name}-backend:latest'
            os.system(f'cd {self.backend_path}')
            os.system(f'docker build -t {backend_image_tag} .')
            os.system(f'docker tag {backend_image_tag} {self.container_registry}/{backend_image_tag}')
            os.system(f'docker push {self.container_registry}/{backend_image_tag}')
        except OSError as e:
            raise CommandError(e)
