import os
import cv2
import pandas as pd
import re

def extract_numbers(input_string):
    # Regular expression pattern to match numbers
    pattern = r'\d+'
    # Use findall() to extract numbers from the input string
    numbers = re.findall(pattern, input_string)
    # Convert the list of strings to integers
    numbers = [int(num) for num in numbers]
    return numbers

def get_conc(name):
    numbers = extract_numbers(name)
    conc = numbers[0] ** (-numbers[1])
    return conc

def remove_characters(input_string, characters_to_remove):
    # Create a translation table where characters_to_remove are mapped to None
    translation_table = str.maketrans('', '', characters_to_remove)
    # Use translate() to remove characters specified in translation_table
    return input_string.translate(translation_table)

def read_images(directory_path):
    image_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    images = []
    for image_file in image_files:
        image_path = os.path.join(directory_path, image_file)
        image = cv2.imread(image_path)
        if image is not None:
            images.append((image_file, image))
        else:
            print(f"Failed to read image: {image_file}")

    return images

# Directory containing images
directory_path = "E:/Documents/Mahindra_University/Supra/HMI Sensing/Co activator pH12 hydrophobic/activator pH12 hydrophobic"

# Read images
images = read_images(directory_path)

max_b = []
max_g = []
max_r = []
file_names = []
concentrations = []

# Display image names and dimensions
for name, img in images:
    #print(f"Image Name: {name}, Dimensions: {img.shape}")

    # Split the image into its RGB channels
    b, g, r = cv2.split(img)

    file_names.append(remove_characters(name, ".jpg"))
    concentrations.append(get_conc(name))

    # Find the maximum intensity in each channel
    max_b.append(cv2.minMaxLoc(b)[1])
    max_g.append(cv2.minMaxLoc(g)[1])
    max_r.append(cv2.minMaxLoc(r)[1])

data = {
    "Name" : file_names,
    "Blue channel max. intensity" : max_b,
    "Green channel max. intensity" : max_g,
    "Red channel max. intensity" : max_r,
    "Concentration" : concentrations, 
}
df = pd.DataFrame(data)
df.to_csv(f"Image_data_{name[0]}{name[1]}.csv")