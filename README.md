## Scan Slasher - Image Detection From Scanned Files

This script processes scan images and performs the following operations: generating previews for scans and extracting photos from scans.
It's a proof of concept, and in early stage.

### Input Parameters

- `-p` or `--generate-preview`: Generates previews for scans (optional)
- `-e` or `--extract-scans`: Extracts photos from scans (optional)
- `scan_file_name`: Specify the name of a specific scan file (optional)

### Usage

To process scan images, run the following command:

```
python src/main.py [-p] [-e] [scan_file_name]
```

### Output Results

The script generates the following output results:

- Processed Images: The processed images are saved in the "processed" folder.
- Previews: Preview images with contours are saved in the "previews" folder.
- Config Files: Configuration settings for each preview are saved as JSON files in the "previews" folder.

The script provides the following information as JSON:

- Filename: The name of the processed scan image.
- Source: The path to the source scan image.
- Preview: The path to the preview image with contours.
- Config: The path to the configuration file for the preview.
- Processed: A list of paths to the processed images.

The JSON response will be in the following format:

```json
[
    {
        "name": "scan_image.jpg",
        "source": "path/to/scan_image.jpg",
        "preview": "path/to/preview_image.jpg",
        "config": "path/to/config.json",
        "processed": [
            "path/to/processed_image1.jpg",
            "path/to/processed_image2.jpg",
            ...
        ]
    },
    ...
]
```

### Executable

The script can also be packed into an executable file for easy distribution and usage on systems without Python installed. To create an executable, you can use tools like PyInstaller or cx_Freeze.

To create an executable using PyInstaller, run the following command:

```
pyinstaller --onefile src/main.py
```

The executable file will be generated in the "dist" folder.
