import configparser
import os


def loadConfig():
    """
    A function that load api_id, api_hash and phone number from config.ini
    Returns
    -------
    tuple (api_id, api_hash, phone_number)
    """
    config = configparser.ConfigParser()
    if not os.path.exists('appfiles/config.ini'):
        return
    config.read('appfiles/config.ini')
    api_id = int(config.get('API', 'ID'))
    api_hash = config.get('API', 'HASH')
    phone_number = config.get('API', 'PHONE')
    extended_report = config.get('REPORT', 'EXTENDED')
    return api_id, api_hash, phone_number, extended_report


def saveConfig(api_id, api_hash, phone_number, extended_report):
    """
    A function that save api_id, api_hash and phone number in config.ini
    Parameters
    ----------
    api_id: int
    api_hash string
    phone_number string

    Returns
    -------
    tuple (api_id, api_hash, phone_number)

    """
    if api_id is None or len(api_hash) == 0 or len(phone_number) == 0:
        return
    config = configparser.ConfigParser()
    config['API'] = {'ID': str(api_id),
                     'HASH': str(api_hash),
                     'PHONE': str(phone_number)}
    config['REPORT'] = {'EXTENDED': extended_report}
    with open('appfiles/config.ini', 'w') as configfile:
        config.write(configfile)
    return loadConfig()