# coding=utf-8
"""
Setup for gym-acnportal.
"""
# TODO: Once open-ai-prototyping is merged in and a new acnportal is
#  released, we can just put acnportal in requirements.
import setuptools

with open("README.md") as fh:
    long_description = fh.read()
setuptools.setup(
    name="gym-acnportal",
    version="0.0.1",
    author="Sunash Sharma",
    author_email="sbsharma@caltech.edu",
    url="https://github.com/sunash/gym-acnportal",
    description="Utilities for RL with the ACN Research Portal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={"": ["LICENSE.txt", "THANKS.txt"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "acnportal @ git+https://github.com/zach401/acnportal" "@dev#egg=acnportal",
        "gym>=0.15.4",
    ],
)
