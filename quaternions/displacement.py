# coding: utf-8

r"""Displacement logic"""

import numpy as np

from quaternions.quaternion import Quaternion, QPoint
from quaternions.dual_quaternion import DualQuaternion


class Displacement(DualQuaternion):
    """ Class implementing a displacement

    A displacement is a DualQuaternion built from a rotation and a translation

    Parameters
    ----------
    qr : unitary quaternion
    qt : pure vector

    """

    def __init__(self, qr=Quaternion(1+0j, 0+0j), qt=Quaternion(0j, 0+0j)):
        assert(np.allclose(abs(qr), 1))
        assert(np.allclose(qt.scal(), 0))
        DualQuaternion.__init__(self, qr, 0.5*qr*qt)

    def setdis(self, v):
        self.qd = 0.5 * QPoint(v)

    def setrotation(self, qr):
        self.qr = qr