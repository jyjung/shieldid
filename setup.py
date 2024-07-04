from setuptools import setup, find_packages

setup(
    name="shieldid",
    version="0.1.0",
    author="Jung JinYoung",
    author_email="bungker@gmail.com",
    description="utilities package for SHIELD ID",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyjung/shieldid",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)