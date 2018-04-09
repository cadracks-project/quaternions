# coding: utf-8

r"""Quaternion logic"""

import numpy as np
import copy


class Quaternion(object):
    r"""Quaternion class

    Parameters
    ----------
    a : np.array (Nx4) dtype=complex
    b : np.array (Nx4) dtype=complex

    """
    def __init__(self, a=1, b=0):
        """

        """
        # if type(a) != np.ndarray:
        if not isinstance(a, np.ndarray):
            self.a = np.array([a])[:, None].astype(complex)
            self.b = np.array([b])[:, None].astype(complex)
        else:
            if len(a.shape) == 2:
                self.a = a.astype(complex)
                self.b = b.astype(complex)
            else:
                self.a = a[:, None].astype(complex)
                self.b = b[:, None].astype(complex)

        assert(self.a.shape == self.b.shape)
        self.shape = np.shape(self.a)

    def __repr__(self):
        st = ''
        st += str(self.a.real)+' + '
        st += str(self.a.imag)+'i + '
        st += str(self.b.real)+'j + '
        st += str(self.b.imag)+'k'
        return st

    def __neg__(self):
        return Quaternion(-self.a, -self.b)

    def __add__(self, other):
        return Quaternion(self.a+other.a, self.b+other.b)

    def __sub__(self, other):
        return Quaternion(self.a-other.a, self.b-other.b)

    def __mul__(self, other):
        c = self.a*other.a-self.b*other.b.conjugate()
        d = self.a*other.b+self.b*other.a.conjugate()
        return Quaternion(c, d)

    def __rmul__(self, k):
        return Quaternion(self.a*k, self.b*k)

    def __abs__(self):
        return np.hypot(abs(self.a), abs(self.b))

    def __getitem__(self, key):
        return Quaternion(self.a[key], self.b[key])

    def __setitem__(self, key, val):
        self.a[key] = copy.copy(val.a)
        self.b[key] = copy.copy(val.b)

    def normalize(self):
        r"""Normalized version of the Quaternion"""
        return (1 / abs(self)) * self

    def conjugate(self):
        return Quaternion(self.a.conjugate(), -self.b)

    def polar(self):
        mq = abs(self)
        qu = (1./mq)*self
        return mq, qu

    def scal(self):
        return self.a.real

    def vect(self):
        v = np.hstack((self.a.imag, self.b.real, self.b.imag)).T
        return v

    def vecang(self):
        v = self.vect()
        cas2 = self.scal()
        sas2 = np.sqrt(np.sum(v*v))
        vn = v/sas2
        angle = 2. * np.arctan2(sas2, cas2)
        return vn, angle

    def from_mat(self, M):
        tr = np.trace(M)
        if tr > 0:
            S = np.sqrt(tr+1.0)*2
            self.a = 0.25 * S + 1j * (M[2, 1] - M[1, 2])/S
            self.b = (M[0, 2]-M[2, 0]/S)+1j*(M[1, 0]-M[0, 1])/S
        elif (M[0, 0] > M[1, 1]) & (M[0, 0] > M[2, 2]):
            S = np.sqrt(1.0 + M[0, 0] - M[1, 1] - M[2, 2])*2
            self.a = (M[2, 1] - M[1, 2])/S + 1j * 0.25 * S
            self.b = (M[0, 1] + M[1, 0])/S + 1j*(M[0, 2] + M[2, 0])/S
        elif M[1, 1] > M[2, 2]:
            S = np.sqrt(1.0 + M[1, 1] - M[0, 0] - M[2, 2])*2
            self.a = (M[0, 2] - M[2, 0])/S+1j*(M[0, 1]+M[1, 0])/S
            self.b = 0.25*S + 1j * (M[1, 2] + M[2, 1]) / S
        else:
            S = np.sqrt(1.0 + M[2, 2] - M[0, 0] - M[1, 1])*2
            self.a = (M[1, 0] - M[0, 1])/S + 1j * (M[0, 2] + M[2, 0])/S
            self.b = (M[1, 2] + M[2, 1])/S + 1j * 0.25 * S

    def __div__(self, other):
        u = 1./abs(other)**2
        qu = Quaternion(u+0j, np.zeros(u.shape)+0j)
        qv = qu*other.conjugate()
        return self*qv

    def log(self):
        q = abs(self)
        v = self.vect()
        if len(v.shape) > 1:
            vn = v/np.sqrt(np.sum(v*v, axis=1))
            v2 = np.arccos(self.a.real/q)*vn
            a = np.log(q) + 1j*v2[:, 0]
            b = v2[:, 1]+1j*v2[:, 2]
        else:
            vn = v/np.sqrt(np.sum(v*v))
            v2 = np.arccos(self.a.real/q)*vn
            a = np.log(q) + 1j*v2[0]
            b = v2[1]+1j*v2[2]
        return Quaternion(a, b)

    def exp(self):
        """ exponential of a quaternion"""
        ea = np.exp(self.a.real)
        v = self.vect()
        if len(v.shape) > 1:
            theta = np.sqrt(np.sum(v*v, axis=1))
            vn = v/theta
            a = np.cos(theta)+1j*np.sin(theta)*vn[:, 0]
            b = np.sin(theta)*(vn[:, 1]+1j*vn[:, 2])
        else:
            theta = np.sqrt(np.sum(v*v))
            vn = v/theta
            a = np.cos(theta)+1j*np.sin(theta)*vn[0]
            b = np.sin(theta)*(vn[1]+1j*vn[2])

        ev = Quaternion(a, b)
        return ea*ev

    def __pow__(self, n):
        r = 1
        for _ in range(n):
            r *= self
        return r


class QPoint(Quaternion):
    """ Quaternion point

    The scalar part is 0

    """
    def __init__(self, pt):
        if len(pt.shape) == 2:
            Quaternion.__init__(self, 1j * pt[:, 0][:, None],
                                pt[:, 1][:, None] + 1j * pt[:, 2][:, None])
        else:
            Quaternion.__init__(self, 1j * np.array([pt[0]])[:, None]
                                , np.array([pt[1]])[:, None]
                                + 1j * np.array([pt[2]])[:, None])
