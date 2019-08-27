import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfconfig",
    version="0.1.2",
    author="Virgile Jarry",
    author_email="virgilejarry@mailbox.org",
    description="A python library to manage your network interfaces under linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acceis/pyfconfig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "pyroute2"
    ]
)
