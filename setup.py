# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in pni_report_dashboard/__init__.py
from pni_report_dashboard import __version__ as version

setup(
	name='pni_report_dashboard',
	version=version,
	description='PNI Dashboard',
	author='Jigar Tarpara',
	author_email='jigartarpara68@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
