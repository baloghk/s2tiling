# s2tiling: Sentinel-2 Tile ID Lookup

This library resolves the overlapping issues found in the Sentinel tiling grid, which is based on MGRS but utilizes 110x110km tiles.

## Data Source & Attribution

This software utilizes data from the **Copernicus Sentinel-2 mission**, produced by the European Space Agency (ESA) and the Copernicus program.
* **Source:** [Sentinel-2 Tiling Grid (KML)](https://sentiwiki.copernicus.eu/web/s2-products)
* The use of the grid data is governed by the [Copernicus Sentinel Data Terms and Conditions](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).

## ChangeLog

### 0.1.0
* Initial release.
* Implemented coordinate to tile ID lookup functionality, properly handling areas with overlapping tiles.
* Supports retrieval of rich metadata, including raw KML descriptions and Shapely geometries (Polygon Z).
* Includes an optimized internal database based on the official ESA KML grid for offline use.

## Installation

You can install the package via pip:

```bash
pip install s2tiling
```

## Usage
The library accepts coordinates in **WGS84** (Decimal Degrees) format.

Note: On the very first run, the library will extract the grid database to your user cache directory (e.g., ~/.cache/s2tiling). This may take a few seconds. Subsequent runs will be instant.

```python 
import s2tiling

# Initialize the locator
s2t = s2tiling.S2TILING()

# Example coordinates (Felcsút, Hungary)
latitude = 47.454442
longitude = 18.585869

# 1. Get the first matching Tile ID
# Returns the first ID from the alphabetically sorted list of matches
first_tile_id = s2t.getFirstTile(latitude, longitude)
print(first_tile_id)
# Output: '33TYN'

# 2. Get the last matching Tile ID
# Returns the last ID from the alphabetically sorted list
last_tile_id = s2t.getLastTile(latitude, longitude)
print(last_tile_id)
# Output: '34TCT'

# 3. Get ALL matching Tile IDs as a list
all_tiles_id = s2t.getAllTiles(latitude, longitude)
print(all_tiles_id)
# Output: ['33TYN', '34TCT']

# 4. Get specific metadata ('Name', 'description', 'geometry')
# The default return value is the Tile ID ('Name'), but you can query 
# other attributes (e.g., 'geometry', 'description') or a list of them.
first_tile_geometry = s2t.getFirstTile(latitude, longitude, 'geometry')
print(first_tile_geometry)
# Output: GEOMETRYCOLLECTION Z (POLYGON Z ((17.6715394264 47.8226075595 0, 19.1352584753 47.7791570714 0, 19.059029865 46.7936706873 0, 17.6221956555 46.8356557267 0, 17.6715394264 47.8226075595 0)), POINT Z (18.3787270654 47.30813912339999 0))

all_tiles_data = s2t.getAllTiles(latitude, longitude, ['Name', 'geometry'])
print(all_tiles_data)
# [{'Name': '33TYN', 'geometry': <GEOMETRYCOLLECTION Z (POLYGON Z ((17.672 47.823 0, 19.135 47.779 0, 19.059 ...>}, {'Name': '34TCT', 'geometry': <GEOMETRYCOLLECTION Z (POLYGON Z ((18.328 47.823 0, 19.794 47.847 0, 19.817 ...>}]
```

## Features
**Offline**: Works entirely offline after installation (data is bundled).  
**Fast**: Uses geopandas and spatial indexing for quick lookups.  
**Simple**: No API keys or external services required.

## Requirements
Python 3.9 +  
geopandas  
shapely


## License
The source code of this library is licensed under the **MIT License**.

However, the **data** contained within (MGRS grid definitions) belongs to the Copernicus program. Please refer to the `NOTICE` file for full data attribution details.