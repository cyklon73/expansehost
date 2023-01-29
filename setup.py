from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="expansehost",
    version="1.0.1",
    description="A Python API Wrapper for the expansehost API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyklon73/expansehost",
    author="Cyklon73",
    author_email="cyklon698@gmail.com",
    license="MIT",
    packages=["expansehost"],
)
