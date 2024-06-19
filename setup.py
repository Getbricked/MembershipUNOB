# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="membershipUNOB",
    version="0.3",
    packages=find_packages(),
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
    author="Minh Quang Bui",
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
