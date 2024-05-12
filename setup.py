from setuptools import setup

setup(
    name="count-hall-hoag-orgs",
    version="0.0.1",
    description="Uses public repository API to count all hall-hoag org-items.",
    py_modules=["count_orgs"],
    entry_points={
        "console_scripts": ["count_orgs=count_orgs:main"],
    },
    install_requires=['requests==2.26.0'],
)
