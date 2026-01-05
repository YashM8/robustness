import numpy as np
from src.corrupt_tta import corrupt
import os

def verify_frost():
    print("Verifying Frost Corruption...")
    # Create a dummy image
    img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    
    try:
        # Apply frost corruption
        corrupted = corrupt(img, severity=3, corruption_name="frost")
        
        # Check output
        print(f"Original shape: {img.shape}")
        print(f"Corrupted shape: {corrupted.shape}")
        print(f"Min value: {np.min(corrupted)}")
        print(f"Max value: {np.max(corrupted)}")
        
        if corrupted.shape == img.shape and np.max(corrupted) <= 255:
            print("SUCCESS: Frost corruption applied correctly.")
        else:
            print("FAILURE: Frost corruption output is incorrect.")
            
    except Exception as e:
        print(f"FAILURE: Frost corruption raised an error: {e}")

if __name__ == "__main__":
    verify_frost()
