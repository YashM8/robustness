from .corruptions import *
import numpy as np
from PIL import Image

# Define the supported corruptions
corruption_tuple = (gaussian_noise, shot_noise, impulse_noise, defocus_blur,
                    glass_blur, motion_blur, zoom_blur, snow, frost, fog,
                    brightness, contrast, elastic_transform, pixelate, jpeg_compression,
                    speckle_noise, gaussian_blur, spatter, saturate)

corruption_dict = {corr_func.__name__: corr_func for corr_func in corruption_tuple}

def get_corruption_names(subset='common'):
    """
    Returns a list of corruption names.
    :param subset: 'common' (first 15 used in ImageNet-C benchmark), 'validation' (extra 4), or 'all' (19).
    """
    # Common corruptions used in the benchmark
    common_list = [
        'gaussian_noise', 'shot_noise', 'impulse_noise',
        'defocus_blur', 'glass_blur', 'motion_blur', 'zoom_blur',
        'snow', 'frost', 'fog',
        'brightness', 'contrast', 'elastic_transform', 'pixelate', 'jpeg_compression'
    ]

    # Validation corruptions
    validation_list = ['speckle_noise', 'gaussian_blur', 'spatter', 'saturate']

    if subset == 'common':
        return common_list
    elif subset == 'validation':
        return validation_list
    elif subset == 'all':
        return common_list + validation_list
    else:
        raise ValueError("subset must be 'common', 'validation', or 'all'")

def corrupt(x, severity=1, corruption_name=None, corruption_number=-1):
    """
    :param x: image to corrupt; a 224x224x3 numpy array in [0, 255] or a PIL Image.
    :param severity: strength with which to corrupt x; an integer in [1, 5].
    :param corruption_name: specifies which corruption function to call.
    :param corruption_number: the position of the corruption_name in the list.
    :return: the corrupted image as a uint8 numpy array.
    """

    # Ensure x is a PIL Image for processing
    if isinstance(x, np.ndarray):
        x_pil = Image.fromarray(x.astype(np.uint8))
    elif isinstance(x, Image.Image):
        x_pil = x
    else:
        raise TypeError("Input x must be a numpy array or PIL Image")

    if corruption_name:
        if corruption_name not in corruption_dict:
            raise ValueError(f"Corruption '{corruption_name}' not found.")
        x_corrupted = corruption_dict[corruption_name](x_pil, severity)
    elif corruption_number != -1:
        names = get_corruption_names('all')
        if 0 <= corruption_number < len(names):
             # Map number to name based on the 'all' list order (which matches tuple order mostly)
             # Wait, corruption_tuple order in corruptions.py vs the list I defined might differ?
             # Let's rely on corruption_tuple index.
             if corruption_number >= len(corruption_tuple):
                  raise ValueError(f"Corruption number {corruption_number} out of range")
             x_corrupted = corruption_tuple[corruption_number](x_pil, severity)
        else:
             raise ValueError(f"Corruption number {corruption_number} out of range")
    else:
        raise ValueError("Either corruption_name or corruption_number must be passed")

    return np.uint8(x_corrupted)
