import pathlib
from datetime import datetime
import requests


def notify_mobile(message=''):
    response = requests.post(
        'https://maker.ifttt.com/trigger/bto_notify/with/key/123456789',
        data={
            'value1': message,
        }
    )
    print("IFTTT: ", response.text)
    return response


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


def get_save_dir(measurement_time=datetime.now()):
    current_dir = pathlib.Path(__file__).parent.resolve()
    save_dir = current_dir.parent / 'swabian' / measurement_time.strftime('%Y-%m-%d')
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def get_latest_save_dir():
    current_dir = pathlib.Path(__file__).parent.resolve()
    data_dir = current_dir.parent / 'swabian'
    save_dir = sorted(data_dir.glob('*-*-*'), reverse=True)[0]
    return save_dir

def timestamp():
    """Time stamping for swabian save"""
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')
