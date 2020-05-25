"""Project setup"""

from setuptools import setup

setup(
    name='devops-toolset',
    version='0.29.0',
    packages=['core', 'core.tests', 'i18n', 'i18n.tests', 'tools', 'tools.tests', 'devops', 'wordpress', 'filesystem',
              'filesystem.tests'],
    url='https://github.com/aheadlabs/devops-toolset/',
    license='https://github.com/aheadlabs/devops-toolset/blob/master/LICENSE',
    author='Iván Sainz | Alberto Carbonell',
    author_email='',
    description='General purpose DevOps-related scripts and tools.',
)
