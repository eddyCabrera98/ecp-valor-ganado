
def cpi(ac, ev):
    return ev/ac

def spi(ev, pv):
    return ev/pv

def cv(ac, ev):
    return ev - ac

def sv(pv, ev):
    return ev - pv

def csi(c, s):
    return c*s

def etc(ea, ac):
    return ea - ac 

def eac(b, cs):
    return b/cs

def bac(pvs):
    return sum(pvs)
