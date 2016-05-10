import os
from PIL import Image, ExifTags


def fix_exif(image_path):
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    fix_extensions = ['.jpg', '.jpeg']
    rotate = {3: 180, 6: 270, 8: 90}
    if os.path.splitext(image_path)[1].lower() not in fix_extensions:
        return -1
    try:
        i = Image.open(image_path)
        exif = dict(i._getexif().items())
        if exif[orientation] in rotate:
            r = rotate[exif[orientation]]
            i = i.rotate(r, expand=True)
            i.save(image_path)
            return r
        i.close()
        return 0
    except (AttributeError, KeyError, IndexError):
        return -2
