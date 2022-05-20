from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[
        'bin/finufft-benchmark'
    ],
    include_package_data = True,
    install_requires=[
        'click',
        'pyyaml',
        'kachery-cloud>=0.1.13',
        'figurl>=0.2.3'
    ]
)
