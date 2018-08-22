#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import os.path as fs


HERE = fs.abspath(fs.dirname(__file__))


def openfile(fname):
    with open(fs.join(HERE, fname)) as fp:
        return fp.read()


requirements = [ ]
setup_requirements = [ ]
test_requirements = ['pytest', ]

setup(
    name='tinypascal',
    version='0.1.dev0',
    url='https://github.com/hkmshb/tinypascal',
    author="Abdul-Hakeem Shaibu",
    author_email='hkmshb@gmail.com',
    description="A Pascal interpreter written in Python",
    long_description='\n\n'.join([
        openfile('README.md'),
        openfile('CHANGES.md')
    ]),
    keywords='tinypascal pascal interpreter',
    license="MIT license",
    include_package_data=True,
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
