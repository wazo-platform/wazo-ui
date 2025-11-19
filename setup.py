#!/usr/bin/env python3
# Copyright 2018-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections import defaultdict
from glob import glob
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

PROJECT = 'wazo_ui'
AUTHOR = 'Wazo Authors'
EMAIL = 'dev@wazo.community'


class build_py(_build_py):
    """Ensure translations are compiled during build."""

    def run(self):
        self.run_command('compile_catalog')
        _build_py.run(self)


def get_package_data_recursive(data: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    The option `package_data` does not resolve `**` recursive globs.
    """
    matches = defaultdict(list)
    root_dir = Path(__file__).parent.resolve()
    for module, glob_patterns in data.items():
        module_dir = root_dir / module.replace('.', '/')
        for glob_pattern in glob_patterns:
            matches[module].extend(glob(str(module_dir / glob_pattern), recursive=True))
    return matches


setup(
    name=PROJECT,
    version='0.1',
    description='Wazo UI',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='https://github.com/wazo-platform/wazo-ui',
    packages=find_packages(),
    package_data=get_package_data_recursive(
        {
            'wazo_ui': [
                'static/**',
                'templates/**',
                'translations/**',
            ],
            'wazo_ui.plugins': [
                '*/static/**',
                '*/templates/**',
            ],
        }
    ),
    setup_requires=['babel'],
    install_requires=['babel'],
    zip_safe=False,
    cmdclass={
        'build_py': build_py,
    },
    entry_points={
        'console_scripts': [
            'wazo-ui = wazo_ui.bin.daemon:main',
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
            'phonebook = wazo_ui.plugins.phonebook.plugin:Plugin',
            'phone_number = wazo_ui.plugins.phone_number.plugin:Plugin',
            'plugin = wazo_ui.plugins.plugin.plugin:Plugin',
            'provisioning = wazo_ui.plugins.provisioning.plugin:Plugin',
            'queue = wazo_ui.plugins.queue.plugin:Plugin',
            'recording_announcement = wazo_ui.plugins.recording_announcement.plugin:Plugin',
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
    },
)
