# -*- coding: utf-8 -*-
""""
This module handles schema validation of json objects
"""

from jsonschema import validate, ValidationError


def is_valid(freelance: dict, schema: dict) -> bool:
    """
    Validate the freelance object against a schema
    :param freelance: the freelance object
    :param schema: the validation schema
    :return: if the object matches the schema
    """

    try:
        validate(instance=freelance, schema=schema)
    except ValidationError:
        return False

    return True
