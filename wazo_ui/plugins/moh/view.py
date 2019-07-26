# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import cgi

from flask_babel import lazy_gettext as l_
from flask import (
    jsonify,
    render_template,
    request,
    send_file,
    redirect,
    flash,
    url_for
)
from flask_classful import route
from io import BytesIO
from requests.exceptions import HTTPError

from wazo_ui.helpers.classful import (
    LoginRequiredView,
    extract_select2_params,
    build_select2_response
)
from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import MohForm, sort_map, mode_map


class MohView(BaseIPBXHelperView):
    form = MohForm
    resource = 'moh'

    @menu_item('.ipbx.moh', l_('Musics'), icon='music', multi_tenant=True)
    def index(self):
        return super().index()

    def _index(self, form=None):
        try:
            resource_list = self.service.list()
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self.form()
        form = self._populate_form(form)

        return render_template(self._get_template('list'),
                               form=form,
                               resource_list=resource_list,
                               listing_urls=self.listing_urls,
                               current_breadcrumbs=self._get_current_breadcrumbs(),
                               mode_map=mode_map,
                               sort_map=sort_map)

    def download_filename(self, uuid, moh_filename):
        response = self.service.download_filename(uuid, moh_filename)
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            _, params = cgi.parse_header(content_disposition)
            if params:
                moh_filename = params['filename']

        return send_file(
            BytesIO(response.content),
            attachment_filename=moh_filename,
            as_attachment=True,
            mimetype=response.headers.get('content-type')
        )

    def delete_filename(self, uuid, moh_filename):
        self.service.delete_filename(uuid, moh_filename)
        return redirect(url_for('.{}:{}'.format(self.__class__.__name__,
                                                'get'), id=uuid))

    @route('/upload_filename/<uuid>', methods=['POST'])
    def upload_filename(self, uuid):
        if 'moh_filename' not in request.files:
            flash('[upload] Upload attempt with no file', 'error')
            return redirect(url_for('.{}:{}'.format(self.__class__.__name__,
                                                    'get'), id=uuid))

        file = request.files.get('moh_filename')

        self.service.upload_filename(uuid, file.filename, file.read())

        return redirect(url_for('.{}:{}'.format(self.__class__.__name__,
                                                'get'), id=uuid))

    def _map_resources_to_form_errors(self, form, resources):
        form.populate_errors(resources.get('moh', {}))
        return form


class MohListingView(LoginRequiredView):

    def list_json(self):
        params = extract_select2_params(request.args)
        musiconhold = self.service.list(**params)
        results = [{'id': moh['name'], 'text': moh['name']} for moh in musiconhold['items']]
        return jsonify(build_select2_response(results, musiconhold['total'], params))
