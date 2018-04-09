# coding: utf-8

r"""Dual quaternion logic"""

import numpy as np
import pdb

from quaternions.dual_number import DualNumber


class DualQuaternion(object):
    """

    For more details about Dual quaternions see the following ref

    www.euclideanspace.com/maths/algebra/realNormedAlgebra/other/dualQuaternion
    https://en.wikipedia.org/wiki/Dual_quaternion

    Real Time skeletal Animation (Ladislav Kavan) 2007
    https://www.cs.utah.edu/~ladislav/thesis/LKthesisHiresPrint.pdf

    """

    def __init__(self, qr, qd):
        """
        Parameters
        ----------

        qr : Quaternion
            real part
        qd : Quaternion
            dual part

        """
        # assert(qr.shape==qd.shape), "%r , %r   " % (qr.shape,qd.shape)
        assert (qr.shape == qd.shape), pdb.set_trace()
        self.qr = qr
        self.qd = qd
        self.shape = self.qr.shape

    def __repr__(self):
        st = ''
        st += str(self.qr.scal()) + '+'
        if len(self.qr.vect().shape) > 1:
            st += str(self.qr.vect()[:, 0]) + ' i +'
            st += str(self.qr.vect()[:, 1]) + ' j +'
            st += str(self.qr.vect()[:, 2]) + ' k +'
            st += str(self.qd.scal()) + ' e +'
            st += str(self.qd.vect()[:, 0]) + ' ei+'
            st += str(self.qd.vect()[:, 1]) + ' ej+'
            st += str(self.qd.vect()[:, 2]) + ' ek'
        else:
            st += str(self.qr.vect()[0]) + ' i +'
            st += str(self.qr.vect()[1]) + ' j +'
            st += str(self.qr.vect()[2]) + ' k +'
            st += str(self.qd.scal()) + ' e +'
            st += str(self.qd.vect()[0]) + ' ei+'
            st += str(self.qd.vect()[1]) + ' ej+'
            st += str(self.qd.vect()[2]) + ' ek'

        return st

    def __neg__(self):
        return DualQuaternion(-self.qr, -self.qd)

    def __add__(self, other):
        return DualQuaternion(self.qr + other.qr, self.qd + other.qd)

    def __sub__(self, other):
        return DualQuaternion(self.qr - other.qr, self.qd - other.qd)

    def __rmul__(self, s):
        return DualQuaternion(s * self.qr, s * self.qd)

    def __mul__(self, other):
        c = self.qr * other.qr
        d = self.qr * other.qd + self.qd * other.qr
        return DualQuaternion(c, d)

    def __getitem__(self, key):
        return DualQuaternion(self.qr[key], self.qd[key])

    def __setitem__(self, key, val):
        self.qr[key] = val.qr
        self.qd[key] = val.qd

    def conj1(self):
        """Quaternion conjugaison

            (Q1 Q2)* = Q2*Q1*

        """
        return DualQuaternion(self.qr.conjugate(), self.qd.conjugate())

    def conj2(self):
        """Dual conjugaison """
        return DualQuaternion(self.qr, -self.qd)

    def conj3(self):
        """Quaternion Dual conjugaison
        ( conjugaison used for chaining displacement )

            dis * dqp * dis.conj3

        """
        return DualQuaternion(self.qr.conjugate(), -self.qd.conjugate())

    def abs(self):
        dq = self * self.conjugate()
        assert (np.allclose(dq.qr.vect(), 0))
        assert (np.allclose(dq.qd.vect(), 0))
        magnitude2 = DualNumber(dq.qr.scal(), dq.qd.scal())
        magnitude = magnitude2.sqrt()
        return magnitude


class DQPoint(DualQuaternion):
    """ Dual quaternion point

    The real part is unitary purely scalar quaternion
    The dual part is a QPoint

    """
    def __init__(self, pt):
        if len(pt.shape) > 1:
            N = pt.shape[0]
        else:
            N = 1
        DualQuaternion.__init__(self, Quaternion(np.ones((N, 1)),
                                                 np.zeros((N, 1))), QPoint(pt))