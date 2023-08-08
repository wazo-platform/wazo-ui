# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask_babel import lazy_gettext as l_
from requests.exceptions import HTTPError
from flask_classful import route
from flask import request, redirect, render_template, flash, url_for

from wazo_ui.helpers.menu import menu_item
from wazo_ui.helpers.view import BaseIPBXHelperView

from .form import PhonebookForm, ManagePhonebookForm


class PhonebookView(BaseIPBXHelperView):
    form = PhonebookForm
    resource = 'phonebook'

    @menu_item('.ipbx.phonebooks', l_('Phonebooks'), icon="book", multi_tenant=True)
    @menu_item(
        '.ipbx.phonebooks.config',
        l_('Configuration'),
        order=1,
        icon="wrench",
        multi_tenant=True,
    )
    def index(self):
        return super().index()


class ManagePhonebookView(BaseIPBXHelperView):
    form = ManagePhonebookForm
    resource = 'phonebook'
    settings = 'manage_phonebook'

    @menu_item(
        '.ipbx.phonebooks.manage',
        l_('Contacts'),
        order=2,
        icon="users",
        multi_tenant=True,
    )
    def index(self, form=None):
        phonebook_uuid = request.args.get('phonebook_uuid')
        try:
            phonebook_list = self.service.list_phonebook()
            if len(phonebook_list['items']) < 1:
                flash(l_('Please add phonebook before adding contacts!'), 'error')
                return redirect(url_for('wazo_engine.phonebook.PhonebookView:index'))
            resource = phonebook_list['items'][0]
            phonebook_uuid = resource[
                'phonebook_uuid'
            ] = phonebook_uuid or resource.get('uuid')
            resource_list = self.service.list_contacts(phonebook_uuid)
        except HTTPError as error:
            self._flash_http_error(error)
            return redirect(url_for('wazo_engine.phonebook.PhonebookView:index'))

        form = form or self._map_resources_to_form(resource)
        form = self._populate_form(form)

        kwargs = {
            'form': form,
            'resource_list': resource_list,
            'phonebook_uuid': phonebook_uuid,
            'phonebook_list': phonebook_list['items'],
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

        flash(
            l_('%(resource)s: Resource has been created', resource=self.resource),
            'success',
        )
        return self._redirect_referrer_or('index')

    @route('/delete/<phonebook_uuid>/<id>', methods=['GET'])
    def delete(self, phonebook_uuid, id):
        try:
            self.service.delete_contact(phonebook_uuid, id)
            flash(
                l_(
                    '%(resource)s: Resource %(id)s has been deleted',
                    resource=self.resource,
                    id=id,
                ),
                'success',
            )
        except HTTPError as error:
            self._flash_http_error(error)

        return self._redirect_referrer_or('index')
