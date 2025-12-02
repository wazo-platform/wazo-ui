# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from email.message import Message


def parse_content_disposition_filename(content_disposition: str) -> str | None:
    """
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Disposition
    """
    msg = Message()
    msg['content-disposition'] = content_disposition
    return msg.get_filename()
