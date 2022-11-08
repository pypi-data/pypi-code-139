import os
import glob
import platform
from InquirerPy import prompt
from fire import Fire
from .consts import ENV_KEY, LOCATIONS, VARIATIONS, DEFAULT_VARIATION

## 環境変数を表示
def show_status():
    print(f'{ENV_KEY}: {os.getenv(ENV_KEY)}')


## プロフィールディレクトリを環境変数に設定
def set_profile_dir():
    variation = get_variation()
    profile_dir = os.getenv(ENV_KEY)
    profile_dirs = get_profile_dirs(variation)
    questions = [
        {
            "type": "list",
            "message": f"Select an profile directory [{variation}]:",
            "choices": profile_dirs,
            "default": profile_dir,
        },
    ]
    profile_dir = prompt(questions)
    os.environ[ENV_KEY] = profile_dir[0]
    show_status()


## ブラウザバリエーションを取得
def get_variation():
    variation = DEFAULT_VARIATION
    questions = [
        {
            "type": "list",
            "message": "Select an bowser variation:",
            "choices": VARIATIONS,
            "default": variation,
        },
    ]
    variation = prompt(questions)
    return variation[0]

## プロフィールディレクトリ一覧の取得
def get_profile_dirs(variation=DEFAULT_VARIATION)->str:
    platform_type = (lambda v: v if v in ['Darwin', 'Windows'] else 'Linux')(platform.system())
    home_dir = os.getenv('LOCALAPPDATA') if platform_type == 'Windows' else os.path.expanduser('~')
    
    profile_home_dir = home_dir + LOCATIONS[platform_type][variation]
    profile_dirs = list(filter(
      lambda f : f != 'System Profile' and os.path.exists(os.path.join(f, 'Preferences')), 
      glob.glob(os.path.join(profile_home_dir,'*'))
    ))
    return profile_dirs



class Command:
    def status(self):
        show_status()
    def setup(self):
        set_profile_dir()

if __name__ == '__main__':
    #set_profile_dir()
    Fire(Command)