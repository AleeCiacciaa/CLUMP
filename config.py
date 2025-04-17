#Enter your path
file_fits = 'combined-cont-fits/almagal/124103_cont_7MTM2_jointdeconv.image.pbcor.fits'
new_file_fits = 'combined-cont-fits/new_file.fits'
verification_fits = 'combined-cont-fits/verification.fits'
file_path = 'cat_7MTM2_ipac.txt'
file_regionsds9 = 'combined-cont-fits/file_regionsds9.reg'

#spw0 default
cube_fits_spw0 = 'combined-line-fits/almagal/124103_spw0_7MTM2_jointdeconv.image.fits'
cube_fits_spw1 = 'combined-line-fits/almagal/124103_spw1_7MTM2_jointdeconv.image.fits'
cube_fits = cube_fits_spw0 

pb_fits = 'combined-cont-fits/almagal/124103_cont_7MTM2_jointdeconv.pb.fits'
cube_pb_fits_spw0 = '/combined-line-fits/almagal/124103_spw0_7MTM2_jointdeconv.image.pbcor.fits'
cube_pb_fits_spw1 = 'combined-line-fits/almagal/124103_spw1_7MTM2_jointdeconv.image.pbcor.fits'
cube_pb_fits = cube_pb_fits_spw0

plot_file_spw0 = 'combined-line-fits/plotting/spw0/plot_image_spw0.jpg'
data_freqs_file_spw0 ='combined-line-fits/plotting/spw0/data_freqs_spw0.txt'
data_velocities_file_spw0 ='combined-line-fits/plotting/spw0/data_velocities_spw0.txt'
data_freqs_pixel_file_spw0 ='combined-line-fits/plotting/spw0/data_freqs_pixel_spw0.txt'
data_velocities_pixel_file_spw0 ='combined-line-fits/plotting/spw0/data_velocities_pixel_spw0.txt'

plot_file_spw1 = 'combined-line-fits/plotting/spw1/plot_image_spw1.jpg'
data_freqs_file_spw1 ='combined-line-fits/plotting/spw1/data_freqs_spw1.txt'
data_velocities_file_spw1 ='combined-line-fits/plotting/spw1/data_velocities_spw1.txt'
data_freqs_pixel_file_spw1 ='combined-line-fits/plotting/spw1/data_freqs_pixel_spw1.txt'
data_velocities_pixel_file_spw1 ='combined-line-fits/plotting/spw1/data_velocities_pixel_spw1.txt'

plot_file = plot_file_spw0
data_freqs_file = data_freqs_file_spw0
data_velocities_file = data_velocities_file_spw0
data_freqs_pixel_file = data_freqs_pixel_file_spw0

sliced_cube_H2CO_fits ='combined-line-fits/momentumn/sliced_H2CO_cube.fits'
moment0_H2CO_fits = 'combined-line-fits/momentumn/mom0_H2CO.fits'
moment1_H2CO_fits = 'combined-line-fits/momentumn/mom1_H2CO.fits'
moment2_H2CO_fits = 'combined-line-fits/momentumn/mom2_H2CO.fits'

sliced_cube_SiO_fits ='combined-line-fits/momentumn/sliced_SiO_cube.fits'
moment0_SiO_fits = 'combined-line-fits/momentumn/mom0_SiO.fits'
moment1_SiO_fits = 'combined-line-fits/momentumn/mom1_SiO.fits'
moment2_SiO_fits = 'combined-line-fits/momentumn/mom2_SiO.fits'

sliced_cube_CH3CN_fits ='combined-line-fits/momentumn/sliced_CH3CN_cube.fits'
moment0_CH3CN_fits = 'combined-line-fits/momentumn/mom0_CH3CN.fits'
moment1_CH3CN_fits = 'combined-line-fits/momentumn/mom1_CH3CN.fits'
moment2_CH3CN_fits = 'combined-line-fits/momentumn/mom2_CH3CN.fits'

#H2CO default
sliced_cube_fits = sliced_cube_H2CO_fits
moment0_fits = moment0_H2CO_fits
moment1_fits = moment1_H2CO_fits
moment2_fits = moment2_H2CO_fits

value_clump = '124103'  #for tryng another clump with 5 kers insert value_clump = '100309'
column_name = 'RA'      #change this name according to the column whose type and units you want to know about
ker_plot = 4            #default
c = 3e8                 #m/s     
freq_min = 218.15       #GHz (H2CO) value changes depending on the molecule
freq_max = 218.16       #GHz (H2CO)
nu_rest = 218.222192    #GHz (H2CO)
