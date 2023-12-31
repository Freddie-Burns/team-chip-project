from pathlib import Path
from datetime import datetime


SETTINGS_DIR = Path("../data/swabian/setting_sweeps")


def user_confirm(prompt="Continue? [y]/n", default=True):
    while(True):
        response = input(prompt)
        if len(response) == 0:
            if default is not None:
                return default
        elif response[0].lower() == 'y':
            return True
        elif response[0].lower() == 'n':
            return False


def user_confirm_exit(prompt="Continue?"):
    result = user_confirm('{} [y]/n'.format(prompt))
    if result is False:
        exit(2)


def timestamp():
    """Time stamping for swabian save"""
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')
