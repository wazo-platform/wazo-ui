# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class RtpService:
    def __init__(self, confd_client):
        self._confd = confd_client

    def get(self):
        rtp_general = self._confd.rtp_general.get()
        rtp_general['options']['ice_host_candidates'] = self._build_ice_host_candidates(
            self._confd.rtp_ice_host_candidates.get()['options']
        )
        return rtp_general

    def update(self, resource):
        self.update_ice_host_candidates(resource['ice_host_candidates'])
        resource.pop('ice_host_candidates')
        options = {'options': {k: v for k, v in resource.items() if v is not None}}
        return self._confd.rtp_general.update(options)

    def update_ice_host_candidates(self, resource):
        options = {'options': {}}
        for option in resource:
            options['options'].update({option['option_key']: option['option_value']})
        self._confd.rtp_ice_host_candidates.update(options)

    def _build_ice_host_candidates(self, options):
        result = []
        for k, v in options.items():
            result.append({'option_key': k, 'option_value': v})

        return result
