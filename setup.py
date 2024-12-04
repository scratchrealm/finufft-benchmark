from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[
        'bin/finufft-benchmark'
    ],
    include_package_data = True,
    install_requires=[
        'click',
        'pyyaml'
    ]
)
