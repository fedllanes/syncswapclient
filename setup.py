from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SyncSwapClient',
    version='0.0.1',
    packages=['syncswap', 'syncswap.tokens'],
    url='',
    license='MIT',
    author='fedllanes',
    author_email='',
    description='An easy way to interact with the SyncSwap smart contract',
    install_requires=requirements
)
