from dotenv import load_dotenv
import os
import configparser


class Config:
    load_dotenv()

    required_keys = [
        "TW_API_KEY",
        "TW_API_SECRET",
        "TW_ACCESS_TOKEN",
        "TW_ACCESS_TOKEN_SECRET",
    ]

    for key in required_keys:
        if key not in os.environ:
            raise Exception(f"{key} is not defined in .env")

    TW_API_KEY = os.getenv('TW_API_KEY', '')
    TW_API_SECRET = os.getenv('TW_API_SECRET', '')
    TW_ACCESS_TOKEN = os.getenv('TW_ACCESS_TOKEN', '')
    TW_ACCESS_TOKEN_SECRET = os.getenv('TW_ACCESS_TOKEN_SECRET', '')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')

    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini', encoding='utf-8')
    TW_DATE_INTERVAL = config_ini.get('Twitter', 'DateInterval')
    TW_BASE_SEARCH_QUERY = config_ini.get('Twitter', 'BaseSearchQuery')
    GOOGLE_DRIVE_ROOT_DIR = config_ini.get('GoogleDrive', 'RootDir')
    CSV_AFTER_DELETE = config_ini.getboolean('CSV', 'AfterDelete')
    SEND_POST_TO_SLACK = config_ini.getboolean('SLACK', 'SendPost')

    # In the case of Serverless, the number of places
    # where the write privilege can be used is limited.
    if config_ini.get('Deploy', 'Type') == "GCP_Cloud_Functions":
        DEPLOY_TYPE = "server_less"
    else:
        DEPLOY_TYPE = "local"
