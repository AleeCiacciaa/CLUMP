from def_astro import info_fits
from astropy.io import fits

import argparse
import config
import logging
import time
import numpy as np
import sys


def show_progress_bar(current, total, length=30):
    percent = int((current / total) * 100)
    bar = '#' * int((current / total) * length)
    sys.stdout.write(f'\rNormalizing: [{bar:<{length}}] {percent}%')
    sys.stdout.flush()

def divide_cube_by_pb(cube_fits, pb_fits, cube_pb_fits):
    
    print("\nScript cube pb corrected running, it may take few seconds.")

    start_time = time.time()

    t0 = time.time()
    with fits.open(cube_fits) as hdul_cube:
        cube_data = hdul_cube[0].data
        cube_header = hdul_cube[0].header
    t1 = time.time()
    print(f"Cube loaded in {t1 - t0:.2f} seconds.")

    t2 = time.time()
    with fits.open(pb_fits) as hdul_bp:
        bp_data = hdul_bp[0].data
        bp_header = hdul_bp[0].header
    t3 = time.time()
    print(f"PB map loaded in {t3 - t2:.2f} seconds.")

    if cube_data.ndim != 3:
        raise ValueError("Cube has to be 3D.")

    if bp_data.shape != cube_data.shape[1:]:
        raise ValueError("Conitnuous has to be 2D and of the same cube spatial dimension.")
    #print(bp_data.shape)
    #print(type(bp_data))

    t4 = time.time()
    normalized_cube = np.empty_like(cube_data)
    n_channels = cube_data.shape[0]
    for i in range(n_channels):
        normalized_cube[i] = cube_data[i] / bp_data
        show_progress_bar(i + 1, n_channels)
    t5 = time.time()
    print(f"\nNormalization completed in {t5 - t4:.2f} seconds.")

    t6 = time.time()
    hdu = fits.PrimaryHDU(data=normalized_cube, header=cube_header)
    hdu.writeto(cube_pb_fits, overwrite=True)
    t7 = time.time()
    print(f"New FITS file saved in {t7 - t6:.2f} seconds.")

    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds.")
    print(f"\nNew file .fits pb corrected saved: {cube_pb_fits}")

    return normalized_cube, cube_data, cube_header, bp_data, bp_header

if __name__ == "__main__":
    divide_cube_by_pb(config.cube_fits, config.pb_fits, config.cube_pb_fits)
