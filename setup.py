import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="librunner",
    version="0.0.1",
    author="Alex van Vliet",
    author_email="alex@vanvliet.pro",
    description="A package to run python models in parallel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-van-vliet/librunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
