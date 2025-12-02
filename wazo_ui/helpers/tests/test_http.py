# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from wazo_ui.helpers.http import parse_content_disposition_filename


class TestParseContentDispositionFilename(unittest.TestCase):
    CONTENT_DISPOSITION_FILENAMES = [
        ('inline', None),
        ('attachment', None),
        ('attachment; filename="file name.jpg"', 'file name.jpg'),
        ('attachment; filename*=UTF-8\'\'file%20name.jpg', 'file name.jpg'),
    ]

    def test_parse_content_disposition_filename(self):
        for header, expected_filename in self.CONTENT_DISPOSITION_FILENAMES:
            filename = parse_content_disposition_filename(header)
            assert filename == expected_filename
