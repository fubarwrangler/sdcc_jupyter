#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Minimal Python VERSION sanity check (from IPython/Jupyterhub)
# -----------------------------------------------------------------------------

from __future__ import print_function

import sys

from setuptools import setup, find_packages

VERSION = '0.2.0'

install_requires = []
with open('requirements.txt') as f:
    for line in f.readlines():
        req = line.strip()
        if not req or req.startswith(('-e', '#')):
            continue
        install_requires.append(req)


def main():
    setup(
        name             = 'sdccjupyter',
        packages         = find_packages(),
        package_data     = {'sdccjupyter': ['conf/*.cfg', 'cron/*', 'static/*.html']},
        version          = VERSION,
        description      = """SDCC Jupyter Spawners""",
        long_description = "",
        author           = "William Strecker-Kellogg",
        author_email     = "willsk@bnl.gov",
        url              = "https://www.sdcc.bnl.gov",
        license          = "BSD",
        install_requires = install_requires,
        platforms        = "Linux, Mac OS X",
        keywords         = ['Interactive', 'Shell', 'Web', 'Jupyter'],
        classifiers      = [
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
        ],
    )

if __name__ == '__main__':
    main()
