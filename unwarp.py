"""
    "Discorpy is an open-source Python package for correcting radial distortion with sub-pixel accuracy."

    Bellow is the implementation of a visual inspection camera calibration.
"""
import os
import imutils
import numpy as np
import discorpy.losa.loadersaver as io
import discorpy.proc.processing as proc
import discorpy.post.postprocessing as post


def find_point_to_point(points, xcenter, ycenter, list_fact):
    """
    points : (row_index, column_index) of the point.
    """
    xi, yi = points[1] - xcenter, points[0] - ycenter
    ri = np.sqrt(xi * xi + yi * yi)
    factor = np.float64(np.sum(list_fact * np.power(ri, np.arange(len(list_fact)))))
    xo = xcenter + factor * xi
    yo = ycenter + factor * yi
    return xo, yo


def unwarp(img, list_power, list_coef):
    height, width, _ = img.shape
    xcenter = int(width/4)
    ycenter = int(height/4)

    # Get a good estimation of the forward model
    list_ffact = list_coef * list_power
    # Transform to the backward model for correction
    ref_points = [[i - ycenter, j - xcenter] for i in range(0, img.shape[0], 50) for j in
                range(0, img.shape[1], 50)]
    list_bfact = proc.transform_coef_backward_and_forward(list_ffact, ref_points=ref_points)
    """
    # Find top-left point in the undistorted space given top-left point in the distorted space.
    xu_top_left, yu_top_left = find_point_to_point((0, 0), xcenter, ycenter, list_ffact)
    # Find bottom-right point in the undistorted space given bottom-right point in the distorted space.
    xu_bot_right, yu_bot_right = find_point_to_point((height - 1, width - 1), xcenter, ycenter,
                                                     list_ffact)

    # Calculate padding width for each side.
    pad_top = int(np.abs(yu_top_left))
    pad_bot = int(yu_bot_right - height)
    pad_left = int(np.abs(xu_top_left))
    pad_right = int(xu_bot_right - width)

    img_pad = np.pad(img, ((pad_top, pad_bot), (pad_left, pad_right), (0, 0)), mode="constant")

    xcenter += pad_left
    ycenter += pad_top
    """
    img_corrected = []
    for i in range(img.shape[-1]):
        img_corrected.append(post.unwarp_image_backward(img[:, :, i], xcenter,
                                                        ycenter, list_bfact, mode='constant'))
    img_corrected = np.moveaxis(np.asarray(img_corrected), 0, 2)

    frame = imutils.resize(img_corrected, width=width, height=height)

    return frame


def execute(file_path, zero, first, second, third, fourth, click):
    img = io.load_image(file_path, average=False)

    list_power = np.asarray([1.0, 10**(-4), 10**(-7), 10**(-10), 10**(-13)])
    list_coef = np.asarray([zero, first, second, third, fourth])

    file_name = os.path.abspath('./runs/image' + str(click) + '.jpg')
    io.save_image(file_name, unwarp(img, list_power, list_coef),
                  overwrite=True)

    return file_name
