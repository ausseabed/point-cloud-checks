"""
Collection of utils used by test cases
"""

import laspy
import numpy as np
import random
import pyproj

from pathlib import Path


class LasTestFileBuilder():
    """
    Build a simple las file that randomly generates points to satisfy
    a 2d point density array.
    """

    def __init__(
        self,
        densities: list[list[int]],
        top_left_x: float,
        top_left_y: float,
        resolution: float,
        crs: pyproj.CRS,
        output_file: Path
    ) -> None:
        self.densities = densities
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.resolution = resolution
        self.crs = crs
        self.output_file = output_file

    def run(self):
        x_coordinates:list[float] = []
        y_coordinates:list[float] = []
        z_coordinates:list[float] = []

        x = self.top_left_x
        y = self.top_left_y
        for row in self.densities:
            # loop through all the rows of the grid
            for col in row:
                # loop through all the columns of the grid
                # each col value is the density count - the number
                # of points we're going to generate in this cell
                for pt_count in range(0, col):
                    x_max = x + self.resolution
                    y_min = y - self.resolution
                    # currently the height information isn't particularly relevant
                    # so just use a dummy value 
                    pt_z = 2.3
                    pt_x = random.uniform(x, x_max)
                    pt_y = random.uniform(y_min, y)

                    x_coordinates.append(pt_x)
                    y_coordinates.append(pt_y)
                    z_coordinates.append(pt_z)

                x += self.resolution

            x = self.top_left_x
            y -= self.resolution

        x_np = np.array(x_coordinates, dtype=np.int32)
        y_np = np.array(y_coordinates, dtype=np.int32)
        z_np = np.array(z_coordinates, dtype=np.int32)

        header = laspy.header.LasHeader()
        header.add_crs(self.crs)
        header.x_scale = 1.0
        header.y_scale = 1.0
        header.z_scale = 1.0

        las = laspy.create()
        las.header = header
        las.X = x_np
        las.Y = y_np
        las.Z = z_np
        las.update_header()
        las.write(str(self.output_file))

