
import pytest

from metricas import cpi, spi, cv, sv, csi, etc, eac


def test_cpi():
    assert cpi(10, 20) == 2
    assert cpi(5, 15) == 3
    with pytest.raises(ZeroDivisionError):
        cpi(0, 20)

def test_spi():
    assert spi(20, 10) == 2
    assert spi(15, 5) == 3
    with pytest.raises(ZeroDivisionError):
        spi(10, 0)

def test_cv():
    assert cv(10, 20) == 10
    assert cv(5, 15) == 10
    assert cv(20, 10) == -10

def test_sv():
    assert sv(10, 20) == 10
    assert sv(5, 15) == 10
    assert sv(20, 10) == -10

def test_csi():
    assert csi(2, 5) == 10
    assert csi(3, 3) == 9
    assert csi(0, 10) == 0

def test_etc():
    assert etc(20, 10) == 10
    assert etc(15, 5) == 10
    assert etc(10, 10) == 0

def test_eac():
    assert eac(20, 10) == 2
    assert eac(15, 5) == 3
    with pytest.raises(ZeroDivisionError):
        eac(10, 0)