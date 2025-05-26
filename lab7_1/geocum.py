import rasterio
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

tiles = ["T36UUB", "T36UUA"]

methods = ["nearest", "bilinear", "cubic", "lanczos"]

for tile in tiles:
    print(f"Processing {tile}...")

    for method in methods:
        try:
            # open the GeoTIFF file in read mode
            with rasterio.open(
                    f"C:/Users/User/Desktop/Homework/2year/2/AD/lab7_1/output/resampled_concatenated_{method}_{tile}.tif") as src:
                original = src.read([1, 2, 3])  # read only the first 3 bands, RGB relevant for analysis

            # pan-sharpened file
            with rasterio.open(
                    f"C:/Users/User/Desktop/Homework/2year/2/AD/lab7_1/output/pansharpened_{method}_{tile}.tif") as src:
                sharpened = src.read() # contains only 3 bands

            # for comparison flatten
            original_flat = original.flatten()                                                                                                                                       # example: original = np.array([[10, 20], [30, 40]]) --> original_flat = original.flatten() == [10, 20, 30, 40]
            sharpened_flat = sharpened.flatten()

            # arrays have same length
            if len(original_flat) != len(sharpened_flat):
                print(f"Dimension mismatch for {tile} ({method}): Original ({len(original_flat)}), Sharpened ({len(sharpened_flat)})")
                continue

            rmse = np.sqrt(mean_squared_error(original_flat, sharpened_flat))
            r2 = r2_score(original_flat, sharpened_flat)

            print(f"{tile} Results for {method}:")
            print(f"RMSE: {rmse}")
            print(f"R² Score: {r2}")
            print("-" * 50)

        except FileNotFoundError as e:
            print(f"Error loading files for {tile} ({method}): {e}")