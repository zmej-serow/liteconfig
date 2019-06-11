import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="liteconfig",
    version="0.1.2",
    author="Zmej Serow",
    author_email="zmej.serow@gmail.com",
    description="Lightweight and configurable .ini config parser with dot notation property access.",
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
