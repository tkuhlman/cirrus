import os
from setuptools import find_packages, setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Cirrus",
    version = "0.10",
    author = "Tim Kuhlman",
    author_email = "tim@backgroundprocess.com",
    description = ("A set of tools for configuring Amazon route53"),
    license = "BSD",
    keywords = "cloud boto route53",
    include_package_data = True,
    url = "https://launchpad.net/cirrus",
    packages=find_packages(),
    scripts=['bin/dns_setup.py', 'bin/update_host.py'],
    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires = ['boto>=2.0', 'PyYAML>=3.09', 'dnspython'],
)

