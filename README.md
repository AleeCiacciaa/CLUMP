# Analysis of CLUMP and KER Data - Python Interface
This project contains a set of Python scripts developed to analyse observational data related to the study of clumps and kerfs. The programme makes it possible to calculate emission moments, filter data according to frequency intervals, select regions of interest and produce visual and numerical output.

## ALMAGAL
The ALMAGAL project is a survey conducted with the ALMA radio telescope to observe star-forming regions. The observations were carried out with various antenna configurations, each with a different spatial resolution. As can be read in the papers in the 'reference paper' folder, the configurations vary depending on the type of data to be obtained:

- 7m: data taken with the ACA (Atacama Compact Array). It is a set of 7-metre diameter antennas. It has low resolution but high sensitivity to extended structures (large, diffuse).

- TM2: data with short baseline configurations of ALMA's 12-m array. Lower resolution than long configurations, but better than 7m. Used in C-2 configuration for near sources, C-3 for far sources.
  
- TM1: data with long baseline configurations of the 12-m array. Have the highest spatial resolution. Used in C-5 configuration for near sources, C-6 for far sources.

The data used in this project involves joint deconvolution, which allows data from different configurations to be combined to obtain more accurate images. Specifically, 7m and TM2 were combined in a product called 7m+tm2 and balances the sensitivity of the extended structures of 7m with the good resolution of TM2 for studying clumps formation.

## File types used
The programme works mainly with FITS files and is divided into two main parts, namely continuous and cube analysis.

A continuous file ('combined-cont-fits') represents the background emission deprived of spectral lines, in fact it is a two-dimensional map (RA, Dec) of the continuous and global emission of a certain source at certain frequencies.

A spectroscopic data cube ('combined-line-fits') is a three-dimensional structure (RA, Dec, Frequency) representing the emission of an astronomical source along the line of sight. Due to the decrease in sensitivity along the edges of the field of view caused by the measuring instruments themselves, such as radio telescopes or interferometers, a correction must be made. The Primary Beam (PB) correction allows the cube data to be normalised to reflect the true intensity of the observed sources over the entire field of view, including the edges. In order to make this correction, a continuum file is used which contains the continuous emission component and thus allows for the correct calibration with the primary beam.

## Uploaded files

## Scripts
- **main_script.py**: main script in which the study of clump 124103 and the brightest ker inside it (ker number 4 for the numbering carried out) is performed by default. Instead, the astrochemical chemistry part is studied the H2CO molecule.
- **config.py**: script containing all the constants and files used.
- **def_stro.py**: script with all the functions used in the study of the continuum and the cube, with a few additional contour functions for readability.
- **cube_pb_fits.py**: script that allows PB correction of cube using a continuous file. It has been separated from the other scripts because it is much slower to run, as the data dubs are very heavy (~ 2'350'000 KB).
- **user_interface**: script used to simplify the readability of the programme by dividing it into sections according to the type of analysis desired:
    - [1] Continuous: continuous analysis of the clump of interest and study of its kers,  
      identifying the regions that identify their position, specifically using SAOImage ds9.  
      Finally, the integrated flow was studied and compared with the theoretical references  
      in the table `cat_7MTM2_ipac.txt`.
    - [2] Cube: analysing the cube of the clump of interest and studying its brightest ker  
      representing the spectrum of a certain spectral wind (0.1). From this representation,  
      it was possible to proceed with the study of the peaks to identify the chemistry of  
      the source using MADCUBA.
    - [3] Continuous and cube: both previous.
    - [4] Script cube pb correction: to run the `cube_pb_fits.py` script separately.
    - [5] Reading table: to be able to read the columns in the table for a certain clump,  
      specifying the unit and data type of a certain column, as it is not easy to read by  
      opening the document. This is the only part of the programme that can be done by  
      entering a clump value other than the default one (for example try `100309`).
    - [6] Calculation of momentum 0, 1, 2: analysis concerning astrochemistry with the  
      study of three molecules present in the brighter ker, already studied in the cube part.  
      Specifically, the molecules studied through MADCUBA are H₂CO, SiO and CH₃CN.
  
