#!/usr/bin/env python
# coding: utf-8

r"""quaternion use example"""

from quaternions.quaternion import Quaternion

q = Quaternion()

print(q)
print(q.normalize())
print(q.conjugate())

q = Quaternion(a=2, b=3)
print(q)

