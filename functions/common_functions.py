import os
import requests

def download_icon(icon_url, icon_name):
    """ Downloads icon, and saves it to data path.
    param icon_url:
    param icon_name:
    return icon_path:
    """
    icon_path = f'data/icons/{icon_name}.ico'
    if os.path.exists(icon_path):
        return icon_path
    icon_response = requests.get(icon_url)
    with open(icon_path, 'wb') as icon_file:
        icon_file.write(icon_response.content)
    return icon_path

