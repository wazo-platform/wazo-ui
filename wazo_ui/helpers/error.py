# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re
import logging

from flask_babel import lazy_gettext as l_

GENERIC_MESSAGE_ERRORS = {
    'resource-not-found': l_('Resource not found'),
    'invalid-data': l_('Input error'),
}

SPECIFIC_MESSAGE_ERRORS = {
    'contains-only': l_('One or more of the choices you made was not acceptable'),
    'equal': l_('Invalid value'),
    'field-format-datetime': l_('cannot be formatted as a datetime'),
    'field-format-time': l_('cannot be formatted as date'),
    'field-format-timedelta': l_('cannot be formatted as a timedelta'),
    'field-invalid-boolean': l_('Not a valid boolean'),
    'field-invalid-datetime': l_('Not a valid datetime'),
    'field-invalid-dict': l_('Not a valid mapping type'),
    'field-invalid-email': l_('Not a valid email address'),
    'field-invalid-formatted-string': l_('Cannot format string with given data'),
    'field-invalid-integer': l_('Not a valid integer'),
    'field-invalid-number': l_('Not a valid number'),
    'field-invalid-string': l_('Not a valid string'),
    'field-invalid-time': l_('Not a valid time'),
    'field-invalid-timedelta': l_('Not a valid period of time'),
    'field-invalid-url': l_('Not a valid URL'),
    'field-invalid-uuid': l_('Not a valid UUID'),
    'field-null': l_('Field may not be null'),
    'field-required': l_('Missing data for required field'),
    'field-type': l_('Invalid input type'),
    'field-validator-failed': l_('Invalid value'),
    'input': l_('Invalid input'),
    'length': l_('Invalid length'),
    'oneof': l_('Not a valid choice'),
    'range': l_('Invalid range'),
    'regexp': l_('String does not match expected pattern'),
    'regex': l_('String does not match expected pattern')
}

logger = logging.getLogger(__name__)


class ErrorTranslator():
    generic_messages = {}
    specific_messages = {}
    resources = {}

    @classmethod
    def register_generic_messages(cls, messages):
        cls.generic_messages.update(messages)

    @classmethod
    def register_specific_messages(cls, messages):
        cls.specific_messages.update(messages)

    @classmethod
    def register_resources(cls, resources):
        cls.resources.update(resources)

    @classmethod
    def translate_constraint(cls, constraint):
        return cls.specific_messages.get(constraint, constraint)


# Match
# /1.1/users
# /1.1/users/id
# Do not match:
# /1.1/users/id/funckeys
RESOURCE_REGEX = r'^/[^/]+/([^/]+)(?:/[^/]+)?$'


class ErrorExtractor():
    url_to_name_resources = {}

    @classmethod
    def register_url_to_name_resources(cls, resources):
        cls.url_to_name_resources.update(resources)

    @classmethod
    def extract_resource(cls, request):
        # TODO: How to extract sub-resource like /users/id/funckeys
        regex = re.compile(RESOURCE_REGEX)
        match = regex.match(request.path_url)
        if not match:
            logger.debug('Unable to extract resource from: %s', request.path_url)
            return None
        url_resource = match.group(1)
        return cls.url_to_name_resources.get(url_resource, url_resource)

    @classmethod
    def extract_error_details(cls, details):
        result = {}
        for field, errors in details.items():
            if field not in result:
                result[field] = []

            if isinstance(errors, dict):
                result[field].append(cls.extract_error_detail(errors))
            elif isinstance(errors, list):
                for error in errors:
                    result[field].append(cls.extract_error_detail(error))

        return result

    @classmethod
    def extract_error_detail(cls, error):
        if 'constraint_id' not in error or 'constraint' not in error:
            logger.debug('Unable to extract error from: %s', error)
        else:
            constraint_message = ErrorTranslator.translate_constraint(error['constraint_id'])
            return '{constraint_message} ({constraint})'.format(
                constraint_message=constraint_message,
                constraint=error['constraint']
            )

    @classmethod
    def get_resource_from_error(cls, error):
        response = error.response.json()
        if 'resource' not in response:
            resource = ErrorExtractor.extract_resource(error.request)
        else:
            resource = response['resource']
        return ErrorTranslator.resources.get(resource, resource)
