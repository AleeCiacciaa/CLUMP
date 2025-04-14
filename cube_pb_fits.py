#to be implemented
from def_astro import info_fits
from astropy.io import fits

import argparse
import config

def divide_cube_by_pb(cube_fits, pb_fits, cube_pb_fits):
    
    
    print("\nScript cube pb corrected running, it may take a few seconds...")

    with fits.open(cube_fits) as hdul_cube:
        cube_data = hdul_cube[0].data
        cube_header = hdul_cube[0].header

    with fits.open(pb_fits) as hdul_bp:
        bp_data = hdul_bp[0].data
        bp_header = hdul_bp[0].header


    if cube_data.ndim != 3:
        raise ValueError("Cube has to be 3D.")

    if bp_data.shape != cube_data.shape[1:]:
        raise ValueError("Conitnuous has to be 2D and of the same cube spatial dimension.")
    #print(bp_data.shape)
    #print(type(bp_data))

    normalized_cube = cube_data / bp_data

    hdu = fits.PrimaryHDU(data=normalized_cube, header=cube_header)
    hdu.writeto(cube_pb_fits, overwrite=True)

    print(f"\nNew file .fits pb corrected saved: {cube_pb_fits}")

    return normalized_cube, cube_data, cube_header, bp_data, bp_header

if __name__ == "__main__":
    divide_cube_by_pb(config.cube_fits, config.pb_fits, config.cube_pb_fits)
