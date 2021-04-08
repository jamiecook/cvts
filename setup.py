from setuptools import setup

setup(
    name='cvts',
    description='Tools for working with commercial vehicles GPS traces in Vietnam',
    author='Simon Knapp',
    author_email='simon.knapp@csiro.au',
    version='0.0.2',
    python_requires='>=3',
    packages=['cvts'],
    scripts=['bin/json2geojson', 'bin/csv2json', 'bin/processtraces'])
