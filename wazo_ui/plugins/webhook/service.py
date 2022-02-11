# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class WebhookService(object):

    def __init__(self, webhookd, confd_client):
        self.webhookd = webhookd
        self._confd = confd_client

    def list(self):
        return self.webhookd.subscriptions.list()

    def create(self, resource):
        return self.webhookd.subscriptions.create(self._create_resource(resource))

    def get(self, uuid):
        return self.webhookd.subscriptions.get(uuid)

    def get_logs(self, uuid):
        return self.webhookd.subscriptions.get_logs(uuid)

    def delete(self, uuid):
        return self.webhookd.subscriptions.delete(uuid)

    def update(self, resource):
        webhook_id = resource.get('uuid')
        return self.webhookd.subscriptions.update(webhook_id, self._create_resource(resource))

    def list_services(self):
        return self.webhookd.subscriptions.list_services()

    def list_users(self):
        return self._confd.users.list(view='summary')

    def _create_resource(self, resource):
        return {
            'name': resource.get('name'),
            'service': resource.get('services'),
            'events': resource.get('events'),
            'events_user_uuid': resource.get('user_uuid', None),
            'config': {
                'url': resource.get('url'),
                'content_type': resource.get('content_type'),
                'method': resource.get('method'),
                'body': resource.get('body', ''),
                'verify_certificate': str(resource.get('verify_certificate', 'false')).lower()
            }
        }
