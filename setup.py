from setuptools import setup

setup(
    name='cvts',
    version='0.0.1',
    description='Tools for working with commercial vehicles GPS traces in Vietnam',
    author='Simon Knapp',
    author_email='simon.knapp@csiro.au',
    packages=['cvts'],
    scripts=['bin/json2geojson', 'bin/csv2json', 'bin/processtraces'])
