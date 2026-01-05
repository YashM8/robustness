import numpy as np
import pandas as pd
from src.corrupt_tta import corrupt, corruption_dict
import matplotlib.pyplot as plt
import seaborn as sns

def generate_report():
    # Use a fixed seed for reproducibility
    np.random.seed(42)
    
    # Create a base image (uniform gray with some structure)
    base_img = np.full((224, 224, 3), 128, dtype=np.uint8)
    # Add some structure
    base_img[50:150, 50:150, :] = 200
    
    results = []
    
    for name, func in corruption_dict.items():
        for severity in [1, 3, 5]:
            corrupted = func(base_img, severity=severity)
            
            # Calculate statistics
            mean_diff = np.mean(np.abs(base_img.astype(float) - corrupted.astype(float)))
            std_dev = np.std(corrupted)
            min_val = np.min(corrupted)
            max_val = np.max(corrupted)
            
            results.append({
                "Corruption": name,
                "Severity": severity,
                "Mean Diff": mean_diff,
                "Std Dev": std_dev,
                "Min": min_val,
                "Max": max_val
            })
            
    df = pd.DataFrame(results)
    
    # Save to CSV
    df.to_csv("/home/ubuntu/corruption_stats.csv", index=False)
    
    # Create a visualization of Mean Difference by Severity
    plt.figure(figsize=(15, 10))
    sns.barplot(data=df, x="Corruption", y="Mean Diff", hue="Severity")
    plt.xticks(rotation=45, ha='right')
    plt.title("Impact of Corruptions (Mean Pixel Difference from Original)")
    plt.tight_layout()
    plt.savefig("/home/ubuntu/corruption_impact.png")
    
    print("Statistical report and visualization generated.")
    return df

if __name__ == "__main__":
    generate_report()
