import numpy as np
import pytest
from scipy.sparse import csr_matrix

import spartans as st

m = np.array([[1, -2, 0, 50],
              [0, 0, 0, 100],
              [1, 0, 0, 80],
              [1, 4, 0, 0],
              [0, 0, 0, 0],
              [0, 4, 0, 0],
              [0, 0, 0, -50]])
c = csr_matrix(m)
y = np.array([1, 1, 0, 0, 1, 0, 1])

options_axes = [0, 1, None]


@pytest.mark.parametrize('axis', options_axes)
def test_variance(axis):
    result = st.variance(c, axis=axis).squeeze()
    expected = m.var(axis=axis).squeeze()
    assert np.allclose(result, expected)


def test_cov():
    result = st.cov(c)
    expected = np.cov(m, rowvar=False, ddof=0)
    assert np.allclose(result, expected)


def test_cor():
    result = st.corr(c)
    expected = np.corrcoef(m, rowvar=False)
    assert np.allclose(result, expected, equal_nan=True)


def test_cor_y():
    result = st.corr(c, y)
    expected = np.corrcoef(m, y, rowvar=False)[:-1, -1]
    assert np.allclose(result, expected, equal_nan=True)


def test_constant_index_0():
    result = st.constant_index(c, axis=0, as_bool=False)
    expected = np.array([2])
    assert np.allclose(result, expected)


def test_constant_index_1():
    result = st.constant_index(c, axis=1, as_bool=False)
    expected = np.array([4])
    assert np.allclose(result, expected)


def test_non_constant_index():
    result = st.non_constant_index(c, 0, as_bool=False)
    expected = np.array([0, 1, 3])
    assert np.allclose(result, expected)


def test_non_constant_index_threshold():
    result = st.non_constant_index(c, 0, as_bool=True, threshold=1)
    expected = np.array([False, True, False, True])
    assert np.allclose(result, expected)
