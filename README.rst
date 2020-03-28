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


* Free software: GNU General Public License v3
* Documentation: https://spartans.readthedocs.io.

Examples
--------

Full example notebook_



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



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _notebook: https://github.com/Sentinel-One/``spartans``/blob/master/examples/Usage.ipynb
