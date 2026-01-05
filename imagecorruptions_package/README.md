# Image Corruptions (ImageNet-C)

This package provides a collection of image corruptions used in the [ImageNet-C benchmark](https://github.com/hendrycks/robustness). It allows you to easily apply these corruptions to your own images to test model robustness.

## Installation

You can install this package from PyPI (once published) or directly from source.

```bash
pip install imagecorruptions
```

To include support for `motion_blur` and `snow`, you must install `wand` (Python ImageMagick bindings) and the ImageMagick system library.

```bash
pip install imagecorruptions[wand]
# And install ImageMagick on your system (e.g., sudo apt-get install imagemagick)
```

## Usage

### Applying Corruptions by Name

```python
import numpy as np
from imagecorruptions import corrupt, get_corruption_names

# Load your image as a numpy array (H, W, C) with values 0-255
image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

# Get list of common corruptions
for corruption in get_corruption_names('common'):
    for severity in range(1, 6):
        corrupted = corrupt(image, corruption_name=corruption, severity=severity)
        # corrupted is a numpy array
        print(f"Applied {corruption} with severity {severity}")
```

### Applying Corruptions by Number

```python
from imagecorruptions import corrupt

# Loop through the first 15 (common) corruptions
for i in range(15):
    for severity in range(1, 6):
        corrupted = corrupt(image, corruption_number=i, severity=severity)
        print(f"Applied corruption #{i} with severity {severity}")
```

## Available Corruptions

**Common (ImageNet-C):**
1. Gaussian Noise
2. Shot Noise
3. Impulse Noise
4. Defocus Blur
5. Glass Blur
6. Motion Blur (requires `wand`)
7. Zoom Blur
8. Snow (requires `wand`)
9. Frost
10. Fog
11. Brightness
12. Contrast
13. Elastic Transform
14. Pixelate
15. JPEG Compression

**Validation:**
16. Speckle Noise
17. Gaussian Blur
18. Spatter
19. Saturate

## Dependencies
- numpy
- scikit-image
- scipy
- opencv-python-headless (or opencv-python)
- Pillow
- Wand (optional, for motion blur and snow)
