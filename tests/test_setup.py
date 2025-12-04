import os

import pytest

from s2tiling import S2TILING


@pytest.fixture
def s():
    return S2TILING()


def test_import():
    assert S2TILING is not None


def test_cache_creation(s):
    assert os.path.exists(s.kml_path)


def test_tiles_loaded(s):
    assert len(s.tiles) > 0
