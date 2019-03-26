import requests
import json
from lib.config import config
from lib.error import Error
import docker


def get_json(url, token):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return True, json.loads(r.content.decode())
    except:
        return False, 'GetLatestJsonFailed'


def get_version(app_id, token):
    err, j = get_json(config.ADDRESS+'app_store/'+str(app_id)+'/mainfest', token)
    if err:
        return j['version']
    else:
        raise Error.UpdaterException(err)


def get_docker_name(app_id, token):
    err, j = get_json(config.ADDRESS+'app_store/'+str(app_id)+'/mainfest', token)
    if err:
        return j['docker_name']
    else:
        raise Error.UpdaterException(err)

def update_system(token):
    pass


def update_app(app_id,token):
    pass


def update_service(app_id, token):
    if app_id == 0:
        update_system(token)
    else:
        update_app(app_id,token)