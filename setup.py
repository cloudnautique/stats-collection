from setuptools import setup, find_packages

from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(req.req) for req in install_reqs]

setup(
    name='rldc',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='ASL 2.0',
    install_requires=reqs,
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'twitter_collector=rldc.collectors.twitter_collector:main',
        ]
    }
)
