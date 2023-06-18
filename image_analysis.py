from PIL import Image
from PIL.ExifTags import TAGS, IFD          #https://exiftool.org/TagNames/EXIF.html
import subprocess, os, pathlib, datetime

def start_check(directory, file_name = None):

    if file_name == None:
        image = Image.open(directory)
    else:
        image = Image.open(directory + "\\" + file_name)
    
    fname = pathlib.Path(image.filename)    #path object
    
    #   Dictionary Creation
    info_dict = {
        "Directory": os.path.dirname(image.filename),
        "File Name": os.path.basename(image.filename),
        "Size": fname.stat().st_size,
        "Creation Time": datetime.datetime.fromtimestamp(fname.stat().st_ctime).strftime("%d.%m.%Y %H:%M:%S"),
        "Modification Time": datetime.datetime.fromtimestamp(fname.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S"),
    #    "Image Size": image.size,
    #    "Image Height": image.height,
    #    "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    #   Extracting Exif metadata
    exif_info = image.getexif()
    for tag, value in exif_info.items():
        if tag != 59932:
            info_dict["[Base] " + TAGS.get(tag, "Unknown " + str(tag))] = value
        else:
            pass
    for tag, value in exif_info.get_ifd(IFD.Exif).items():
        if tag != 59932:
            info_dict["[Exif] " + TAGS.get(tag, "Unknown " + str(tag))] = value
        else:
            pass
    for tag, value in exif_info.get_ifd(IFD.GPSInfo).items():
        if tag != 59932:
            info_dict["[GPSInfo] " + TAGS.get(tag, "Unknown " + str(tag))] = value
        else:
            pass
    for tag, value in exif_info.get_ifd(IFD.IFD1).items():
        if tag != 59932:
            info_dict["[IFD1] " + TAGS.get(tag, "Unknown " + str(tag))] = value
        else:
            pass

    #   Extracting metadata with subprocess hachoir   
    exeProcess = "hachoir-metadata"
    
    process = subprocess.Popen([exeProcess,image.filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)

    for tag in process.stdout:
            line = tag.strip().split(':')
            if line[0].strip().replace("- ", "") != "Metadata" :
                info_dict["[Hachoir] " + line[0].strip().replace("- ", "")] = line[-1].strip()

    return info_dict