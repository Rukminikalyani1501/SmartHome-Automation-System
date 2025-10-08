import requests

from model import Device


def turn_on_light():
    return change_color_red()


def turn_off_light():
    url = f"http://{Device.query.filter_by(device_name='RGBLight').first().IP}/RGBLight/off"
    response = requests.get(url)
    if response.status_code == 200:
        return 'Light Turned off'
    else:
        return "Failed to turn off the light"


def change_color_blue():
    url = f"http://{Device.query.filter_by(device_name='RGBLight').first().IP}/RGBLight/color?red={255}&green={0}&blue={255}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        print("Failed to change the color")


def change_color_red():
    url = f"http://{Device.query.filter_by(device_name='RGBLight').first().IP}/RGBLight/color?red={255}&green={255}&blue={0}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        print("Failed to change the color")


def change_color_pink():
    url = f"http://{Device.query.filter_by(device_name='RGBLight').first().IP}/RGBLight/color?red={255}&green={100}&blue={0}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        print("Failed to change the color")


def change_color_purple():
    url = f"http://{Device.query.filter_by(device_name='RGBLight').first().IP}/RGBLight/color?red={255}&green={0}&blue={0}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        print("Failed to change the color")


def lock_door():
    url = f"http://{Device.query.filter_by(device_name='DoorLock').first().IP}/DoorLock/lock"
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        return 'Door have been locked.'
    else:
        return 'Failed to lock the door.'


def unlock_door():
    url = f"http://{Device.query.filter_by(device_name='DoorLock').first().IP}/DoorLock/unlock"
    response = requests.get(url)
    if response.status_code == 200:
        return 'Door have been unlocked'
    else:
        return 'Failed to unlock the door.'
