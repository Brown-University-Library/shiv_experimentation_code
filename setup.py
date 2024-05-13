from setuptools import setup

setup(
    name="count-hall-hoag-orgs",
    version="0.0.1",
    description="Uses public repository API to count all hall-hoag org-items.",
    py_modules=["count_orgs"],
    entry_points={
        "console_scripts": ["count_orgs=count_orgs:prep_org_count"],
    },
    install_requires=['requests==2.31.0'],
)
