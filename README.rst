========================================
``spartans`` - SPARse Tools for ANalysiS
========================================

.. image:: img/spartans.svg
        :width: 100
        :alt: logo

.. image:: https://img.shields.io/pypi/v/spartans.svg
        :target: https://pypi.python.org/pypi/``spartans``


.. image:: https://readthedocs.org/projects/spartans/badge/?version=latest
        :target: https://spartans.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


When working with sparse matrices, it is desired to have a way to work with them as
if they were a regular ``numpy.array``\s. Yet, many popular methods for arrays don't exist for
sparse matrices. ``spartans`` wishes to help, with many operations to work with

Full example notebook_

* Free software: GNU General Public License v3
* Documentation: https://spartans.readthedocs.io.


Features
--------
Mathematical Operations
    Rich set of operations not supported on sparse matrices like ``variance``, ``cov``
    (covariance matrix) and ``corrcoef`` (correlation matrix).

Easy Indexing
    Convenient methods to index for "extra" sparse features by variance or by quantity.

Masking
    Many algorithms consider the zeros in a sparse matrix as missing data. Or considering missing
    data as zeros. Depending on the use-case. ``spartans``

FeatureMatrix
    FeatureMatrix is a ``spartan``\'s first-class citizen. It is a wrapper around ``scipy.sparse.csr``
    Matrix built with data analysis and data-science in mind.

Examples
--------

Full example notebook_

.. code-block:: python

    >>> import spartans as st
    >>> from scipy.sparse import csr_matrix
    >>> import numpy as np
    >>> m = np.array([[1, -2, 0, 50],
                      [0, 0, 0, 100],
                      [1, 0, 0, 80],
                      [1, 4, 0, 0],f
                      [0, 0, 0, 0],
                      [0, 4, 0, 0],
                      [0, 0, 0, -50]])
    >>> c = csr_matrix(m)

We can get the the correlation matrix of m using numpy.

.. code-block:: python

   >>> np.corrcoef(m, rowvar=False)

.. code-block:: shell

    Out[]: array([[ 1.  , -0.08,   nan,  0.31],
                  [-0.08,  1.  ,   nan, -0.35],
                  [  nan,   nan,   nan,   nan],
                  [ 0.31, -0.35,   nan,  1.  ]])

This won't work with the sparse matrix ``c``

.. code-block:: python

   >>> np.corrcoef(c, rowvar=False)

.. code-block:: shell

    AttributeError: 'float' object has no attribute 'shape'

But with ``spartans`` this can be done.

.. code-block:: python

   >>> st.corr(c)

.. code-block:: shell

    Out[]: array([[ 1.  , -0.08,   nan,  0.31],
                  [-0.08,  1.  ,   nan, -0.35],
                  [  nan,   nan,   nan,   nan],
                  [ 0.31, -0.35,   nan,  1.  ]])

The column and row with ``nan`` is because the original matrix has a columns (feature) which is
zero for the entire column. ``spartans`` can handle that using ``st.non_zero_index(c, axis=0, as_bool=False)``
which will return ``array([0, 1, 3])``.
A lot more functionality is in the notebook_.

Credits
-------
* This open-source project is backed by SentinelOne_
* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _SentinelOne: https://www.sentinelone.com/blog/
.. _notebook: https://github.com/Sentinel-One/spartans/blob/master/examples/Usage.ipynb
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
