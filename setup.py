from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()

long_description = read_file("README.md")
version = read_file("VERSION")
requirements = read_requirements("requirements.txt")

setup(
    name = 'PYzza',
    version = version,
    author = 'piledge',
    author_email = '',
    url = 'https://github.com/piledge/PYzza/',
    description = 'Small but useful collection of Python-Functions',
    long_description_content_type = "Small but useful collection of Python-Functions",
    long_description = long_description,
    license = "MIT license",
    packages = find_packages(exclude=["test"]),
    install_requires = requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
