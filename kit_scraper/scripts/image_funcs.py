import cairosvg
import os
import cv2
import numpy as np


def convert_svg_to_png(file_path, output_folder):
    # Check if the file is an SVG
    if not file_path.lower().endswith('.svg'):
        return file_path  # Return original path if not an SVG

    # Get the base name (without extension) and the full output path
    base_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    png_file_path = os.path.join(output_folder, f"{file_name_without_ext}.png")

    # Check if the PNG already exists
    if os.path.exists(png_file_path):
        return png_file_path  # Return PNG path if it already exists

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert the SVG to PNG and save it
    try:
        cairosvg.svg2png(url=file_path, write_to=png_file_path)
        print(f"Converted {file_path} to {png_file_path}")
        return png_file_path  # Return the path to the newly created PNG
    except Exception as e:
        print(f"Error converting SVG to PNG: {e}")
        return file_path  # Return the original path if an error occurs


def hex_to_rgb(hex_color: str) -> tuple:
    """
    Converts a hex color string (e.g., '#FF5733') to an RGB tuple (R, G, B).

    Args:
        hex_color (str): The hex color string, optionally prefixed with '#'.

    Returns:
        tuple: A tuple representing the RGB color.
    """
    hex_color = hex_color.lstrip('#')  # Remove the '#' if present
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    else:
        raise ValueError(f"Invalid hex color code: {hex_color}")


def detect_dominant_colors(image_path, mask_path, k=3):
    # Load the image and the mask
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # Load mask as grayscale

    # Ensure the mask is binary (0 and 255 values)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # Reshape the image to a 2D array of pixels (excluding masked areas)
    pixels = masked_image.reshape(-1, 3)

    # Remove black pixels (masked-out areas where RGB = [0, 0, 0])
    pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

    # Convert pixels to float32 for KMeans input (required by OpenCV)
    pixels = np.float32(pixels)

    # Define criteria for K-means (iterations and accuracy)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Run KMeans clustering on the pixels
    _, labels, centers = cv2.kmeans(
        pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    # Convert the centers (dominant colors) back to integer type (RGB)
    dominant_colors_bgr = np.uint8(centers)

    # Convert the BGR colors to RGB format
    dominant_colors_rgb = dominant_colors_bgr[:, ::-1]  # Swap B and R channel

    return dominant_colors_rgb
