import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liteconfig",
    version="0.0.1",
    author="Zmej Serow",
    author_email="zmej.serow@gmail.com",
    description="Easy, fast and lightweight config parser with dot notation property access.",
    keywords='configparser ini parsing conf cfg configuration file',
    platforms=['any'],
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zmej-serow/liteconfig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)