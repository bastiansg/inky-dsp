from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requires = f.read().splitlines()

setup(
    name="inkywhat_dsp",
    packages=find_packages(),
    version="1.0.0",
    install_requires=requires,
    package_data={"": ["*.yml", "*.yaml"]},
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
