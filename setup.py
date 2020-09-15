#!/usr/bin/env python3
# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from distutils.cmd import Command as _Command
from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

PROJECT = 'wazo_ui'
AUTHOR = 'Wazo Authors'
EMAIL = 'dev@wazo.community'


class build_py(_build_py):
    def run(self):
        # self.run_command('compile_catalog')
        _build_py.run(self)


class BabelWrapper(object):
    DEFAULT_HEADER = u"""\
# Translations template for {PROJECT}.
# Copyright (C) 2018 The Wazo Authors  (see the AUTHORS file)
# This file is distributed under the same license as the
# {PROJECT} project.
# Wazo Dev Team <dev@wazo.community>, 2018.
#""".format(PROJECT=PROJECT)

    class Command(_Command):
        user_options = []

    class compile_catalog(Command):
        def __new__(cls, *args, **kwargs):
            return BabelWrapper().babel.compile_catalog(*args, **kwargs)

    class extract_messages(Command):
        def __new__(cls, *args, **kwargs):
            return BabelWrapper().babel.extract_messages(*args, **kwargs)

    class init_catalog(Command):
        def __new__(cls, *args, **kwargs):
            return BabelWrapper().babel.init_catalog(*args, **kwargs)

    class update_catalog(Command):
        def __new__(cls, *args, **kwargs):
            return BabelWrapper().babel.update_catalog(*args, **kwargs)

    @property
    def babel(self):
        from babel.messages import frontend as babel
        from babel.messages.catalog import Catalog as _Catalog

        class Catalog(_Catalog):
            def __init__(self,
                         project=PROJECT,
                         copyright_holder='The Wazo Authors  (see the AUTHORS file)',
                         msgid_bugs_address=EMAIL,
                         last_translator='{author} <{email}>'.format(author=AUTHOR, email=EMAIL),
                         language_team='en <{email}>'.format(email=EMAIL), **kwargs):
                super().__init__(header_comment=BabelWrapper.DEFAULT_HEADER,
                                 project=project, copyright_holder=copyright_holder,
                                 msgid_bugs_address=msgid_bugs_address, last_translator=last_translator,
                                 language_team=language_team, fuzzy=False, **kwargs)

        babel.Catalog = Catalog
        return babel


babel_wrapper = BabelWrapper()

setup(
    name=PROJECT,
    version='0.1',
    description='Wazo UI',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='https://github.com/wazo-platform/wazo-ui',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['babel'],
    install_requires=['babel'],
    zip_safe=False,

    cmdclass={
        'build_py': build_py,
        'compile_catalog': babel_wrapper.compile_catalog,
        'extract_messages': babel_wrapper.extract_messages,
        'init_catalog': babel_wrapper.init_catalog,
        'update_catalog': babel_wrapper.update_catalog,
    },

    entry_points={
        'console_scripts': [
            'wazo-ui=wazo_ui.bin.daemon:main',
        ],
        'wazo_ui.plugins': [
            'access_feature = wazo_ui.plugins.access_feature.plugin:Plugin',
            'authentication = wazo_ui.plugins.authentication.plugin:Plugin',
            'index = wazo_ui.plugins.index.plugin:Plugin',
            'application = wazo_ui.plugins.application.plugin:Plugin',
            'agent = wazo_ui.plugins.agent.plugin:Plugin',
            'cli = wazo_ui.plugins.cli.plugin:Plugin',
            'call_filter = wazo_ui.plugins.call_filter.plugin:Plugin',
            'call_permission = wazo_ui.plugins.call_permission.plugin:Plugin',
            'call_pickup = wazo_ui.plugins.call_pickup.plugin:Plugin',
            'cdr = wazo_ui.plugins.cdr.plugin:Plugin',
            'conference = wazo_ui.plugins.conference.plugin:Plugin',
            'context = wazo_ui.plugins.context.plugin:Plugin',
            'device = wazo_ui.plugins.device.plugin:Plugin',
            'dird_profile = wazo_ui.plugins.dird_profile.plugin:Plugin',
            'dird_source = wazo_ui.plugins.dird_source.plugin:Plugin',
            'dhcp = wazo_ui.plugins.dhcp.plugin:Plugin',
            'extension = wazo_ui.plugins.extension.plugin:Plugin',
            'external_auth = wazo_ui.plugins.external_auth.plugin:Plugin',
            'funckey = wazo_ui.plugins.funckey.plugin:Plugin',
            'general_settings = wazo_ui.plugins.general_settings.plugin:Plugin',
            'group = wazo_ui.plugins.group.plugin:Plugin',
            'global_settings = wazo_ui.plugins.global_settings.plugin:Plugin',
            'ha = wazo_ui.plugins.ha.plugin:Plugin',
            'hep = wazo_ui.plugins.hep.plugin:Plugin',
            'identity = wazo_ui.plugins.identity.plugin:Plugin',
            'incall = wazo_ui.plugins.incall.plugin:Plugin',
            'ivr = wazo_ui.plugins.ivr.plugin:Plugin',
            'line = wazo_ui.plugins.line.plugin:Plugin',
            'moh = wazo_ui.plugins.moh.plugin:Plugin',
            'outcall = wazo_ui.plugins.outcall.plugin:Plugin',
            'paging = wazo_ui.plugins.paging.plugin:Plugin',
            'parking_lot = wazo_ui.plugins.parking_lot.plugin:Plugin',
            'plugin = wazo_ui.plugins.plugin.plugin:Plugin',
            'provisioning = wazo_ui.plugins.provisioning.plugin:Plugin',
            'queue = wazo_ui.plugins.queue.plugin:Plugin',
            'rtp = wazo_ui.plugins.rtp.plugin:Plugin',
            'schedule = wazo_ui.plugins.schedule.plugin:Plugin',
            'sip_template = wazo_ui.plugins.sip_template.plugin:Plugin',
            'skill = wazo_ui.plugins.skill.plugin:Plugin',
            'skillrule = wazo_ui.plugins.skillrule.plugin:Plugin',
            'sound = wazo_ui.plugins.sound.plugin:Plugin',
            'switchboard = wazo_ui.plugins.switchboard.plugin:Plugin',
            'transport = wazo_ui.plugins.transport.plugin:Plugin',
            'trunk = wazo_ui.plugins.trunk.plugin:Plugin',
            'user = wazo_ui.plugins.user.plugin:Plugin',
            'voicemail = wazo_ui.plugins.voicemail.plugin:Plugin',
            'webhook = wazo_ui.plugins.webhook.plugin:Plugin',
        ],
    }
)
