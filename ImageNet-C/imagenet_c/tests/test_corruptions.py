import sys
import os
import numpy as np
from PIL import Image
import unittest

# Try to import the package. If it fails, add the parent directory to sys.path
try:
    from imagenet_c import corrupt, corruption_dict
except ImportError:
    # Assuming this script is at ImageNet-C/imagenet_c/tests/test_corruptions.py
    # We want to add ImageNet-C/imagenet_c to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(project_root)
    try:
        from imagenet_c import corrupt, corruption_dict
    except ImportError:
        print("Failed to import imagenet_c. Please ensure the package is installed or set PYTHONPATH.")
        sys.exit(1)

class TestCorruptions(unittest.TestCase):
    def setUp(self):
        # Create a dummy image: 224x224 RGB
        self.img_np = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        self.supported_corruptions = list(corruption_dict.keys())

    def test_all_severities(self):
        """Test all corruptions across all severity levels (1-5)."""
        for name in self.supported_corruptions:
            with self.subTest(corruption=name):
                # Check for skipped dependencies (wand)
                try:
                    # Check if the function raises the specific ImportError for wand
                    corruption_dict[name](Image.fromarray(self.img_np), severity=1)
                except ImportError as e:
                    if "Wand/ImageMagick" in str(e):
                        print(f"Skipping {name}: {e}")
                        continue
                    else:
                        raise e
                except Exception as e:
                    self.fail(f"{name} (sev=1) failed with error: {e}")

                for severity in range(1, 6):
                    try:
                        out = corrupt(self.img_np, severity=severity, corruption_name=name)

                        self.assertIsInstance(out, np.ndarray, f"{name} sev={severity} did not return numpy array")
                        self.assertEqual(out.dtype, np.uint8, f"{name} sev={severity} did not return uint8")
                        self.assertEqual(out.shape, (224, 224, 3), f"{name} sev={severity} output shape mismatch")

                    except Exception as e:
                         self.fail(f"{name} severity={severity} failed: {e}")

    def test_corrupt_api_inputs(self):
        """Test corrupt() function API inputs."""
        # Test valid inputs with name
        out = corrupt(self.img_np, severity=1, corruption_name='gaussian_noise')
        self.assertEqual(out.shape, (224, 224, 3))

        # Test integer index
        out_idx = corrupt(self.img_np, severity=1, corruption_number=0)
        self.assertEqual(out_idx.shape, (224, 224, 3))

        # Test missing arguments
        with self.assertRaises(ValueError):
            corrupt(self.img_np, severity=1)

if __name__ == '__main__':
    unittest.main()
