from warnings import warn

import numpy as np
from scipy import sparse


def asarray(a):
    """convenience - turn np.matrix to np.array including dim reduction"""
    return np.array(a).squeeze()


def density(x):
    return x.getnnz() / (x.shape[0] * x.shape[1])


def _sum_false(msk, axis):
    if axis is None:
        top = msk.shape[0] * msk.shape[1]
    else:
        top = msk.shape[axis]
    return asarray(top - msk.sum(axis=axis))


def make_nan_mask(x):
    nans = np.isnan(x.data)
    msk = sparse.csc_matrix((nans, x.indices, x.indptr), shape=x.shape).copy()
    msk.eliminate_zeros()
    return msk


def mean(x, axis=None, mask=None, safe=False, **kwargs):
    if mask is None:
        m = np.mean(x, axis=axis, **kwargs)
        if np.isnan(m).sum() > 0:
            warn('Result contains nans. Consider adding a nan mask')
        return asarray(m)
    assert x.shape == mask.shape, 'x and mask must have the same shape'
    assert mask.dtype == 'bool', 'mask must be boolean'
    if safe:
        warn("Masking is safe making sure original matrix is zeroed. May be slow")
        xcp = x.copy()
        xcp[mask] = 0
        xcp.eliminate_zeros()
    else:
        xcp = x
    s = xcp.sum(axis=axis, )
    c = _sum_false(mask, axis=axis)
    return asarray(s / c)


def variance(x, axis=None, mask=None, **kwargs):
    """
    Returns variance by axis or for entire sparse matrix

    Parameters
    ----------
    mask
    x : sparse.csr_matrix
        matrix to compute variance for
    axis : int or None
        axis to return variance for, or None if for entire matrix
    kwargs
        passed to np.mean

    Returns
    -------
    var_ : array_like
        array of ndim=1 if axis is given or 0 dim (scalar) if axis is None
    """
    L = mean(x.power(2), axis=axis, mask=mask, **kwargs)
    R = np.power(mean(x, axis=axis, mask=mask, **kwargs), 2)
    var_ = asarray(L - R)
    return var_


# cov and corr
def _cov_block(x, y=None, mask=None):
    '''Uses cov(x,y) = e(xy) - e(x)e(y)'''
    xmean = mean(x, axis=0, mask=mask).reshape(-1, 1)
    if y is None:
        y = x
        ymean = xmean.T
    else:
        assert x.shape[0] == y.shape[0], 'x and y must have same number of rows'
        ymean = mean(y, axis=0, mask=mask).reshape(-1, 1).T
    R = xmean.dot(ymean).squeeze()
    L = x.T.dot(y)
    L = L / x.shape[0]
    #
    return L - R


def cov(x, y=None, mask=None, blocks=1):
    """

    Parameters
    ----------
    x : sparse matrix
        Data Matrix
    y : array_like
        target array
    mask : sparse matrix [bool]
        mask of values to consider as nan
    blocks : int
        amount of blocks of computing (for large matrices)

    Returns
    -------
    ret
        covariance vector if y in given, also auto-covariance for x

    """
    if blocks == 1:
        return _cov_block(x, y, mask)
    else:
        raise NotImplementedError
        # TODO Blocks Code
        # rows, cols = m.shape
        # block_size = rows // blocks
        # ret = np.empty((cols, cols))
        # for i in tqdm_notebook(range(blocks)):
        #     mi =
        #     _cov_block()


def _autocorr(x, mask=None):
    '''
    Returns a correlation matrix for the features of matrix x

    Parameters
    ----------
    x :  sparse matrix
        data matrix
    mask : sparse matrix [bool]
        mask of values to consider as nan

    Returns
    -------
    np.ndarray
        correlation matrix ndim=2

    '''
    cv = cov(x, mask=mask)
    dv = np.sqrt(np.diag(cv))
    corr = cv / dv[:, None]
    corr = corr / dv[None, :]
    return corr


def _corr_target(x, y, mask=None):
    '''
    Return a correlation vector between matrix x and target column y

    Parameters
    ----------
    x : sparse matrix
        Data Matrix
    y : array_like
        target array
    mask : sparse matrix [bool]
        mask of values to consider as nan
    Returns
    -------
    np.ndarray
        vector of correlation to target column ndim=1
    '''
    cv = cov(x, y, mask=mask)
    xvar = variance(x, axis=0, mask=mask)
    yvar = y.var()
    return cv / np.sqrt(xvar * yvar)


def corr(x, y=None, mask=None):
    '''
    Return a correlation vector between matrix x and target column y if given,
    else a auto-correlation matrix for the features of matrix x

    Parameters
    ----------
    x : sparse matrix
        Data Matrix
    y : array_like
        target array
    mask : sparse matrix [bool]
        mask of values to consider as nan
    Returns
    -------
    ret
        correlation vector if y in given, also auto-correlation for x
    '''
    if y is None:
        ret = _autocorr(x, mask=mask)
    else:
        ret = _corr_target(x, y, mask=mask)
    return np.array(ret)


# Indexing
def non_zero_index(x, axis, as_bool=True):
    """
    return the index of all rows/features that are not all zero

    Parameters
    ----------
    x : sparse matrix
        data matrix
    axis : int
        axis to return indices for
    mask : sparse matrix [bool]
        mask of values to consider as nan
    as_bool : bool
        whether to return a mask of bool indices or vector of numbers

    Returns
    -------
    cond : array_like
        Either an array with number of indices or boolean mask
    """
    abs_ = abs(x).sum(axis=axis)
    cond = asarray(abs_)
    if as_bool:
        return cond.astype(bool)
    else:
        return cond.nonzero()[0]


def non_constant_index(x, axis, mask=None, as_bool=True, threshold=0, method='variance'):
    """
    Returns the indices of the non constant (informative) rows/features

    Parameters
    ----------
    x : sparse matrix
        data matrix
    axis : int
        axis to return indices for
    mask : sparse matrix [bool]
        mask of values to consider as nan
    as_bool : bool
        whether to return a mask of bool indices or vector of numbers
    threshold : numeric
        decided constant by the feature variance, can be larger than 0 for
        "almost-constant" features

    Returns
    -------
    cond : array_like
        Either an array with number of indices or boolean mask
    """
    if (threshold == 0) and (mask is None):
        return non_zero_index(x, axis, as_bool)
    elif method == 'variance':
        cond = variance(x, axis=axis, mask=mask) > threshold
    elif method == 'nnz':
        cond = x.getnnz(axis=axis) > threshold
    else:
        raise KeyError
    if as_bool:
        return cond
    else:
        return np.where(cond)[0]


def constant_index(x, axis, mask=None, as_bool=True, threshold=0):
    """
    Returns the indices of the constant rows/features

    Parameters
    ----------
    x : sparse matrix
        data matrix
    axis : int
        axis to return indices for
    mask : sparse matrix [bool]
        mask of values to consider as nan
    as_bool : bool
        whether to return a mask of bool indices or vector of numbers
    threshold : numeric
        decided constant by the feature variance, can be larger than 0 for
        "almost-constant" features

    Returns
    -------
    cond : array_like
        Either an array with number of indices or boolean mask
    """
    cond = variance(x, axis=axis, mask=mask) <= threshold
    if as_bool:
        return cond
    else:
        return np.where(cond)[0]
