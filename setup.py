import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="networkbill-EIGENMODE",
    version="0.0.1",
    author="Eric Sheppard",
    author_email="eric@eigenmo.de",
    description="Parse and Verify Network Bill Files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/esheppa/networkbill-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dateutil',
    ],
    python_requires='>=3.8',
)
