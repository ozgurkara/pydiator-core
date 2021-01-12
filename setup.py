import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydiator-core",
    version="1.0.9",
    author="Özgür Kara",
    author_email="ozgurkara85@gmail.com",
    description="Pydiator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ozgurkara/pydiator-core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
