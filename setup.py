from setuptools import setup, find_packages

setup(
    name='mls',
    scripts=['mlsphere/cli/mls.py'],
    package_dir={'mlsphere': 'mlsphere'},
    packages=find_packages(),
)
