import argparse
import os
import cv2
import numpy as np
import imutils
import json


class Config:
    # Image processing parameters

    # Minimum threshold value for binarization (lower values capture more details)
    THRESHOLD_MIN = 210

    # Maximum threshold value for binarization (higher values reduce noise)
    THRESHOLD_MAX = 235

    # Minimum contour area as a percentage of the image area
    # Smaller contours are filtered out as noise (lower values capture larger regions)
    CONTOUR_MIN_AREA = 0.1

    # Maximum contour area as a percentage of the image area
    # Larger contours are filtered out as background (higher values capture smaller regions)
    CONTOUR_MAX_AREA = 0.67

    # Thickness of the contour outline (increase for thicker outlines)
    CONTOUR_THICKNESS = 22

    # Preview width (adjust to control the size of the preview)
    PREVIEW_WIDTH = 800


def generate_or_load_config(previews_folder, filename):
    config_path = os.path.join(
        previews_folder, f"{os.path.splitext(filename)[0]}_config.json")

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "threshold_min": Config.THRESHOLD_MIN,
            "threshold_max": Config.THRESHOLD_MAX,
            "contour_min_area": Config.CONTOUR_MIN_AREA,
            "contour_max_area": Config.CONTOUR_MAX_AREA,
            "contour_thickness": Config.CONTOUR_THICKNESS,
            "preview_width": Config.PREVIEW_WIDTH
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

    return config


def process_scans(input_folder, output_folder, previews_folder, generate_preview_flag, extract_scans_flag, scan_file_name=None):
    # Check if the "uploads" folder exists, create it if it doesn't
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(previews_folder, exist_ok=True)

    results = []

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if scan_file_name and filename != scan_file_name:
                continue

            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            image_path = os.path.join(root, filename)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Error loading image: {image_path}")
                continue

            # Step 1: Generate or load the config settings for the preview
            config = generate_or_load_config(previews_folder, filename)
            threshold_min = config["threshold_min"]
            threshold_max = config["threshold_max"]
            contour_min_area = config["contour_min_area"]
            contour_max_area = config["contour_max_area"]
            contour_thickness = config["contour_thickness"]
            preview_width = config["preview_width"]

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            ret, th = cv2.threshold(gray, threshold_min, threshold_max, 1)

            if int(cv2.__version__.split('.')[0]) < 4:
                _, cnts, hierarchy = cv2.findContours(
                    th.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            else:
                cnts, hierarchy = cv2.findContours(
                    th.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            # Create a copy of the original image to save without contours
            output_image = image.copy()

            processed_images = []

            for idx, c in enumerate(cnts):
                box = cv2.minAreaRect(c)
                if int(cv2.__version__.split('.')[0]) < 4:
                    box = cv2.cv2.boxPoints(box)
                else:
                    box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                Area = image.shape[0] * image.shape[1]
                if Area * contour_min_area < cv2.contourArea(box) < Area * contour_max_area:
                    cv2.drawContours(image, [box], -1,
                                     (0, 255, 0), contour_thickness)
                    # Crop the region of interest (ROI) and save it as a separate image
                    x, y, w, h = cv2.boundingRect(box)
                    roi = output_image[y:y+h, x:x+w]

                    if roi.size == 0:
                        print(f"Error: Empty ROI for image {filename}")
                        continue

                    output_path = os.path.join(
                        output_folder, f"{os.path.splitext(filename)[0]}_image_{idx}.png")

                    if cv2.imwrite(output_path, roi):
                        processed_images.append(output_path)
                    else:
                        print(f"Error saving image: {output_path}")
                        continue

            # Step 2: Save the updated config settings
            config_path = os.path.join(
                previews_folder, f"{os.path.splitext(filename)[0]}_config.json")
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)

            # Step 3: Display the processed image with contours in a smaller preview window
            preview_image = cv2.resize(image, (preview_width, int(
                image.shape[0] * preview_width / image.shape[1])))

            if generate_preview_flag:
                #cv2.imshow("Processed Image", preview_image)
                #cv2.waitKey(0)
                pass

            # Step 4: Save the preview image
            preview_output_path = os.path.join(
                previews_folder, f"{os.path.splitext(filename)[0]}_preview.png")
            cv2.imwrite(preview_output_path, preview_image)

            result = {
                "name": filename,
                "source": image_path,
                "preview": preview_output_path,
                "config": config_path,
                "processed": processed_images
            }
            results.append(result)

            if not generate_preview_flag and extract_scans_flag:
                break

    #cv2.destroyAllWindows()

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process scan images")
    parser.add_argument("-p", "--generate-preview",
                        action="store_true", help="Generate previews for scans")
    parser.add_argument("-e", "--extract-scans",
                        action="store_true", help="Extract photos from scans")
    parser.add_argument("scan_file_name", nargs="?",
                        help="Specify the name of a specific scan file")

    args = parser.parse_args()

    input_folder = "uploads"  # Folder where the input scan images are placed
    output_folder = "processed"  # Folder where the processed images will be saved
    # Folder where the preview images and config files will be saved
    previews_folder = "previews"

    results = process_scans(input_folder, output_folder,
                            previews_folder, args.generate_preview, args.extract_scans, args.scan_file_name)

    print("Results:")
    for result in results:
        print(f"Name: {result['name']}")
        print(f"Source: {result['source']}")
        print(f"Preview: {result['preview']}")
        print(f"Config: {result['config']}")
        print(f"Processed Images: {result['processed']}")
        print("-----------------------------")
