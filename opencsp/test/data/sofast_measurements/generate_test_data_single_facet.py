"""Generates test data from measurement file for mirror type 'single_facet'.
Multiple combinations of display and surface types are iterated over.
"""
import os
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np

from opencsp.common.lib.deflectometry.Display import Display
from opencsp.common.lib.deflectometry.FacetData import FacetData
from opencsp.app.sofast.lib.ImageCalibrationScaling import ImageCalibrationScaling
from opencsp.app.sofast.lib.Measurement import Measurement
from opencsp.app.sofast.lib.Sofast import Sofast
from opencsp.common.lib.camera.Camera import Camera


def generate_dataset(
    file_measurement: str,
    file_camera: str,
    file_display: str,
    file_calibration: str,
    file_facet: str,
    surface_type: Literal['parabolic', 'plano'],
    robust_ls: bool,
    file_dataset_out: str,
):
    """Generates and saves dataset"""
    # Load components
    camera = Camera.load_from_hdf(file_camera)
    display = Display.load_from_hdf(file_display)
    measurement = Measurement.load_from_hdf(file_measurement)
    calibration = ImageCalibrationScaling.load_from_hdf(file_calibration)
    facet_data = FacetData.load_from_json(file_facet)

    # Calibrate fringes
    measurement.calibrate_fringe_images(calibration)

    # Creates sofast object
    S = Sofast(measurement, camera, display)

    # Update mask calculation options
    S.params.mask_keep_largest_area = True

    # Define surface data
    if surface_type == 'parabolic':
        surface_data = dict(
            surface_type=surface_type,
            initial_focal_lengths_xy=(100.0, 100.0),
            robust_least_squares=robust_ls,
            downsample=10,
        )
    elif surface_type == 'plano':
        surface_data = dict(
            surface_type=surface_type, robust_least_squares=robust_ls, downsample=10
        )

    # Process optic data
    S.process_optic_singlefacet(facet_data, surface_data)

    # Check output file exists
    if not os.path.exists(os.path.dirname(file_dataset_out)):
        os.mkdir(os.path.dirname(file_dataset_out))

    # Save testing data
    S.save_data_to_hdf(file_dataset_out)
    display.save_to_hdf(file_dataset_out)
    camera.save_to_hdf(file_dataset_out)
    calibration.save_to_hdf(file_dataset_out)
    print(f'All data saved to: {file_dataset_out:s}')

    # Show slope map
    mask = S.data_image_processing_facet[0]['mask_processed']
    slopes_xy = S.data_characterization_facet[0]['slopes_facet_xy']
    slopes = np.sqrt(np.sum(slopes_xy**2, 0))
    image = np.zeros(mask.shape) * np.nan
    image[mask] = slopes

    plt.imshow(image, cmap='jet')
    plt.title('Slope Magnitude')

    plt.show()


if __name__ == '__main__':
    # Generate measurement set 1 data
    base_dir = os.path.join(os.path.dirname(__file__), 'data')

    # Nominal
    generate_dataset(
        file_measurement=os.path.join(base_dir, 'measurement_facet.h5'),
        file_camera=os.path.join(base_dir, 'camera.h5'),
        file_display=os.path.join(base_dir, 'display_distorted_2d.h5'),
        file_calibration=os.path.join(base_dir, 'calibration.h5'),
        file_facet=os.path.join(base_dir, 'Facet_NSTTF.json'),
        surface_type='parabolic',
        robust_ls=True,
        file_dataset_out=os.path.join(base_dir, 'calculations_facet/data.h5'),
    )

    # Rectangular display
    generate_dataset(
        file_measurement=os.path.join(base_dir, 'measurement_facet.h5'),
        file_camera=os.path.join(base_dir, 'camera.h5'),
        file_display=os.path.join(base_dir, 'display_rectangular.h5'),
        file_calibration=os.path.join(base_dir, 'calibration.h5'),
        file_facet=os.path.join(base_dir, 'Facet_NSTTF.json'),
        surface_type='parabolic',
        robust_ls=True,
        file_dataset_out=os.path.join(
            base_dir, 'calculations_facet/data_rectangular.h5'
        ),
    )

    # 3D distorted display
    generate_dataset(
        file_measurement=os.path.join(base_dir, 'measurement_facet.h5'),
        file_camera=os.path.join(base_dir, 'camera.h5'),
        file_display=os.path.join(base_dir, 'display_distorted_3d.h5'),
        file_calibration=os.path.join(base_dir, 'calibration.h5'),
        file_facet=os.path.join(base_dir, 'Facet_NSTTF.json'),
        surface_type='parabolic',
        robust_ls=True,
        file_dataset_out=os.path.join(
            base_dir, 'calculations_facet/data_distorted_3d.h5'
        ),
    )

    # No robust least squares
    generate_dataset(
        file_measurement=os.path.join(base_dir, 'measurement_facet.h5'),
        file_camera=os.path.join(base_dir, 'camera.h5'),
        file_display=os.path.join(base_dir, 'display_distorted_2d.h5'),
        file_calibration=os.path.join(base_dir, 'calibration.h5'),
        file_facet=os.path.join(base_dir, 'Facet_NSTTF.json'),
        surface_type='parabolic',
        robust_ls=False,
        file_dataset_out=os.path.join(base_dir, 'calculations_facet/data_no_ls.h5'),
    )

    # Plano optic
    generate_dataset(
        file_measurement=os.path.join(base_dir, 'measurement_facet.h5'),
        file_camera=os.path.join(base_dir, 'camera.h5'),
        file_display=os.path.join(base_dir, 'display_distorted_2d.h5'),
        file_calibration=os.path.join(base_dir, 'calibration.h5'),
        file_facet=os.path.join(base_dir, 'Facet_NSTTF.json'),
        surface_type='plano',
        robust_ls=True,
        file_dataset_out=os.path.join(base_dir, 'calculations_facet/data_plano.h5'),
    )
