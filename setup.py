"""Project setup"""

import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as req_file:
    install_requires = req_file.read().splitlines()

setuptools.setup(
    name='devops-toolset',
    version='1.0.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    url='https://github.com/aheadlabs/devops-toolset/',
    license='https://github.com/aheadlabs/devops-toolset/blob/master/LICENSE',
    author='Ivan Sainz | Alberto Carbonell',
    author_email='',
    description='General purpose DevOps-related scripts and tools.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9"
)
