from setuptools import find_packages, setup

setup(
    name='camelot_communicator',
    packages=find_packages(),
    version='0.1.0',
    description='My first Python library',
    author='Giulio Mori',
    license='MIT',
    install_requires=['pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)