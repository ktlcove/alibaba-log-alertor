import datetime
import logging
import os

from aliyun.log import LogClient, LogException

from kube_admission import http_main as admission_main
from kube_admission.app import app, ABCAdmissionReviewView

logger = logging.getLogger(__name__)


def get_config():
    c = {
        'endpoint': os.getenv('ENDPOINT'),
        'accessKeyId': os.getenv('ACCESS_KEY_ID'),
        'accessKey': os.getenv('ACCESS_KEY_SECRET'),
        'logProjectName': os.getenv('LOG_PROJECT_NAME'),
    }

    for key, value in c.items():
        if not value:
            raise RuntimeError(f'init failed with not found value for env {key}.')
    return c


configs = get_config()


class AliyunSLS:
    def __init__(self):
        self.client = LogClient(configs['endpoint'],
                                configs['accessKeyId'],
                                configs['accessKey'])
        self.project = configs['logProjectName']

    def create_alert(self, detail, project=None):
        dashboard_name = detail['configuration']['dashboard']
        self.ensure_dashboard(dashboard_name, project=project)
        resp = self.client.create_alert(project or self.project, detail)
        return resp.body

    def update_alert(self, detail, project=None):
        resp = self.client.update_alert(project or self.project, detail)
        return resp.body

    def delete_alert(self, name, project=None):
        resp = self.client.delete_alert(project or self.project, name)
        return resp.body

    def get_alert(self, name, project=None):
        resp = self.client.get_alert(project or self.project, name)
        return resp.body

    def ensure_dashboard(self, name, project=None):
        try:
            self.client.get_dashboard(project or self.project, name)
        except LogException as e:
            self.client.create_dashboard(project or self.project,
                                         {'dashboardName': name,
                                          'displayName': name,
                                          'charts': [],
                                          'description': ''})

    # def add_chart_to_dashboard(self, name, chart_title, detail, project=None):
    #     pass


@app.route('/api/v1alpha1/mutate', methods=['POST', ])
class Mutate(ABCAdmissionReviewView):
    client = AliyunSLS()

    @staticmethod
    def ts_to_string(ts, tz=None):
        return datetime.datetime.fromtimestamp(ts, tz=tz).strftime('%Y-%m-%d %H:%M:%S')

    def get_alert_status(self, name):
        resp = self.client.get_alert(name)
        return {
            'detail': {
                'createTime': self.ts_to_string(resp['createTime']),
                'lastModifiedTime': self.ts_to_string(resp['lastModifiedTime']),
                'status': resp['status'],
            }
        }

    async def on_create(self, req):
        alert_configs = req.admission.request_object['spec']
        detail = alert_configs.get('detail')
        # todo: support cross project alert
        # project = alert_configs.get('project', configs['logProjectName'])
        self.client.create_alert(detail)
        return await self.patch_status_response(req, msg=self.get_alert_status(detail['name']))

    async def on_delete(self, req):
        alert_name = req.admission.request_old_object['spec']['detail']['name']
        self.client.delete_alert(alert_name)
        return await self.allow_response(req)

    async def on_update(self, req):
        alert_configs = req.admission.request_object['spec']
        detail = alert_configs.get('detail')
        self.client.update_alert(detail)
        return await self.patch_status_response(req, msg=self.get_alert_status(detail['name']))


def http_main():
    return admission_main('aliyun_log_alertor:app')
