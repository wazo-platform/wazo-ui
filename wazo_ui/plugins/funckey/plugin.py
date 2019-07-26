# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_babel import lazy_gettext as l_

from wazo_ui.helpers.funckey import register_funckey_destination_form

from .form import (
    CustomFuncKeyDestination,
    ForwardServicesFuncKeyDestinationForm,
    GeneralServicesFuncKeyDestinationForm,
    OnlineRecFuncKeyDestinationForm,
    TransferServicesFuncKeyDestinationForm,
)


class Plugin(object):

    def load(self, dependencies):
        register_funckey_destination_form('custom', l_('Custom'), CustomFuncKeyDestination)
        register_funckey_destination_form('transfer', l_('Transfer'), TransferServicesFuncKeyDestinationForm)
        register_funckey_destination_form('service', l_('Service'), GeneralServicesFuncKeyDestinationForm)
        register_funckey_destination_form('forward', l_('Forward'), ForwardServicesFuncKeyDestinationForm)
        register_funckey_destination_form('onlinerec', l_('Online Recording'), OnlineRecFuncKeyDestinationForm)
