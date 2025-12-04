from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="s2tiling",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "s2tiling": ["data/*.zip"],
    },
    install_requires=[
        "geopandas>=0.12.0",
        "shapely>=2.0.0",
    ],
    python_requires=">=3.9",
    description="Python library to get Sentinel-2 tiles data for given lat/lon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Balogh Károly",
    author_email="balogh2k4@gmail.com",
    url="https://github.com/balogh2k4/s2tiling",
    project_urls={
        "Bug Reports": "https://github.com/balogh2k4/s2tiling/issues",
        "Source": "https://github.com/balogh2k4/s2tiling",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="sentinel-2, satellite, mgrs, tiles, overlap, gis, geospatial",
)
