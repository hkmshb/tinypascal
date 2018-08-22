#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tinypascal import get_version


def test_version_detail():
    version = get_version()
    assert version == '0.1.dev0'
