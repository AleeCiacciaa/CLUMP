from def_astro import (
    info_fits,
    conversion_factor,
    conversion_data,
    creating_new_file_fits,
    verify_conversion,
    reading_table,
    units_type,
    conversion_RA_DEG_pixel,
    coordinates_table,
    file_create_region,
    integral_flux,
    compare_integral_flux,
    find_background,
    compare_integral_flux_background,
    plot_spectrum,
    momentumn
)

from cube_pb_fits import divide_cube_by_pb
from contextlib import redirect_stdout

import config
import os
import subprocess
import matplotlib.pyplot as plt

def analisys():
    print("\nWhich analysis do you want to run:")
    print("[1] Continuous")
    print("[2] Cube")
    print("[3] Conitnuos and cube")
    print("[4] Script cube pb correction")
    print("[5] Reading a table column")
    print("[6] Calculation of momentumn 0,1,2")
    print("[0] Exit")
    return input("Select: ")

def main():
    decision = analisys()

    if decision == "1":
        print(f"\nContinuous analysis of CLUMP {config.value_clump} running.")
        hdul, data, header = info_fits(config.file_fits) 
        F, arcsec_per_pixel = conversion_factor(header)
        converted_data, updated_header = conversion_data(hdul, data, header, F)
        creating_new_file_fits(converted_data, updated_header, config.new_file_fits)
        verify_conversion(config.file_fits, config.new_file_fits, config.verification_fits, updated_header)
        hdul.close()
        ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values = reading_table(config.file_path, config.value_clump)
        pixel_coordinates, x_values, y_values  = conversion_RA_DEG_pixel(ra_values, dec_values, header)
        fluxes, discrepancies, pixels_count, region_radius_values_pixel = integral_flux(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values)
        file_create_region(x_values, y_values, region_radius_values_pixel, config.file_regionsds9)
        compare_integral_flux(F_INT_values, fluxes, discrepancies)
        background, fluxes_background, discrepancies_backgoround = find_background(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values, fluxes, pixels_count)
        compare_integral_flux_background(F_INT_values, fluxes_background, discrepancies_backgoround)
        
    elif decision == "2":
        print(f"\nCube analysis of CLUMP {config.value_clump} running.")
        ans1 = input(f"Default KER plot is {config.ker_plot}, do you want to keep it?[y/n] ")
        if ans1.lower() == "n":
            ker_plot = input("Enter new KER plot: ")
        else:
            ker_plot = config.ker_plot
            print(f"Using defaul KER plot: {config.ker_plot}")
        
        print("\nSelect spectral window:")
        print("[0] spw0")
        print("[1] spw1")
        ans2 = input("Select: ")
        if ans2 == "0":
            cube_fits = config.cube_fits_spw0
            plot_file = config.plot_file_spw0
            data_freqs_file = config.data_freqs_file_spw0
            data_velocities_file = config.data_velocities_file_spw0
            data_freqs_pixel_file = config.data_freqs_pixel_file_spw0
            data_velocities_pixel_file = config.data_velocities_pixel_file_spw0

        else:
            cube_fits = config.cube_fits_spw1
            plot_file = config.plot_file_spw1
            data_freqs_file = config.data_freqs_file_spw1
            data_velocities_file = config.data_velocities_file_spw1
            data_freqs_pixel_file = config.data_freqs_pixel_file_spw1
            data_velocities_pixel_file = config.data_velocities_pixel_file_spw1

        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull):
                hdul, data, header = info_fits(config.file_fits)
                F, arcsec_per_pixel = conversion_factor(header)
                ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values = reading_table(config.file_path, config.value_clump)
                pixel_coordinates, x_values, y_values  = conversion_RA_DEG_pixel(ra_values, dec_values, header)
                fluxes, discrepancies, pixels_count, region_radius_values_pixel = integral_flux(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values)
        
            plot_spectrum(ker_plot, config.c, cube_fits, x_values, y_values, region_radius_values_pixel, plot_file, data_freqs_file, data_velocities_file, data_freqs_pixel_file, data_velocities_pixel_file, position=None)

    elif decision == "3":
        print(f"\nRunning main_script.py using default CLUMP value {config.value_clump}, default KER plot {config.ker_plot} and default spectral wind 0.")
        subprocess.run(["python3", "main_script.py"])

    elif decision == "4":
        print("\nSelect spectral window:")
        print("[0] spw0")
        print("[1] spw1")
        ans = input("Select: ")

        if ans == "0":
            cube_fits = config.cube_fits_spw0
            cube_pb_fits = config.cube_pb_fits_spw0
        else:
            cube_fits = config.cube_fits_spw1
            cube_pb_fits = config.cube_pb_fits_spw1

        divide_cube_by_pb(cube_fits, config.pb_fits, cube_pb_fits)

    elif decision == "5":
        ans = input(f"\nDefault CLUMP value is {config.value_clump}, do you want to keep it?[y/n] ")
        if ans.lower() == "n":
            value_clump = input("Enter new CLUMP value: ")
        else:
            value_clump = config.value_clump
            print(f"Using defaul CLUMP value: {config.value_clump}")

        column_name = input("\nName of the column you want to analysis: ")
        ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values = reading_table(config.file_path, value_clump)
        units_type(config.file_path, value_clump, column_name)

    elif decision == "6":
        print("\nSelect molecule: ")
        print("[1] H2CO")
        print("[2] SiO")
        print("[3] CH3CN")
        dec0 = input("Select: ")

        if dec0 == "1":
            mol = "H2CO"
            nu_rest = 218.222192    #GHz
            freq_min = 218.15       #GHz
            freq_max = 218.16       #GHz
            cube_fits = config.cube_fits_spw0
            moment0_fits = config.moment0_H2CO_fits
            moment1_fits = config.moment1_H2CO_fits
            moment2_fits = config.moment2_H2CO_fits
            sliced_cube_fits = config.sliced_cube_H2CO_fits

        elif dec0 == "2":
            mol = "SiO"
            nu_rest = 217.10498     #GHz
            freq_min = 217.02       #GHz
            freq_max = 217.05       #GHz
            cube_fits = config.cube_fits_spw0
            moment0_fits = config.moment0_SiO_fits
            moment1_fits = config.moment1_SiO_fits
            moment2_fits = config.moment2_SiO_fits
            sliced_cube_fits = config.sliced_cube_SiO_fits

        elif dec0 == "3":
            mol = "CH3CN"
            nu_rest = 220.747261    #GHz
            freq_min = 220.67       #GHz
            freq_max = 220.68       #GHz
            cube_fits = config.cube_fits_spw1
            moment0_fits = config.moment0_CH3CN_fits
            moment1_fits = config.moment1_CH3CN_fits
            moment2_fits = config.moment2_CH3CN_fits
            sliced_cube_fits = config.sliced_cube_CH3CN_fits

        else:
            print("Not valid answrer, try again.")
     
        print(f"\nFrequency range for the brightest peak of the {mol} molecule: {freq_min} - {freq_max} GHz.")
        print(f"Nu rest for {mol} is set to {nu_rest} GHz.")
        print("It may take few seconds.")
        momentumn(cube_fits, freq_min, freq_max, config.c, nu_rest, moment0_fits, moment1_fits, moment2_fits, sliced_cube_fits)
        
    elif decision == "0":
        print("Exit from the programme")

    else: 
        print("Not valid answrer, try again.")

if __name__ == "__main__":
    main()
