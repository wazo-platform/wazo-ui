# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


class PJSIPGlobalSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        return self._confd.pjsip_global.get()

    def update(self, pjsip_global):
        self._confd.pjsip_global.update(pjsip_global)


class SipGeneralSettingsService(object):

    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        result = self._confd.sip_general.get()
        result['ordered_options'] = [{'option_key': values[0], 'option_value': values[1]} for values in result['ordered_options']]
        return result

    def update(self, sip_general):
        self._confd.sip_general.update(sip_general)


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
