# -*- coding: utf-8 -*-

import setuptools

from inventree_zapier.version import ZapierPluginVersion

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-zapier",

    version=ZapierPluginVersion,

    author="Matthias Mair",

    author_email="code@mjmair.com",

    description="Zapier plugin for InvenTree",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree inventree-plugin zapier inventory",

    url="https://github.com/matmair/inventree-zapier",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.6",

    entry_points={
        "inventree_plugins": [
            "ZapierPlugin = inventree_zapier.zapier_plugin:ZapierPlugin"
        ]
    },
)
