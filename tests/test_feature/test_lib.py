#!/usr/bin/env python
#-*- coding: utf-8 -*-
from mock import Mock
from nose.tools import assert_equals

from deploystream.providers.interfaces import IPlanningProvider
from deploystream.apps.feature.lib import get_all_features

NON_ASCII_STRING = u"都بيببيðéáöþ"


def test_non_ascii_chars():
    mock_provider = Mock()
    mock_provider.get_features.return_value = [{
        "project": NON_ASCII_STRING,
        "id": NON_ASCII_STRING,
        'title': NON_ASCII_STRING
    }]

    resp = get_all_features({IPlanningProvider: [mock_provider]})

    assert_equals(resp[0].title, NON_ASCII_STRING)
