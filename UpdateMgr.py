from lib.oneline_service import online_service
from lib.error import error
from lib.license import validate
from distutils.version import StrictVersion
from lib.log import log
from lib.message import queue
import json


class Updater(object):
    def __init__(self, app_id, installed_version, token):
        self.app_id = app_id
        self.installed_version = installed_version
        self.token = token
    
    def failed(self, error_word, action):
        message = {}
        message['app_id'] = self.app_id
        message['status'] = 'failed'
        message['error_word'] = error_word
        message['action'] = action
        return json.dumps(message)

    def success(self, status, action):
        message = {}
        message['app_id'] = self.app_id
        message['status'] = status
        message['action'] = action
        message['latest_version'] = self.latest_version
        message['installed_version'] = self.installed_version
        return json.dumps(message)

    # TODO 需要根据online_service.update_service(self.app_id, self.token)的返回值True/False生成一个消息，参考check_update
    def run_update(self):
        online_service.update_service(self.app_id, self.token)
        return 'TODO' # TODO

    def check_update(self):
        try:
            self.latest_version = online_service.get_version(self.app_id, self.token)
            if ( StrictVersion(self.latest_version) > StrictVersion(self.installed_version) ):
                return self.success('find_update', 'check_update')
            else:
                return self.success('latest', 'check_update')
        except error.UpdaterException as e:
            return self.failed(e.error_word, 'check_update')


def update_worker(ch, method, properties, body):
    message_rec = json.loads(body)
    app_id = message_rec['app_id']
    action = message_rec['action']
    if action == 'check_update':
        message_to_send = updaters[app_id].check_update()
        feedback.send_message(message_to_send)
    if action == 'run_update':
        message_to_send = updaters[app_id].run_update()
        feedback.send_message(message_to_send)
        pass
    pass


def get_app_vers():
    return { 0: '0.0.1' }


updaters = {}
token = validate.authToken()
local_version = get_app_vers()
for app in local_version:
    updaters[app] = Updater(app,local_version[app], token)
feedback = queue.MsgProducer('UpdateResult')
msg_handler = queue.MsgRecv('UpdateRequest', update_worker)
msg_handler.chan.start_consuming()
