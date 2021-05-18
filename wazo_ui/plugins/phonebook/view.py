# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError
from flask_classful import route
from flask import (
    request,
    redirect,
    render_template,
    flash
)

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import PhonebookForm, ManagePhonebookForm


class PhonebookView(BaseIPBXHelperView):
    form = PhonebookForm
    resource = 'phonebook'

    @menu_item('.ipbx.phonebooks', l_('Phonebooks'), icon="book", multi_tenant=True)
    @menu_item('.ipbx.phonebooks.config', l_('Configuration'), order=1, icon="wrench", multi_tenant=True)
    def index(self):
        return super().index()


class ManagePhonebookView(BaseIPBXHelperView):
    form = ManagePhonebookForm
    resource = 'phonebook'
    settings = 'manage_phonebook'

    @menu_item('.ipbx.phonebooks.manage', l_('Contacts'), order=2, icon="users", multi_tenant=True)
    def index(self, form=None):
        phonebook_id = request.args.get('phonebook_id')
        try:
            phonebook_list = self.service.list_phonebook()
            resource = phonebook_list['items'][0]
            phonebook_id = resource['phonebook_id'] = phonebook_id or resource['id']
            resource_list = self.service.list_contacts(phonebook_id)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('admin.Admin:get'))

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        kwargs = {
            'form': form,
            'resource_list': resource_list,
            'phonebook_id': phonebook_id,
            'phonebook_list': phonebook_list['items']
        }
        if self.listing_urls:
            kwargs['listing_urls'] = self.listing_urls
        return render_template(self._get_template(self.settings), **kwargs)

    def post(self):
        form = self.form()
        resources = self._map_form_to_resources_post(form)

        if not form.csrf_token.validate(form):
            self._flash_basic_form_errors(form)
            return self._new(form)

        try:
            self.service.create_contact(resources)
        except HTTPError as error:
            form = self._fill_form_error(form, error)
            self._flash_http_error(error)
            return self._new(form)

        flash(l_('%(resource)s: Resource has been created', resource=self.resource), 'success')
        return self._redirect_referrer_or('index')

    @route('/delete/<phonebook_id>/<id>', methods=['GET'])
    def delete(self, phonebook_id, id):
        try:
            self.service.delete_contact(phonebook_id, id)
            flash(l_('%(resource)s: Resource %(id)s has been deleted', resource=self.resource, id=id), 'success')
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')
