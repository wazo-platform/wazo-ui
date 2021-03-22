# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging
import random
import string

import requests

from wazo_ui.helpers.service import BaseConfdService

logger = logging.getLogger(__name__)
ALPHANUMERIC_POOL = string.ascii_lowercase + string.digits


def generate_string(length=8):
    return ''.join(random.choice(ALPHANUMERIC_POOL) for _ in range(length))


class UserService(BaseConfdService):
    resource_confd = 'users'

    def __init__(self, confd_client, auth_client):
        self._confd = confd_client
        self._auth = auth_client

    def get(self, resource_id):
        resource = super().get(resource_id)
        wazo_user = self._auth.users.get(resource_id)
        resource['username'] = wazo_user['username']
        resource['auth_enabled'] = wazo_user['enabled']
        resource['call_permissions'] = self._build_call_permissions_list(resource['call_permissions'])
        return resource

    def import_csv(self, form):
        file_content = form.file.data.stream.read()
        result = self._confd.users.import_csv(file_content)
        if 'errors' in result:
            raise Exception(result['errors'][0]['message'])

    def export_csv(self):
        return self._confd.users.export_csv()

    def update_csv(self, form):
        file_content = form.file.data.stream.read()
        self._confd.users.update_csv(file_content)

    def _build_call_permissions_list(self, call_permissions):
        result = []
        for call_permission in call_permissions:
            result.append({'id': call_permission['id'], 'name': call_permission['name']})
        return result

    def list(self, limit=None, order=None, direction=None, offset=None, search=None):
        return self._confd.users.list(
            view='summary',
            search=search,
            order=order,
            limit=limit,
            direction=direction,
            offset=offset,
        )

    def get_line(self, line_id):
        return self._confd.lines.get(line_id)

    def get_device(self, device_id):
        return self._confd.devices.get(device_id)

    def get_registrar(self, registrar_id):
        return self._confd.registrars.get(registrar_id)

    def list_funckeys(self, user_uuid):
        return self._confd.users(user_uuid).list_funckeys()

    def create(self, user):
        username = user.pop('username')
        password = user.pop('password')
        user['uuid'] = super().create(user)['uuid']
        self._auth.users.new(
            uuid=user['uuid'],
            username=username or user['email'],
            password=password,
            firstname=user['firstname'],
            lastname=user['lastname'],
            email_address=user['email'],
            enabled=password is not None,
        )

        self._create_user_lines(user)

    def update(self, user):
        username = user.pop('username')
        password = user.pop('password')
        super().update(user)
        self._update_wazo_user(user, username, password)

        existing_user = self._confd.users.get(user)

        if user.get('fallbacks'):
            self._confd.users(user['uuid']).update_fallbacks(user['fallbacks'])

        if user.get('services'):
            self._confd.users(user['uuid']).update_services(user['services'])

        if user.get('forwards'):
            self._confd.users(user['uuid']).update_forwards(user['forwards'])

        if user.get('schedules'):
            self._update_schedules(existing_user, user)

        self._update_callpermissions(existing_user, user)

        self._update_voicemail(existing_user, user)
        self._update_user_lines(existing_user, user)

        if 'groups' in user and user.get('lines'):
            self._confd.users(user).update_groups(user['groups'])

        if user.get('funckeys'):
            self._confd.users(user['uuid']).update_funckeys(user['funckeys'])

    def delete(self, user_uuid):
        user = self._confd.users.get(user_uuid)
        self._delete_user_associations(user)
        try:
            self._auth.users.delete(user_uuid)
        except requests.HTTPError as e:
            error = e.response.json() or {}
            if error.get('error_id') != 'unknown-user':
                raise
        self._confd.users.delete(user_uuid)

    def _delete_user_associations(self, user):
        if user.get('voicemail'):
            self._confd.users(user['uuid']).remove_voicemail()

        lines = user.get('lines', [])
        for line in lines:
            device_id = self._confd.lines.get(line['id'])['device_id']
            if device_id:
                self._confd.lines(line['id']).remove_device(device_id)
            self._confd.lines.delete(line)

    def _create_user_lines(self, user):
        lines = user.get('lines', [])

        for line in lines:
            if not line.get('id'):
                line = self._create_line_and_associations(line)
            self._confd.users(user).add_line(line)

    def _update_wazo_user(self, user, username, password):
        self._auth.users.edit(
            user['uuid'],
            username=username or user['email'],
            firstname=user['firstname'],
            lastname=user['lastname'],
            enabled='auth_enabled' in user,
        )
        emails = [{'address': user['email'], 'confirmed': True, 'main': True}] if user['email'] else []
        self._auth.admin.update_user_emails(user['uuid'], emails)

        if password:
            self._auth.users.set_password(user['uuid'], password)

    def _update_schedules(self, existing_user, user):
        if existing_user['schedules']:
            schedule_id = existing_user['schedules'][0]['id']
            self._confd.users(user).remove_schedule(schedule_id)
        if user['schedules'][0].get('id'):
            self._confd.users(user).add_schedule(user['schedules'][0])

    def _update_callpermissions(self, existing_user, user):
        if existing_user:
            existing_call_permissions = self._confd.users.get(existing_user)['call_permissions']
            for existing_call_permission in existing_call_permissions:
                self._confd.users(existing_user).remove_call_permission(existing_call_permission['id'])

        for call_permission in user['call_permissions']:
            self._confd.users(user).add_call_permission(call_permission['id'])

    def _update_voicemail(self, existing_user, user):
        existing_voicemail_id = existing_user['voicemail'].get('id') if existing_user['voicemail'] else None
        voicemail_id = int(user['voicemail']['id']) if user['voicemail'].get('id') else None

        if existing_voicemail_id == voicemail_id:
            return

        if existing_voicemail_id:
            self._confd.users(user).remove_voicemail()

        if voicemail_id:
            self._confd.users(user).add_voicemail(user['voicemail'])

    def _update_user_lines(self, existing_user, user):
        lines = user.get('lines', [])
        line_ids = {line.get('id') for line in lines}
        existing_lines = existing_user['lines']
        existing_line_ids = {line['id'] for line in existing_lines}
        extensions_to_remove = []

        line_ids_to_remove = existing_line_ids - line_ids
        for line_id in line_ids_to_remove:
            line = self._confd.lines.get(line_id)
            device_id = line['device_id']
            extensions = line.get('extensions')
            if extensions:
                extensions_to_remove += extensions
            if device_id:
                self._confd.lines(line_id).remove_device(device_id)
            self._confd.lines.delete(line_id)

        for line in lines:
            if line.get('id'):
                self._update_line_and_associations(line)
            else:
                self._create_line_and_associations(line)

        if line_ids != existing_line_ids or self._get_first_line_id(lines) != self._get_first_line_id(existing_lines):
            self._confd.users(user).update_lines(lines)

        for line in lines:
            if line.get('id'):
                self._update_device_association(line['id'], line.get('device_id'))
            else:
                if line.get('device_id'):
                    self._confd.lines(line).add_device(line['device_id'])

        # Remove extensions associated to removed lines (should be done at the end to avoid relationship issues)
        for extension in extensions_to_remove:
            logger.info("deleting extension: " + str(extension['id']))
            self._confd.extensions.delete(extension['id'])

    def _get_first_line_id(self, lines):
        for line in lines:
            return line['id']
        return None

    def _update_device_association(self, line_id, device_id):
        existing_device_id = self._confd.lines.get(line_id)['device_id']

        if not device_id and not existing_device_id:
            return
        if device_id == existing_device_id:
            return

        if not device_id and existing_device_id:
            self._confd.lines(line_id).remove_device(existing_device_id)
        elif device_id and not existing_device_id:
            self._confd.lines(line_id).add_device(device_id)
        elif device_id != existing_device_id:
            self._confd.lines(line_id).remove_device(existing_device_id)
            self._confd.lines(line_id).add_device(device_id)

    def _create_line_and_associations(self, line):
        line['id'] = self._confd.lines.create(line)['id']

        if 'endpoint_sip' in line:
            # Note(pc-m): This is done here until we find a better solution
            # https://wazo-dev.atlassian.net/browse/WAZO-1912
            max_retries = 3
            for n in range(max_retries):
                name, password = generate_string(), generate_string()
                endpoint_sip_body = dict(line['endpoint_sip'])
                endpoint_sip_body['label'] = name
                endpoint_sip_body['name'] = name
                endpoint_sip_body['auth_section_options'] = [
                    ['username', name],
                    ['password', password],
                ]
                try:
                    endpoint_sip = self._confd.endpoints_sip.create(endpoint_sip_body)
                    break
                except requests.HTTPError as e:
                    if n == max_retries - 1:
                        raise
                    response = getattr(e, 'response', None)
                    status_code = getattr(response, 'status_code', None)
                    if status_code == 400 and '''["Resource Error - SIPEndpoint already exists ('name':''' in response.text:
                        logger.info('generated a duplicate endpoint_sip name. retrying...')
                        continue
                    raise
            if endpoint_sip:
                self._confd.lines(line).add_endpoint_sip(endpoint_sip)
        elif 'endpoint_sccp' in line:
            endpoint_sccp = self._confd.endpoints_sccp.create(line['endpoint_sccp'])
            if endpoint_sccp:
                self._confd.lines(line).add_endpoint_sccp(endpoint_sccp)
        elif 'endpoint_custom' in line:
            endpoint_custom = self._confd.endpoints_custom.create(line['endpoint_custom'])
            if endpoint_custom:
                self._confd.lines(line).add_endpoint_custom(endpoint_custom)
        else:
            logger.debug('No endpoint found for line: %s', line)
            return line

        if line.get('extensions'):
            self._create_or_associate_extension(line, line['extensions'][0])

        if line.get('application', {}).get('uuid'):
            self._confd.lines(line).add_application(line['application'])

        return line

    def _update_line_and_associations(self, line):
        if line.get('endpoint_sip'):
            self._confd.endpoints_sip.update(line['endpoint_sip'])

        if line.get('application', {}).get('uuid'):
            self._confd.lines(line).add_application(line['application'])
        else:
            existing_line = self._confd.lines.get(line['id'])
            if existing_line.get('application'):
                self._confd.lines(line).remove_application(existing_line['application'])

        extensions = line.get('extensions', [])
        if extensions and extensions[0].get('id'):
            old_extension = self._confd.extensions.get(extensions[0])
            form_extension = extensions[0]
            if self._is_extension_has_changed(form_extension, old_extension):
                new_extension = self._get_first_existing_extension(extensions[0])
                if (
                        not self._is_extension_associated_with_other_lines(old_extension)
                        and not new_extension
                ):
                    self._confd.extensions.update(form_extension)
                else:
                    if not new_extension:
                        new_extension = self._confd.extensions.create(form_extension)

                    self._confd.lines(line).remove_extension(old_extension)
                    self._confd.lines(line).add_extension(new_extension)

                    if not self._is_extension_associated_with_other_lines(old_extension):
                        self._confd.extensions.delete(old_extension)

        elif extensions:
            self._create_or_associate_extension(line, extensions[0])

        else:
            existing_extensions = self._confd.lines.get(line['id']).get('extensions')
            if existing_extensions:
                self._confd.lines(line).remove_extension(existing_extensions[0])
                self._confd.extensions.delete(existing_extensions[0])

        self._confd.lines.update(line)

    def _is_extension_associated_with_other_lines(self, extension):
        if len(extension['lines']) > 1:
            return True
        return False

    def _is_extension_has_changed(self, extension, existing_extension):
        if (existing_extension['exten'] == extension['exten']
                and existing_extension['context'] == extension['context']):
            return False
        return True

    def _create_or_associate_extension(self, line, extension):
        existing_extension = self._get_first_existing_extension(extension)

        if not existing_extension:
            existing_extension = self._confd.extensions.create(extension)

        if existing_extension:
            self._confd.lines(line).add_extension(existing_extension)

    def _get_first_existing_extension(self, extension):
        items = self._confd.extensions.list(exten=extension['exten'], context=extension['context'])['items']
        return items[0] if items else None

    def get_first_internal_context(self):
        result = self._confd.contexts.list(type='internal', limit=1, direction='asc', order='id')
        for context in result['items']:
            return context

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_endpoint_sip(self, uuid):
        return self._confd.endpoints_sip.get(uuid)

    def get_sip_template(self, uuid):
        return self._confd.endpoints_sip_templates.get(uuid)

    def get_call_permission(self, id):
        return self._confd.call_permissions.get(id)
