# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


class PJSIPDocService(object):

    def __init__(self, confd_client):
        self._confd = confd_client
        self._cached_doc = None

    def get(self):
        if self._cached_doc is None:
            self._cached_doc = self._confd.pjsip_doc.get()

        return self._cached_doc


class PJSIPGlobalSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.pjsip_global.get()

    def update(self, pjsip_global):
        self._confd.pjsip_global.update(pjsip_global)


class PJSIPSystemSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.pjsip_system.get()

    def update(self, pjsip_system):
        self._confd.pjsip_system.update(pjsip_system)


class IaxGeneralSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'general': self._confd.iax_general.get(),
            'callnumberlimits': self._confd.iax_callnumberlimits.get()['items']
        }
        return resource

    def update(self, resource):
        self._confd.iax_callnumberlimits.update({'items': resource['callnumberlimits']})
        resource['general']['ordered_options'] = self._confd.iax_general.get()['ordered_options']
        self._confd.iax_general.update(resource['general'])


class SccpDocService(object):

    def get(self):
        return [
            {'id': 'cid_name', 'text': 'cid_name'},
            {'id': 'cid_num', 'text': 'cid_num'},
            {'id': 'setvar', 'text': 'setvar'},
        ]


class SccpGeneralSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.sccp_general.get()

    def update(self, sccp_general):
        self._confd.sccp_general.update(sccp_general)


class VoicemailGeneralSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'general': self._confd.voicemail_general.get(),
            'zonemessages': self._confd.voicemail_zonemessages.get()['items']
        }
        return resource

    def update(self, resource):
        self._confd.voicemail_zonemessages.update({'items': resource['zonemessages']})
        self._confd.voicemail_general.update(resource['general'])


class TimezoneService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def list_timezones(self):
        return self._confd.timezones.list()


class FeaturesGeneralSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'general': self._confd.features_general.get(),
            'featuremap': self._confd.features_featuremap.get(),
            'applicationmap': self._confd.features_applicationmap.get()
        }
        return resource

    def update(self, resource):
        self._confd.features_featuremap.update(resource['featuremap'])
        self._confd.features_applicationmap.update(resource['applicationmap'])
        self._confd.features_general.update(resource['general'])


class ConfBridgeGeneralSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        resource = {
            'wazo_default_user': self._confd.confbridge_wazo_default_user.get(),
            'wazo_default_bridge': self._confd.confbridge_wazo_default_bridge.get()
        }
        return resource

    def update(self, resource):
        self._confd.confbridge_wazo_default_user.update(resource['wazo_default_user'])
        self._confd.confbridge_wazo_default_bridge.update(resource['wazo_default_bridge'])
