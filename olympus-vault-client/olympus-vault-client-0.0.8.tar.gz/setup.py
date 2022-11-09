from setuptools import setup

setup(
	author='olympus',
	description='vault client package for Databricks and Chimera',
	install_requires=[
		'hvac'
	],
	name='olympus-vault-client',
	packages=[
		'auth_methods',
		'olympus_vault_client'
	],
	url='https://gitlab.myteksi.net/olympus/olympus-vault-client',
	version='0.0.8'
)