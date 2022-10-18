from setuptools import setup, find_packages

setup(
    name = 'snake-py',
    author = 'Simon Takita',
    version = '0.1',
    package_dir = {'': 'src'},
    packages = find_packages(
        where='',
        include=['snake']
    ),
    install_requires = [
        'docopt',
    ],
    entry_points = {
        'console_scripts': [
            'snake-py = main:main',
        ]
    }
)