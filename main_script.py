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

import config

if __name__ == "__main__":
    hdul, data, header = info_fits(config.file_fits) #from function info_fits
    F, arcsec_per_pixel = conversion_factor(header)
    converted_data, updated_header = conversion_data(hdul, data, header, F)
    creating_new_file_fits(converted_data, updated_header, config.new_file_fits)
    verify_conversion(config.file_fits, config.new_file_fits, config.verification_fits, updated_header)
    hdul.close()
    ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values = reading_table(config.file_path, config.value_clump)
    units_type(config.file_path, config.value_clump, config.column_name)
    pixel_coordinates, x_values, y_values  = conversion_RA_DEG_pixel(ra_values, dec_values, header)
    coordinates_table(pixel_coordinates, region_radius_values)
    fluxes, discrepancies, pixels_count, region_radius_values_pixel = integral_flux(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values)
    file_create_region(x_values, y_values, region_radius_values_pixel, config.file_regionsds9)
    compare_integral_flux(F_INT_values, fluxes, discrepancies)
    background, fluxes_background, discrepancies_backgoround = find_background(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values, fluxes, pixels_count)
    compare_integral_flux_background(F_INT_values, fluxes_background, discrepancies_backgoround)
    plot_spectrum(config.ker_plot, config.c, config.cube_fits, x_values, y_values, region_radius_values_pixel, config.plot_file, config.data_freqs_file, config.data_velocities_file, config.data_freqs_pixel_file, config.data_velocities_pixel_file, position=None)
    momentumn(config.cube_fits, config.freq_min, config.freq_max, config.c, config.nu_rest, config.moment0_fits, config.moment1_fits, config.sliced_cube_fits)
