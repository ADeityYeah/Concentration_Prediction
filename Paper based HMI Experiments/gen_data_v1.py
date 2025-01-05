import os
import cv2
import pandas as pd

def analyze_images(folder_path, output_csv):
    # Create an empty list to store image data
    image_data = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # Check if the file is an image
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
            try:
                # Read the image using OpenCV
                image = cv2.imread(file_path)

                # Ensure the image is loaded
                if image is not None:
                    # Get the maximum intensity values for each channel
                    max_red = image[:, :, 2].max()
                    max_green = image[:, :, 1].max()
                    max_blue = image[:, :, 0].max()

                    # Get the number of pixels
                    num_pixels = image.shape[0] * image.shape[1]

                    # Append the data to the list
                    image_data.append([file_name, max_red, max_green, max_blue, num_pixels])
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Create a DataFrame from the data
    df = pd.DataFrame(image_data, columns=['Image Name', 'Max Red Intensity', 'Max Green Intensity', 'Max Blue Intensity', 'Number of Pixels'])

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")

# Specify the folder containing the images and the output CSV file
folder_path = 'Set 1\Chromium ions'  # Replace with your folder path
output_csv = 'Set 1\Chromium ions\image_analysis.csv'         # Replace with your desired CSV file name

# Run the analysis
analyze_images(folder_path, output_csv)
