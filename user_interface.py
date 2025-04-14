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
    plot_spectrum
)

from cube_pb_fits import divide_cube_by_pb
from contextlib import redirect_stdout

import config
import os
import subprocess

def analisys():
    print("\nWhich analysis do you want to run:")
    print("[1] Continuous")
    print("[2] Cube")
    print("[3] Conitnuos and cube")
    print("[4] Script cube pb correction")
    print("[5] Reading a table column")    
    print("[0] Exit")
    return input("Select: ")

def main():
    decision = analisys()

    if decision == "1":
        print(f"\nConitnuous analysis running...")

        ans = input(f"\nDefault CLUMP value is {config.value_clump}, do you want to keep it?[y/n] ")
        if ans.lower() == "n":
            value_clump = input("Enter new CLUMP value: ")
            print(f"New CLUMP value set to {value_clump}")
        else:
            value_clump = config.value_clump
            print(f"Using defaul CLUMP value: {config.value_clump}")

        hdul, data, header = info_fits(config.file_fits) #from function info_fits
        F, arcsec_per_pixel = conversion_factor(header)
        converted_data, updated_header = conversion_data(hdul, data, header, F)
        creating_new_file_fits(converted_data, updated_header, config.new_file_fits)
        verify_conversion(config.file_fits, config.new_file_fits, config.verification_fits, updated_header)
        hdul.close()
        ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values = reading_table(config.file_path, value_clump)
        pixel_coordinates, x_values, y_values  = conversion_RA_DEG_pixel(ra_values, dec_values, header)
        coordinates_table(pixel_coordinates, region_radius_values)
        fluxes, discrepancies, pixels_count, region_radius_values_pixel = integral_flux(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values)
        file_create_region(x_values, y_values, region_radius_values_pixel, config.file_regionsds9)
        compare_integral_flux(F_INT_values, fluxes, discrepancies)
        background, fluxes_background, discrepancies_backgoround = find_background(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values, fluxes, pixels_count)
        compare_integral_flux_background(F_INT_values, fluxes_background, discrepancies_backgoround)
        
    elif decision == "2":
        print("\nCube analysis running...")

        ans1 = input(f"\nDefault CLUMP value is {config.value_clump}, do you want to keep it?[y/n] ")
        if ans1.lower() == "n":
            value_clump = input("Enter new CLUMP value: ")
        else:
            value_clump = config.value_clump
            print(f"Using defaul CLUMP value: {config.value_clump}")

        ans2 = input(f"\nDefault KER plot is {config.ker_plot}, do you want to keep it?[y/n] ")
        if ans2.lower() == "n":
            ker_plot = input("Enter new KER plot: ")
        else:
            ker_plot = config.ker_plot
            print(f"Using defaul KER plot: {config.ker_plot}")
        
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull):
                hdul, data, header = info_fits(config.file_fits)
                F, arcsec_per_pixel = conversion_factor(header)
                ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values = reading_table(config.file_path, value_clump)
                pixel_coordinates, x_values, y_values  = conversion_RA_DEG_pixel(ra_values, dec_values, header)
                fluxes, discrepancies, pixels_count, region_radius_values_pixel = integral_flux(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values)
        
            plot_spectrum(ker_plot, config.c, config.cube_fits, x_values, y_values, region_radius_values_pixel, config.plot_file, config.data_freqs_file, config.data_velocities_file, config.data_freqs_pixel_file, config.data_velocities_pixel_file, position=None)

    elif decision == "3":
        print("\nRunning main_script.py using default CLUMP value: {config.value_clump} and default KER plot:{config.ker_plot}.")
        subprocess.run(["python3", "main_script.py"])

    elif decision == "4":
        divide_cube_by_pb(config.cube_fits, config.pb_fits, config.cube_pb_fits)

    elif decision == "5":      
        column_name = input("\nName of the column you want to analysis: ")
        units_type(config.file_path, value_clump, column_name)

    elif decision == "0":
        print("Exit from the programme")

    else: 
        print("Not valid answrer, try again.")


if __name__ == "__main__":
    main()
