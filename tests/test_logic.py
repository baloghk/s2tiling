import pytest

from s2tiling import S2TILING

TEST_LAT = 47.454442
TEST_LON = 18.585869
EXPECTED_TILES = ["33TYN", "34TCT"]


@pytest.fixture
def s():
    return S2TILING()


def test_attribute_list(s):
    result = s.getAllTiles(TEST_LAT, TEST_LON, attribute=["name", "description"])
    assert isinstance(result, list)
    assert len(result) > 0
    assert "name" in result[0]
    assert "description" in result[0]


def test_overlapping(s):
    tiles = s.getAllTiles(TEST_LAT, TEST_LON)
    assert EXPECTED_TILES[0] in tiles
    assert EXPECTED_TILES[1] in tiles


def test_first_last_tile(s):
    tiles = s.getAllTiles(TEST_LAT, TEST_LON)
    assert s.getFirstTile(TEST_LAT, TEST_LON) == tiles[0]
    assert s.getLastTile(TEST_LAT, TEST_LON) == tiles[-1]


def test_first_tile(s):
    tile = s.getFirstTile(TEST_LAT, TEST_LON)
    assert tile == EXPECTED_TILES[0]


def test_last_tile(s):
    tile = s.getLastTile(TEST_LAT, TEST_LON)
    assert tile == EXPECTED_TILES[1]


def test_invalid_attribute(s):
    with pytest.raises(ValueError):
        s.getAllTiles(TEST_LAT, TEST_LON, attribute="INVALID")
