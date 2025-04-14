from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.io import ascii
from astropy.table import Table
from tabulate import tabulate
from astropy.wcs import FITSFixedWarning

import astropy.units as u
import os
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import pyregion
import warnings

#For plotting
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

warnings.simplefilter('ignore', FITSFixedWarning)

#Funzion for inital info of file.fits 
def info_fits(file_fits):

    hdul = fits.open(file_fits)
    print("\nInitial info:")
    hdul.info()
    
    #Read data and header
    data = hdul[0].data
    header = hdul[0].header

    return hdul, data, header

#Function for conversation factor B/P
def conversion_factor(header):
    #Value of beam and pixel
    BMAJ = abs(header.get('BMAJ', None)) #higer beam
    BMIN = abs(header.get('BMIN', None)) #lower beam
    mean_values_beam = np.sqrt(BMAJ * BMIN) #geometric mean 
    CDELT = abs(header.get('CDELT1', None)) #pixel

    arcsec_per_pixel = CDELT * 3600
    
    #print("\nBMAJ:", BMAJ)
    #print("BMIN:", BMIN)
    print("Mean values beam:", mean_values_beam)
    print("CDELT pixel:", CDELT, end="\n\n")

    #Ares
    A_beam = (mean_values_beam**2) * math.pi   
    A_pixel = CDELT ** 2
    F = A_beam / A_pixel

    print ("Area beam:", A_beam)
    print("Area pixel:", A_pixel)
    print ("Conversion factor (B/P): ", F, end="\n\n")

    return F, arcsec_per_pixel

#Function for conversion and sostitution
def conversion_data(hdul, data, header, F):
    converted_data = data / F
    hdul[0].data = converted_data
    hdul[0].header['BUNIT'] = 'Jy/pixel'
    updated_header = header 
    print("\nConversion info:")
    hdul.info()

    return converted_data, updated_header

#Function for creating new file
def creating_new_file_fits(converted_data, updated_header, new_file_fits):

    hdu = fits.PrimaryHDU(data=converted_data, header=updated_header)
    hdu.writeto(new_file_fits, overwrite=True)

    print(f"New file .fits saved: {new_file_fits}")

#Function for verfity conversion
def verify_conversion(file_fits, new_file_fits, verification_fits, header):

    hdul1 = fits.open(file_fits)
    hdul2 = fits.open(new_file_fits)

    data1 = hdul1[0].data
    data2 = hdul2[0].data

    F_data_ratio = data1 / data2

    hdu_ratio = fits.PrimaryHDU(data=F_data_ratio, header=header)
    hdul_ratio = fits.HDUList([hdu_ratio])
    hdul_ratio.writeto(verification_fits, overwrite=True)

    hdul1.close()
    hdul2.close()
    hdul_ratio.close()

#Funtion for reading table
def reading_table(file_path, value_clump):
    if not os.path.exists(file_path):
        print(f"Error: file {file_path} non existing.")
        return

    try:
        data = ascii.read(file_path)
        header = data.colnames  

        clump_data = data['CLUMP'].data.astype(str)  
        clump_data = np.char.strip(clump_data)
        filter_line = data[clump_data == value_clump]


        if len(filter_line) > 0:
            print(f"\nLines with CLUMP {value_clump}:")
            print(filter_line)

            ra_values = filter_line['RA'].data
            dec_values = filter_line['DEC'].data
            FWHM_circ_values = filter_line['FWHM_circ'].data
            F_INT_values = filter_line['F_INT'].data

            region_radius_values = [x / 2 for x in FWHM_circ_values]
 
            #print(f"\nRA values:", ra_values)
            #print(f"\nDEC values:", dec_values)
            print(f"\nFWHM Full width at halt Maximum circolar values:", FWHM_circ_values)
            print(f"\nF INT Integral flux:", F_INT_values)
            #print(f"\nRegion radius values:", region_radius_values)
            return ra_values, dec_values, FWHM_circ_values, region_radius_values, F_INT_values
            
        else:
            print(f"\nNo lines with CLUMP {value_clump}.")

    except Exception as e:
        print(f"Error during reading tabel: {e}")

#Function for reading units and type a specific column
def units_type(file_path, value_clump, column_name):

    print(f"\nInformation on '{column_name}' column:")
    try:
        data = Table.read(file_path, format='ascii.ipac')
    except Exception as e:
        print(f"Error during file lecture: {e}")
        return

    header = data.colnames

    if column_name in data.colnames:
        col = data[column_name]

        print(f"'{column_name}' column type: {col.dtype}")

        if hasattr(col, 'unit') and col.unit is not None:
            print(f"'{column_name}' column units : {col.unit}")
        else:
            print(f"'{column_name}' column units not specified.")
    else:
        print(f"'{column_name}' column not existing, see the column header: ")
        print(header)

#Function for conversion RA-DEC in pixel
def conversion_RA_DEG_pixel(ra_values, dec_values, header):
    pixel_coordinates = []

    try: 
        wcs = WCS(header)
        sky_coord = SkyCoord(ra=ra_values, dec=dec_values, unit=(u.deg, u.deg)) #Creating an object SkyCoord
        x_values, y_values = wcs.world_to_pixel(sky_coord) #Conversion coordinates of world (RA-DEC) in pixel

        for i in range(len(x_values)):            
            pixel_coordinates.append((float(x_values[i]),float(y_values[i])))

        #print("\nPixel coordinates:", pixel_coordinates)
        #print("\nX values:", x_values)
        #print("\nY values:", y_values)
        return pixel_coordinates, x_values, y_values

    except Exception as e:
        print(f"Error during WSC: {e}")
        return None

#Function to view parameters for ds9 (user inferface)
def coordinates_table(pixel_coordinates, region_radius_values):
    table = [(i + 1, pixel_coordinates[i], region_radius_values[i]) for i in range(len(pixel_coordinates))]
    df = pd.DataFrame(table, columns=["Number of KER", "Pixel coordinates", "Region radio (arcsec)"])    
    print()
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False, stralign="center"))

#Function for integral flux
def integral_flux(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values):
    region_radius_values_pixel = [r / arcsec_per_pixel for r in region_radius_values]

    fluxes = []
    discrepancies = []
    pixels_count = []

    for i in range(len(x_values)):
        x0 = int(round(x_values[i]))
        y0 = int(round(y_values[i]))
        r = int(round(region_radius_values_pixel[i]))
        flux = 0.0
        pixel_count = 0

        for x in range(max(0, x0 - r), min(data.shape[1], x0 + r + 1)): #boundaries condition
            for y in range(max(0, y0 - r), min(data.shape[0], y0 + r + 1)):
                
                if (x - x0) ** 2 + (y - y0) ** 2 <= r ** 2:
                    flux += data[y][x] 
                    pixel_count += 1

        fluxes.append(flux)
        pixels_count.append(pixel_count)

        F_INT_value = F_INT_values[i]
        discrepacy = flux / F_INT_value
        
        discrepancies.append(discrepacy)
    
    #print("Calculated fluxes:", [float(f) for f in fluxes])
    return fluxes, discrepancies, pixels_count, region_radius_values_pixel


#Funtion for creating region for ds9
def file_create_region(x_values, y_values, region_radius_values_pixel, file_regionsds9):
    regions_text = """
# Region file format: DS9 version 4.1
# Filename: test01.fits
global color=green dashlist=8 3 width=1 font="helvetica 10 normal" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1
image
"""
    regions = []

    for i in range(len(x_values)):
        x = x_values[i]
        y = y_values[i]
        radius = region_radius_values_pixel[i]

        region = pyregion.Shape("circle", [x, y, radius])
        regions.append(region)
        regions_text += f"circle({x},{y},{radius})\n"

    with open(file_regionsds9, 'w') as file:
        file.write(regions_text)
    
    print(f"\nNew file for regions for ds9 has been saved in'{file_regionsds9}'.")
    return regions

#Function to compare integral flux (user inferface)
def compare_integral_flux(F_INT_values, fluxes, discrepancies):
    table = [(F_INT_values[i], fluxes[i], discrepancies[i]) for i in range(len(fluxes))]
    df = pd.DataFrame(table, columns=["Theoretical integral fluxes", "Calculated integral fluxes", "Discrepancy"])    
    print()
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False, stralign="center"))

#Funcion for background
def find_background(x_values, y_values, region_radius_values, arcsec_per_pixel, data, F_INT_values, fluxes, pixels_count):
    old_fluxes = fluxes
    old_pixels_count = pixels_count
    fluxes, discrepancies, pixels_count, region_radius_values_pixel = integral_flux(x_values, y_values, [2 * r for r in region_radius_values], arcsec_per_pixel, data, F_INT_values)
    new_fluxes = fluxes
    new_pixels_count =  pixels_count
    #print(old_pixels_count)
    #print(old_fluxes)
    #print(new_pixels_count)
    #print(new_fluxes)

    pixel_differences = []
    for i in range(len(old_pixels_count)):
        difference = new_pixels_count[i] - old_pixels_count[i]
        pixel_differences.append(difference)
    
    fluxes_differences = []
    for i in range(len(old_fluxes)):
        difference = new_fluxes[i] - old_fluxes[i]
        fluxes_differences.append(difference)
    #print(pixel_differences)
    #print(fluxes_differences)

    background = []
    for i in range(len(pixel_differences)):
        mean = (1 / pixel_differences[i]) * fluxes_differences[i]

        background.append(mean)
    #print(background)

    fluxes_background = []
    for i in range(len(old_fluxes)):
        difference = old_fluxes[i] - (background[i] * old_pixels_count[i])
        fluxes_background.append(difference)
    #print (fluxes_background)

    discrepancies_backgoround = []
    for i in range(len(discrepancies)):
        discrepacy = fluxes_background[i] / F_INT_values[i]
        discrepancies_backgoround.append(discrepacy)
    #print(discrepancies_backgoround)

    return background, fluxes_background, discrepancies_backgoround

#Function to compare integral flux background (user inferface)
def compare_integral_flux_background(F_INT_values, fluxes_background, discrepancies_backgoround):
    table = [(F_INT_values[i], fluxes_background[i], discrepancies_backgoround[i]) for i in range(len(fluxes_background))]
    df = pd.DataFrame(table, columns=["Theoretical integral fluxes", "Calculated integral fluxes with background", "Discrepancy"])    
    print()
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False, stralign="center"))

#Function for plotting spctrum
def plot_spectrum(ker_plot, c, cube_fits, x_values, y_values, region_radius_values_pixel, plot_file, data_freqs_file, data_velocities_file, data_freqs_pixel_file, data_velocities_pixel_file, position=None):
    x_value = x_values[ker_plot]
    y_value = y_values[ker_plot]
    r_value = region_radius_values_pixel[ker_plot]

    with fits.open(cube_fits) as hdul:
        cube_data = hdul[0].data
        cube_header = hdul[0].header

    ref_freq = cube_header['CRVAL3']    #Reference frequence (Hz)
    step_freq = cube_header['CDELT3']   #Step (Hz)
    ref_pixel = cube_header['CRPIX3']   #Reference pixels (=1.0)
    n_freq = cube_data.shape[0]         #Number of frequences in the cube
    bmaj = cube_header['BMAJ'] * 3600   #Beam major axis in arcsec
    bmin = cube_header['BMIN'] * 3600   #Beam minor axis in arcsec

    print(f"\nCRVAL3 values:", ref_freq)
    print(f"\nCDELT3 values:", step_freq)
    print(f"\nCRPIX3 values:", ref_pixel)

    center_freq = ref_freq + ((n_freq - 1)/2 - (ref_pixel - 1)) * step_freq
    nu_rest = center_freq

    freqs = ref_freq + (np.arange(n_freq) - (ref_pixel - 1)) * step_freq    #Hz
    freqs_GHz = freqs / 1e9                                                 #GHz
    velocities = ( c * (nu_rest - freqs) / nu_rest ) / 1e3                  #km/s
    nu_rest = np.mean(freqs)

    #Circolar mask
    y_indices, x_indices = np.indices(cube_data.shape[1:3])  
    distance_from_center = np.sqrt((x_indices - x_value)**2 + (y_indices - y_value)**2)
    mask = distance_from_center <= r_value

    region_data = cube_data[:, mask] 
    #print(f"Shape of region_data: {region_data.shape}")

    #Mean spectrum 
    spectrum_mean = np.mean(region_data, axis=1)                                 #Jy/beam    
    spectrum_mean_K = 1.222e3 * (spectrum_mean * 1e3) / (freqs_GHz**2 * bmaj * bmin) #K
   
    #Spectrum sum
    spectrum_sum = np.sum(region_data, axis=1)                                       #Jy/beam
    spectrum_sum_K = 1.222e3 * (spectrum_sum * 1e3) / (freqs_GHz**2 * bmaj * bmin)   #K

    #Mean spectrum for each pixel
    spectrum_pixel = np.mean(region_data, axis=1)                               #Jy/beam
    spectrum_pixel_K = 1.222e3 * (spectrum_pixel * 1e3) / (freqs_GHz**2 * bmaj * bmin)   #K

    #More plotting (simultaneous)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    #Sx&Up: frecquecies - mean spectrum
    axes[0, 0].plot(freqs, spectrum_mean_K, color='blue')
    axes[0, 0].set_xlabel('Observed Frequency [Hz]')
    axes[0, 0].set_ylabel('Flux Density [K]')
    axes[0, 0].set_title(f'Spectrum in Frequency\n({x_value}, {y_value})')

    #Dx&Up: velocities - mean spectrum
    axes[0, 1].plot(velocities, spectrum_mean_K, color='red')
    axes[0, 1].set_xlabel('Observed Velocity [km/s]')
    axes[0, 1].set_ylabel('Flux Density [K]')
    axes[0, 1].set_title(f'Spectrum in Velocity\n({x_value}, {y_value})')

    #Sx&Down: frquencies - spectrum sum
    axes[1, 0].plot(freqs, spectrum_sum_K, color='orange')
    axes[1, 0].set_xlabel('Observed Frequency [Hz]')
    axes[1, 0].set_ylabel('Total Flux [K]')
    axes[1, 0].set_title(f'Total Integrated Spectrum\n({x_value}, {y_value})')
    
    #DX&Down: velocities - spectrum sum
    axes[1, 1].plot(velocities, spectrum_sum_K, color='green')
    axes[1, 1].set_xlabel('Observed Velocity [km/s]')
    axes[1, 1].set_ylabel('Total Flux [K]')
    axes[1, 1].set_title(f'Total Integrated Spectrum\n({x_value}, {y_value})')

    #Main plot, same of [0, 0] but bigger
    plt.tight_layout()
    plt.savefig(plot_file)

    np.savetxt(data_freqs_file, np.column_stack((freqs, spectrum_sum_K)), header="Frequency [Hz]    Flux Density [K]")
    np.savetxt(data_velocities_file, np.column_stack((velocities, spectrum_sum_K)), header="Velocity [km/s]    Flux Density [K]")
    np.savetxt(data_freqs_pixel_file, np.column_stack((freqs, spectrum_pixel_K)), header="Frequency [Hz]    Flux for pixel [K]")
    np.savetxt(data_velocities_pixel_file, np.column_stack((velocities, spectrum_pixel_K)), header="Velocity [km/s]    Flux for pixel [K]")
    plt.show()
    
    plt.figure(figsize=(8, 6))

    plt.plot(freqs_GHz, spectrum_mean_K, color='blue')
    plt.xlabel('Observed Frequency [GHz]')
    plt.ylabel('Flux Density [K]')
    plt.title(f'Spectrum in Frequency\n({x_value}, {y_value})')
    
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    data_text = """\
    UnitAngle : deg
    UnitSpectral : Hz
    UnitVelo : km/s
    UnitInten : K
    TempScale : TA*
    Beammaj : 0.0
    Beammin : 0.0
    BeamPA : 0.0
    """

    with open(data_freqs_file, 'w') as f:
        f.write(data_text + '\n') 
        np.savetxt(f, np.column_stack((freqs, spectrum_sum_K)), header="Frequency [Hz]    Flux Density [K]", comments='')

    with open(data_velocities_file, 'w') as f:
        f.write(data_text + '\n')
        np.savetxt(f, np.column_stack((velocities, spectrum_sum_K)), header="Velocity [km/s]    Flux Density [K]", comments='')

    with open(data_freqs_pixel_file, 'w') as f:
        f.write(data_text + '\n')
        np.savetxt(f, np.column_stack((freqs, spectrum_pixel_K)), header="Frequency [Hz]    Flux for pixel [K]", comments='')

    with open(data_velocities_pixel_file, 'w') as f:
        f.write(data_text + '\n')
        np.savetxt(f, np.column_stack((velocities, spectrum_pixel_K)), header="Velocity [km/s]    Flux for pixel [K]", comments='')

    print(f"\nPlot has been saved in: {plot_file}")
    print(f"\nData has been saved in: {data_freqs_file} & {data_velocities_file}")
    print(f"\nData for each pixel has been saved in: {data_freqs_pixel_file} & {data_velocities_pixel_file}")
