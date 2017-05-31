import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='slowevents',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Copyright 2017',  # example license
    description='Custom made app for middleman transactions',
    long_description=README,
    url='https://www.slowevents.io/',
    author='Davide Pugliese',
    author_email='dvd.pugliese@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: Flask :: 0.12.2',
        'Intended Audience :: Developers',
        'License :: Copyright 2017',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
