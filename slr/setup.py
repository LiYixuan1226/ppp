from setuptools import setup

setup(
    name='Slirm',
    version='0.1',
    packages=['slirm'],
    package_dir={'': '.'},
    url='https://gitlab.com/twsswt/slirm',
    license='',
    author='Tim Storer',
    author_email='timothy.storer@glasgow.ac.uk',
    description='Systematic Literature RevIew Maker',
    setup_requires=['bibtexparser'],
    install_requires=['bibtexparser'],
    test_suite='nose.collector',
    tests_require=['nose']
)
