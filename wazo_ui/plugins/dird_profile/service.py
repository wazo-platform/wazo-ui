# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class DirdProfileService:

    def __init__(self, dird_client):
        self._dird = dird_client

    def list(self):
        return self._dird.profiles.list()

    def get(self, uuid):
        return self._dird.profiles.get(uuid)

    def update(self, profile_data):
        return self._dird.profiles.edit(profile_data['uuid'], profile_data)
