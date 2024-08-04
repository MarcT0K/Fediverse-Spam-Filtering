from setuptools import setup, find_packages

setup(
    name="Fediverse Spam Filtering",
    version="0.1.0",
    description="Python microservice to perform spam filtering in the Fediverse",
    author="Marc 'TOK_' Damie",
    author_email="marc@damie.eu",
    packages=["fedispam"],
    install_requires=["socketify", "lmdb"],
    entry_points={
        "console_scripts": ["fedispam = fedispam.main:main"],
    },
)
