# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_
from flask_menu.classy import register_flaskview

from wazo_ui.helpers.funckey import register_funckey_destination_form
from wazo_ui.helpers.plugin import create_blueprint
from wazo_ui.helpers.view import register_listing_url

from .form import CallFilterFuncKeyDestinationForm
from .service import CallFilterService
from .view import CallFilterView, CallFilterMemberListingView

call_filter = create_blueprint('call_filter', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']
        clients = dependencies['clients']

        CallFilterView.service = CallFilterService(clients['wazo_confd'])
        CallFilterView.register(call_filter, route_base='/callfilters')
        register_flaskview(call_filter, CallFilterView)

        CallFilterMemberListingView.service = CallFilterService(clients['wazo_confd'])
        CallFilterMemberListingView.register(call_filter, route_base='/callfilters_listing')

        register_funckey_destination_form('bsfilter', l_('Call Filter'), CallFilterFuncKeyDestinationForm)
        register_listing_url('bsfilter', 'call_filter.CallFilterMemberListingView:list_json')

        core.register_blueprint(call_filter)
