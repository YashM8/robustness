import sys
import os
import numpy as np
from PIL import Image
import traceback

# Add the directory containing the package to python path
sys.path.append(os.path.abspath('ImageNet-C/imagenet_c'))

try:
    from imagenet_c import corruptions
    print("Successfully imported corruptions module.")
except Exception as e:
    print(f"Failed to import corruptions module: {e}")
    traceback.print_exc()
    sys.exit(1)

# Dummy image: 224x224 RGB
img_np = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
img_pil = Image.fromarray(img_np)

corruption_list = [
    'gaussian_noise', 'shot_noise', 'impulse_noise', 'speckle_noise',
    'gaussian_blur', 'glass_blur', 'defocus_blur', 'motion_blur', 'zoom_blur',
    'fog', 'frost', 'snow', 'spatter',
    'contrast', 'brightness', 'saturate', 'jpeg_compression', 'pixelate',
    'elastic_transform'
]

# Note: fgsm requires a model, so we skip it for this basic test.

passed = 0
skipped = 0
failed = 0

print("\nRunning corruption tests...")
print("-" * 50)

for name in corruption_list:
    if not hasattr(corruptions, name):
        print(f"[FAIL] {name}: Function not found in module.")
        failed += 1
        continue

    func = getattr(corruptions, name)
    print(f"Testing {name}...", end=" ")

    try:
        # Some corruptions expect PIL image, some numpy array.
        # The original `corrupt` wrapper in __init__.py handles this usually.
        # But we are testing corruptions.py directly.
        # Looking at code:
        # Most take 'x'.
        # jpeg_compression takes x and calls x.save(), so expects PIL.
        # motion_blur takes x and calls x.save(), so expects PIL.
        # pixelate takes x and calls x.resize(), so expects PIL.
        # others usually do np.array(x).

        if name in ['jpeg_compression', 'motion_blur', 'pixelate']:
            inp = img_pil
        else:
            inp = img_np # or PIL, np.array(PIL) works fine.

        # frost expects resource files, hopefully they are found.
        # frost uses resource_filename which should work if pkg_resources is happy,
        # otherwise we might need to mock or ensure files exist relative to execution.

        out = func(inp, severity=1)

        # Check output
        if isinstance(out, Image.Image):
            out = np.array(out)

        if out.shape != (224, 224, 3):
            print(f"[FAIL] Output shape mismatch: {out.shape}")
            failed += 1
        else:
            print("[PASS]")
            passed += 1

    except ImportError as e:
        if "Wand/ImageMagick" in str(e):
            print(f"[SKIP] Missing dependency: {e}")
            skipped += 1
        else:
            print(f"[FAIL] ImportError: {e}")
            traceback.print_exc()
            failed += 1
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        traceback.print_exc()
        failed += 1

print("-" * 50)
print(f"Tests Completed. Passed: {passed}, Skipped: {skipped}, Failed: {failed}")

if failed > 0:
    sys.exit(1)
