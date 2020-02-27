#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy>=0.15', 'scipy>=1.0.0']

setup_requirements = ['pytest-runner',]

test_requirements = ['pytest>=3', ]

setup(
    author="Sentinel-One, Dean Langsam",
    author_email='deanla@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Sparse Tools for Analysis",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='spartans, sparse, matrix, features',
    name='spartans',
    packages=find_packages(include=['spartans', 'spartans.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Sentinel-One/spartans',
    version='0.1.0',
    zip_safe=False,
)
