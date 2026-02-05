from setuptools import setup, find_packages

setup(
    name="elrs_simulator",
    version="0.1",
    # find_packages(where="src") looks for folder with z __init__.py inside src/
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
    ],
    author="Slawek Telega",
    description="ExpressLRS physical layer simulation",
)