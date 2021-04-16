from setuptools import setup

setup(
    name='cvts',
    description='Tools for working with commercial vehicles GPS traces in Vietnam',
    author='Simon Knapp',
    author_email='simon.knapp@csiro.au',
    version='0.0.2',
    python_requires='>=3',
    packages=['cvts'],
    scripts=[
        'bin/csv2json',
        'bin/json2geojson',
        'bin/processtraces',
        'bin/regiondensity'],
    install_requires=[
        'numpy',
        'nptyping',
        'scipy',
        'shapely',
        'tqdm',
        'dataclasses',
        'pyshp'])
