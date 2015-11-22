from setuptools import setup, find_packages

setup(
    name='lab2',
    version='0.1',
    packages=find_packages(),
    test_suite='tests',
    entry_points={
        'console_scripts':
            [
                'external_sort = myitertools.external_sort:main',
                'filtered = myitertools.filtered:main',
                'myrange = myitertools.myrange:main'
            ]
        },
)
