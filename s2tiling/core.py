import importlib.resources
import os
import zipfile

import geopandas as gpd
from shapely.geometry import Point

# -----------------------------------------------------------------------------
# NOTE: This module uses Sentinel-2 tiling grid data.
# The MGRS grid definition is based on Copernicus Sentinel data [2025].
# Attribution: European Space Agency (ESA) - Copernicus Program.
# -----------------------------------------------------------------------------


class S2TILING:
    """
    Manages the Sentinel-2 Level-1C MGRS tiling grid lookup operations.

    This class handles the extraction, caching, and spatial querying of the
    official Sentinel-2 grid definition (KML). It automatically manages
    a local cache of the KML data to ensure fast subsequent access.

    The grid is based on the Military Grid Reference System (MGRS). However, since
    Sentinel tiles are 110x110km and create overlaps within the grid, this library
    offers a solution to this problem.

    Attributes:
        CACHE_DIR (str): Path to the user's local cache directory (~/.cache/s2tiling).
        VALID_ATTRIBUTES (list): List of column names that can be queried
                                 (e.g., 'name', 'description', 'geometry').
    """

    CACHE_DIR = os.path.expanduser("~/.cache/s2tiling")
    VALID_ATTRIBUTES = ["name", "description", "geometry"]

    def __init__(self):
        """
        Initializes the S2TILING locator.

        Checks if the KML grid data exists in the local cache. If not, it extracts
        it from the bundled ZIP file. Then, it loads the data into a GeoDataFrame.

        Note:
            The first initialization might take a few seconds due to file extraction
            and parsing. Subsequent runs will be faster.
        """
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        self.kml_path = os.path.join(self.CACHE_DIR, "s2_tiling.kml")

        if not os.path.exists(self.kml_path):
            self._extract_kml()

        # Only keeping the 'Features' layer and relevant columns to save memory
        self.tiles = gpd.read_file(self.kml_path, driver="KML", layer="Features")

        self.tiles.columns = self.tiles.columns.str.lower()

    def _extract_kml(self):
        """
        Internal method to extract the KML file from the bundled package resource.
        It handles nested directory structures within the ZIP file dynamically.
        """
        with importlib.resources.path("s2tiling.data", "s2_tiling.zip") as p:
            with zipfile.ZipFile(p, "r") as z:
                all_files = z.namelist()
                # Find the .kml file regardless of folder structure
                kml_files = [f for f in all_files if f.lower().endswith(".kml")]

                if not kml_files:
                    raise FileNotFoundError(
                        f"The zip file doesnt contain a .kml file. Content: {all_files}"
                    )

                source_filename = kml_files[0]

                # Extract content directly to target path (flattening structure)
                with (
                    z.open(source_filename) as source,
                    open(self.kml_path, "wb") as target,
                ):
                    target.write(source.read())

    def getAllTiles(self, lat, lon, attribute="name"):
        """
        Retrieves all Sentinel-2 tiles covering the given coordinates.

        Args:
            lat (float): Latitude in decimal degrees (WGS84).
            lon (float): Longitude in decimal degrees (WGS84).
            attribute (str or list, optional): The column(s) to return.
                Defaults to 'name' (the Tile ID).
                Options: 'name', 'description', 'geometry'.

        Returns:
            list:
                - If attribute is a string (e.g., 'name'):
                    A list of values (['33TYN', '34TCT']).
                  Sorted alphabetically (unless attribute is 'geometry').
                - If attribute is a list:
                    A list of dictionaries ([{'name': '...', 'description': '...'}]).

        Raises:
            ValueError: If an invalid attribute name is requested.
        """
        point = Point(lon, lat)
        matches = self.tiles[self.tiles.contains(point)]

        # Attributes validation
        if isinstance(attribute, str):
            if attribute not in self.VALID_ATTRIBUTES:
                raise ValueError(
                    f"Invalid attribute '{attribute}'."
                    f" Must be one of {self.VALID_ATTRIBUTES}."
                )
        elif isinstance(attribute, list):
            invalid = [a for a in attribute if a not in self.VALID_ATTRIBUTES]
            if invalid:
                raise ValueError(
                    f"Invalid attributes {invalid}. "
                    f"Must be subset of {self.VALID_ATTRIBUTES}."
                )
        else:
            raise ValueError("attribute must be a string or a list of strings")

        if isinstance(attribute, str):
            values = matches[attribute].tolist()

            # Geometry objects cannot be sorted
            if attribute == "geometry":
                return values

            try:
                return sorted(values)
            except TypeError:
                return values  # Return unsorted if types are mixed or not comparable
        else:
            return matches.sort_values("name")[attribute].to_dict(orient="records")

    def getFirstTile(self, lat, lon, attribute="name"):
        """
        Returns the first matching tile (alphabetically by name).
        Useful for consistent selection in overlapping areas.
        """
        tiles = self.getAllTiles(lat, lon, attribute)
        return tiles[0] if tiles else None

    def getLastTile(self, lat, lon, attribute="name"):
        """
        Returns the last matching tile (alphabetically by name).
        Useful for consistent selection in overlapping areas.
        """
        tiles = self.getAllTiles(lat, lon, attribute)
        return tiles[-1] if tiles else None
