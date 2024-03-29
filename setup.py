#   -*- coding: utf-8 -*-
#
#   This file is part of allocator-cli
#
#   Copyright (C) 2020 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
from setuptools import find_packages, setup


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    f = open(path, "r")
    return f.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Couldn't parse version from file.")


extras_require = {
    'linter': [
        "flake8==3.8.3",
        "isort>=4.2.15,<4.3.22",
    ],
    'dev': [
        "PyInstaller==5.5",
        "pytest==5.4.2",
        "twine==3.2.0",
        "mock==4.0.2",
        "boto3==1.13.7",
        "pytest-cov==2.10.1",
        "codecov==2.1.7"
    ],
    'hw-wallet': [
        "ledgerblue==0.1.31"
    ]
}

extras_require['dev'] = (
    extras_require['linter'] + extras_require['dev'] + extras_require['hw-wallet']
)


setup(
    name='skale-allocator-cli',
    # *IMPORTANT*: Don't manually change the version here.
    # Use the 'bumpversion' utility instead.
    version=find_version("cli", "__init__.py"),
    include_package_data=True,
    description='SKALE Allocator CLI',
    long_description_markdown_filename='README.md',
    author='SKALE Labs',
    author_email='support@skalelabs.com',
    url='https://github.com/skalenetwork/allocator-cli',
    install_requires=[
        "click==7.1.2",
        "skale.py==5.8dev0",
        "terminaltables==3.1.0",
        "yaspin==0.16.0",
        "texttable==1.6.2",
        "terminaltables==3.1.0"
    ],
    python_requires='>=3.7,<4',
    extras_require=extras_require,

    keywords=['skale', 'cli'],
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
)
