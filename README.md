# ImagesDuplicateDetection-WhatsApp-Fixer
Valid alternative to WhatsApp's "[free up storage](https://faq.whatsapp.com/5503646096388294/?helpref=uf_share)" to keep full control of your photos.

## main.py

You can run this script using `python3 main.py` or `python3 main.py -a .\path_test` or `python3 main.py -f .\path_test file_name.jpg` if you are interested only to analyse a specific file.

Written in Python it checks argv and scans all directories to find ".jpg", ".jpeg", ".png" or ".gif" files.
Using a dictionary and an array, script extract informations from file and calculates an hash code to detect similarity
```python
sha256_hash = hashlib.sha256()
```
When differences are detected, the code will output this information and report the list of files that have been identified as duplicates.

**At the moment, automatic deletion processes are not implemented.**

## image_analysis.py

The code defines a function `start_check` that retrieves detailed information about an image. It utilizes the Pillow library to open the image and extract various details, including EXIF metadata. The retrieved information is stored in a dictionary called `info_dict`.

To use this function, provide the directory path and optionally the file name as input. The function will open the image, retrieve information such as directory, file name, size, creation time, modification time, image format, image mode, and more. It also extracts EXIF metadata and additional metadata using `hachoir-metadata`.

The function returns a dictionary containing all the gathered information. This can be useful for image processing tasks or metadata analysis.

Example usage:
```python
image_info = start_check("/path/to/directory", "image.jpg")
print(image_info)
```
