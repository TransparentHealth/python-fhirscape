import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-fhirscape',
    version='0.0.1',
    packages=['fhirscapet', ],
    include_package_data=True,
    license='MIT',  
    description='Tools for working FHIR data especially EOB.',
    long_description=README,
    url='https://github.com/TransparentHealth/python-fhirscape',
    author='Alan Viars',
    author_email='sales@videntity.com',
    install_requires=[
        'requests',  ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
