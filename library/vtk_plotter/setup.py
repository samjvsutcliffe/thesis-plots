from setuptools import find_packages, setup

setup(
    name='mpmplotter',
    packages=find_packages(include=["mpmplotter"]),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'vtk'
    ],
    # package_dir={"": "src"},
    version='0.1.0',
    description='MPM plotting library',
    author='',
)
