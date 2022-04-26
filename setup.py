from setuptools import find_packages, setup

setup(
    name='camelot_communicator',
    packages=find_packages(),
    version='0.1.0',
    description='My first Python library',
    author='Giulio Mori',
    license='MIT',
    install_requires=[''],
    setup_requires=['requests', 'EV_PDDL', 'singleton-decorator', 'PySimpleGUI'],
    tests_require=['unittest'],
    test_suite='test_camelot_communicator',
    include_package_data=True,
    zip_safe=True,
)