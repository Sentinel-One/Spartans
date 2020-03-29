import joblib
from scipy import sparse
import numpy as np

from . import core


class FeatureMatrix:
    def __init__(self, sparse_matrix: sparse.csc_matrix, columns=None):
        assert sparse.issparse(sparse_matrix), f'{self.__class__.__name__} only supports Sparse matrices'
        self.sparse_matrix = sparse_matrix
        self.set_mask(None)
        self.cache = {}
        self.columns = columns or [f'f{i}' for i in range]
    def __getattr__(self, item):
        return getattr(self.sparse_matrix, item)

    def __repr__(self):
        return self.sparse_matrix.__repr__()

    def __str__(self):
        return self.sparse_matrix.__str__()

    def clear_cache(self, key=None, reset=False):
        if reset and (key is None):
            self.cache = {}
        self.cache.pop(key, None)

    @classmethod
    def load(cls, path, validate=True):
        mat = joblib.load(path)
        if validate:
            assert isinstance(mat, cls), 'File is not a FeatureMatrix'
        return mat

    def dump(self, path):
        joblib.dump(self, path)

    def set_mask(self, M):
        if M is None:
            self.mask = None
        else:
            assert M.shape == self.sparse_matrix.shape, "Mask must have same shape as matrix"
            self.mask = M

    def mean(self, axis=0, mask=True, safe=False, **kwargs):
        if mask:
            mask = self.mask
        else:
            mask = None
        return core.mean(self.sparse_matrix, axis=axis, mask=mask, safe=safe, **kwargs)

    def variance(self, axis=0, mask=True, **kwargs):
        return core.variance(self.sparse_matrix, axis=axis, mask=mask, **kwargs)

    def make_nan_mask(self):
        M = core.make_nan_mask(self)
        self.set_mask(M)

    def eliminate_nans(self):
        if self.mask is None:
            print('No Mask Found')
            return
        else:
            self.sparse_matrix[self.mask] = 0
            self.sparse_matrix.eliminate_zeros()

    def get_column_names(self):
        # This needs to change every time slicing happens
        pass

    def as_df(self):
        # Require pandas > 0.25
        pass


if __name__ == '__main__':
    m = np.array([[1, -2, 0, 50],
                  [0, 0, 0, 100],
                  [1, 0, 0, 80],
                  [1, 4, 0, 0],
                  [0, 0, 0, 0],
                  [0, 4, 0, 0],
                  [0, 0, 0, -50]])
    c = sparse.csc_matrix(m)
    y = np.array([1, 1, 0, 0, 1, 0, 1])
    M = FeatureMatrix(c)
    print(m.mean(axis=1))
    print(M.mean(axis=1))
