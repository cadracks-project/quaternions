# coding: utf-8

r"""Dual number logic"""

import numpy as np


class DualNumber(object):
    """ Class which implements dual numbers

        x = r + e d with e**2 = 0 

        x1 + x2 = r1 + r2 + e ( d1 + d2) 
        x1 - x2 = r1 - r2 + e ( d1 - d2) 
        x1 * x2 = (r1 * r2) + e ( r1 * d2 + d1 * r2 )
        conj(x) = r - e d
        1/x = 1/r  - e d/r**2 

    """
    def __init__(self, r, d):
        """
        r : real part 
        d : dual part 

        """
        self.r = r
        self.d = d
        self.shape = np.shape(self.r)

    def __repr__(self):
        st = ''
        st += str(self.r)+' + '
        st += str(self.d)+' e'
        return st

    def __neg__(self):
        return DualNumber(-self.r, -self.d)

    def __add__(self, other):
        return DualNumber(self.r+other.r, self.d+other.d)

    def __sub__(self, other):
        return DualNumber(self.r-other.r, self.d-other.d)

    def __mul__(self, other):
        c = self.r*other.r
        d = self.r*other.d+self.d*other.r
        return DualNumber(c, d)

    def __div__(self, other):
        # return(DualNumber(1.0*self.n/other.n,
        #                     (self.d*other.n-self.n*other.d)/(1.0*other.n**2)))
        return self*other.inv()

    def __getitem__(self, key):
        return DualNumber(self.r[key], self.d[key])

    def __setitem__(self, key, val):
        self.r[key] = val.r[key]
        self.d[key] = val.d[key]

    def sqrt(self):
        r""""""
        return DualNumber(np.sqrt(self.r), self.d/(2*np.sqrt(self.r)))

    def inv(self):
        assert self.r != 0, "pure dual numbers have no inverse"
        return DualNumber(1./self.r, -1.0*self.d/(self.r**2))