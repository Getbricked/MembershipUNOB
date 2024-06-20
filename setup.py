from setuptools import setup, find_packages
import os

script_dir = os.path.dirname(__file__)
readme = os.path.join(script_dir, "Readme.md")

with open(readme, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="membershipUNOB",
    version="2.0.0",
    packages=find_packages(),
    package_data={
        "membershipUNOB.utils": ["*.json", "*.html"],
        "membershipUNOB.gql": ["*.gql"],
    },
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "requests",
        "selenium",
        "webdriver_manager",
        "fastapi",
        "aiohttp",
        "asyncpg",
        "aiodataloader",
        "sqlalchemy",
        "sqlalchemy_utils",
        "uvicorn",
        "gunicorn",
    ],
    author="Minh Quang Bui - Quang Tai Do",
    author_email="minhquang.bui@unob.cz",
    description="Membership management for UNOB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/getbricked/membershipunob",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
