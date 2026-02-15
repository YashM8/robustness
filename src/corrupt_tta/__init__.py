import numpy as np
from numbers import Integral

from .corruptions import (
    gaussian_noise, shot_noise, impulse_noise, speckle_noise,
    gaussian_blur, glass_blur, defocus_blur, motion_blur, zoom_blur,
    fog, frost, snow, spatter,
    contrast, brightness, saturate, jpeg_compression, pixelate, elastic_transform
)

corruption_tuple = (
    gaussian_noise, shot_noise, impulse_noise, speckle_noise,
    gaussian_blur, glass_blur, defocus_blur, motion_blur, zoom_blur,
    fog, frost, snow, spatter,
    contrast, brightness, saturate, jpeg_compression, pixelate, elastic_transform
)

corruption_dict = {corr_func.__name__: corr_func for corr_func in corruption_tuple}

def corrupt(x, severity=1, corruption_name=None, corruption_number=-1):
    """
    Corrupts an image with a specified corruption and severity.
    
    :param x: image to corrupt; a numpy array in [0, 255]
    :param severity: strength with which to corrupt x; an integer in [1, 5]
    :param corruption_name: specifies which corruption function to call
    :param corruption_number: index of the corruption in corruption_tuple
    :return: corrupted image as a numpy array
    """
    try:
        x_arr = np.asarray(x)
    except Exception as exc:
        raise ValueError(f"x must be array-like, got {type(x).__name__}") from exc

    if x_arr.ndim != 3 or x_arr.shape[2] != 3:
        raise ValueError(f"x must have shape (H, W, 3), got {x_arr.shape}")
    if x_arr.shape[0] < 2 or x_arr.shape[1] < 2:
        raise ValueError(f"x must be at least 2x2 pixels, got {x_arr.shape[:2]}")

    if isinstance(severity, bool) or not isinstance(severity, Integral) or not (1 <= int(severity) <= 5):
        raise ValueError(f"severity must be an integer in [1, 5], got {severity!r}")
    severity = int(severity)

    if corruption_name is not None:
        if corruption_name not in corruption_dict:
            raise ValueError(
                f"Unknown corruption_name {corruption_name!r}. "
                f"Valid names: {sorted(corruption_dict.keys())}"
            )
        return corruption_dict[corruption_name](x_arr, severity)

    if corruption_number != -1:
        if isinstance(corruption_number, bool) or not isinstance(corruption_number, Integral):
            raise ValueError(f"corruption_number must be an integer, got {corruption_number!r}")
        corruption_number = int(corruption_number)
        if not (0 <= corruption_number < len(corruption_tuple)):
            raise ValueError(
                f"corruption_number must be in [0, {len(corruption_tuple) - 1}], "
                f"got {corruption_number}"
            )
        return corruption_tuple[corruption_number](x_arr, severity)

    raise ValueError("Either corruption_name or corruption_number must be specified.")

__version__ = "0.1.6"
