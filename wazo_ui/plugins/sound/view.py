# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import cgi

from io import BytesIO

from flask import jsonify, request, render_template, redirect, url_for, send_file, flash
from flask_babel import lazy_gettext as l_
from flask_babel import gettext as _
from flask_classful import route
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import LoginRequiredView
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import SoundForm, SoundFilenameForm


class SoundView(BaseIPBXHelperView):
    form = SoundForm
    resource = 'sound'

    @menu_item('.ipbx.sound_greeting.sound', l_('Sound Files'), icon="file-sound-o", multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        sounds = []
        for sound in resource_list['items']:
            if sound['name'] == 'system':
                continue
            sound['id'] = sound['name']
            sounds.append(sound)

        resource_list['items'] = sounds

        return render_template(self._get_template('list'),
                               form=self.form(),
                               resource_list=resource_list,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    @route('/delete/<tenant_uuid>/<category>')
    def delete(self, tenant_uuid, category):
        try:
            self.service.delete(tenant_uuid, category)
            flash(_('%(resource)s: Resource %(category)s has been deleted', resource=self.resource, category=category), 'success')
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_for('index')

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('sound', {}))
        return form


class SoundFileView(BaseIPBXHelperView):
    form = SoundFilenameForm
    resource = 'sound'

    @menu_item('.ipbx.global_settings.sound_system', l_('Sound Files System'), order=2, icon="file-sound-o")
    def sound_files_system(self):
        sound = self._get_sound_by_category(tenant_uuid=None, category='system')
        return render_template(self._get_template('list_system_files'),
                               form=self.form(),
                               sound=sound,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    @route('/list_files/<tenant_uuid>/<category>')
    def list_files(self, tenant_uuid, category):
        sound = self._get_sound_by_category(tenant_uuid, category)
        return render_template(self._get_template('list_files'),
                               form=SoundFilenameForm(),
                               sound=sound,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               listing_urls=self.listing_urls)

    def _get_sound_by_category(self, tenant_uuid, category):
        try:
            sound = self.service.get(tenant_uuid, category)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        return sound

    def download_sound_filename(self, tenant_uuid, category, filename):
        response = self.service.download_sound_filename(
            tenant_uuid,
            category,
            filename,
            format_=request.args.get('format'),
            language=request.args.get('language'),
        )
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            _, params = cgi.parse_header(content_disposition)
            if params:
                filename = params['filename']

        return send_file(
            BytesIO(response.content),
            attachment_filename=filename,
            as_attachment=True,
            mimetype=response.headers.get('content-type')
        )

    def download_system_sound_filename(self, filename):
        return self.download_sound_filename(tenant_uuid=None, category='system', filename=filename)

    @route('/upload_sound_filename/<tenant_uuid>/<category>', methods=['POST'])
    def upload_sound_filename(self, tenant_uuid, category):
        if 'name' not in request.files:
            flash(l_('[upload] Upload attempt with no file'), 'error')
            return redirect(url_for('.SoundFileView:list_files', tenant_uuid=tenant_uuid, category=category))

        file_ = request.files.get('name')

        form = self.form()
        resources = self._map_form_to_resources_post(form)
        del resources['name']

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return redirect(url_for('.SoundFileView:list_files', tenant_uuid=tenant_uuid, category=category))

        try:
            self.service.upload_sound_filename(tenant_uuid, category, file_.filename, file_.read(), **resources)
        except HTTPError as error:
            self._flash_http_error(error)

        return redirect(url_for('.SoundFileView:list_files', tenant_uuid=tenant_uuid, category=category))

    def delete_sound_filename(self, tenant_uuid, category, filename):
        self.service.delete_sound_filename(
            tenant_uuid,
            category,
            filename,
            format_=request.args.get('format'),
            language=request.args.get('language')
        )
        return redirect(url_for('.SoundFileView:list_files', tenant_uuid=tenant_uuid, category=category))

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('sound', {}))
        return form


class SoundListingView(LoginRequiredView):

    def list_json(self):
        sounds = self.service.list()
        results = []
        for sound in sounds['items']:
            for file_ in sound['files']:
                for format_ in file_['formats']:
                    results.append({
                        'text': '{}{}{}'.format(
                            file_['name'],
                            ' [{}]'.format(format_['format']) if format_['format'] else '',
                            ' ({})'.format(format_['language']) if format_['language'] else '',
                        ),
                        'id': file_['name'] if sound['name'] == 'system' else format_['path'],
                    })

        return jsonify({'results': results})
