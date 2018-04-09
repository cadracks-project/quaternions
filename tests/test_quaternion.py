#!/usr/bin/env python
# coding: utf-8

r"""quaternion tests"""

from quaternions.quaternion import Quaternion


def test_quaternion():
    r"""Test the bounding box on a box shape"""
    # mesh(box)
    q = Quaternion()
    assert q is not None
