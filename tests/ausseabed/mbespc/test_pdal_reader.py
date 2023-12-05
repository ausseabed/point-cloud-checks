from pathlib import Path
import pytest

from ausseabed.mbespc.lib import pdal_reader


class TestPdalDriver:
    """Testing specific driver instances"""

    las = Path("data.las")
    laz = Path("data.laz")
    tiledb = Path("data.tiledb")
    tdb = Path("data.tdb")
    unknown = Path("data.unknown")

    def test_las(self):
        """Test to detect a LAS (.las) file and load the appropriate driver."""
        drv = pdal_reader.PdalDriver.from_uri(self.las)
        assert isinstance(drv, pdal_reader.DriverLas)

    def test_laz(self):
        """Test to detect a LAZ (.laz) file and load the appropriate driver."""
        drv = pdal_reader.PdalDriver.from_uri(self.laz)
        assert isinstance(drv, pdal_reader.DriverLas)

    def test_tiledb(self):
        """Test to detect a TileDB (.tiledb) array and load the appropriate driver."""
        drv = pdal_reader.PdalDriver.from_uri(self.tiledb)
        assert isinstance(drv, pdal_reader.DriverTileDB)

    def test_tdb(self):
        """Test to detect a TileDB (.tdb) array and load the appropriate driver."""
        drv = pdal_reader.PdalDriver.from_uri(self.tdb)
        assert isinstance(drv, pdal_reader.DriverTileDB)

    def test_driver_not_found(self):
        """Test that a DriverError is raised for an unknown data type."""
        with pytest.raises(pdal_reader.DriverError) as excinfo:
            _ = pdal_reader.PdalDriver.from_uri(self.unknown)

        assert str(excinfo.value) == "Could not determine driver for data.unknown"


@pytest.mark.parametrize(
    "uri, expected",
    [
        (Path("data.las"), '{"type": "readers.las", "filename": "data.las"}'),
        (Path("data.laz"), '{"type": "readers.las", "filename": "data.laz"}'),
        (Path("data.tiledb"), '{"type": "readers.tiledb", "strict": false, "array_name": "data.tiledb"}'),
        (Path("data.tdb"), '{"type": "readers.tiledb", "strict": false, "array_name": "data.tdb"}'),
    ],
)
def test_to_json(uri, expected):
    """Test that the json dump is as expected."""
    drv = pdal_reader.PdalDriver.from_uri(uri)
    assert drv.to_json() == expected
