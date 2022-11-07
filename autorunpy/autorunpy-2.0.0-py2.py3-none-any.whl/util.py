"""

    """

import json

from .models import UserRepo


def get_user_repo_from_url(repo_url) :
    gu = repo_url.split('github.com/')[1]
    user_name = gu.split('/')[0]
    repo_name = gu.split('/')[1]
    user_slash_repo = f'{user_name}/{repo_name}'
    user_und_repo = f'{user_name}_{repo_name}'
    return UserRepo(user_name , repo_name , user_slash_repo , user_und_repo)

def read_json(fp) :
    with open(fp) as f :
        return json.load(f)
