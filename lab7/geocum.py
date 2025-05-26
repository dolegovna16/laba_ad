import rasterio
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Define tile folders
tiles = ["T36UUB", "T36UUA"]

# List of pan-sharpening methods to evaluate
methods = ["nearest", "bilinear", "cubic", "lanczos"]

# Loop through each tile
for tile in tiles:
    print(f"Processing {tile}...")

    # Evaluate each pan-sharpening method
    for method in methods:
        try:
            # Load resampled concatenated image for the current method
            with rasterio.open(
                    f"C:/Users/User/Desktop/Homework/2year/2/AD/lab7/output/resampled_concatenated_{method}_{tile}.tif") as src:
                original = src.read([1, 2, 3])  # Read only the first 3 bands (Red, Green, Blue)

            # Load the pan-sharpened image for the current method
            with rasterio.open(
                    f"C:/Users/User/Desktop/Homework/2year/2/AD/lab7/output/pansharpened_{method}_{tile}.tif") as src:
                sharpened = src.read()  # Read all bands (already 3 bands)

            # Flatten arrays for comparison
            original_flat = original.flatten()
            sharpened_flat = sharpened.flatten()

            # Ensure both arrays have the same length
            if len(original_flat) != len(sharpened_flat):
                print(f"Dimension mismatch for {tile} ({method}): Original ({len(original_flat)}), Sharpened ({len(sharpened_flat)})")
                continue

            # Calculate RMSE and R²
            rmse = np.sqrt(mean_squared_error(original_flat, sharpened_flat))
            r2 = r2_score(original_flat, sharpened_flat)

            print(f"{tile} Results for {method}:")
            print(f"RMSE: {rmse}")
            print(f"R² Score: {r2}")
            print("-" * 50)

        except FileNotFoundError as e:
            print(f"Error loading files for {tile} ({method}): {e}")