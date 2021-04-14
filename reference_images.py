import random

from PIL import Image, ExifTags


def get_image_tags(image):
    img = Image.open(image)
    img_exif = img.getexif()
    data = {}
    if img_exif:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                data[ExifTags.TAGS[key]] = val
    tags = data.get("XPKeywords", b"")
    tags = tags.decode('utf-16')
    tags = tags.replace("\x00", "")
    tags = tags.split(";")
    return tags


if __name__ == "__main__":
    import os
    imageDir = r"Z:\referenzen\Fashion"
    data = {}
    for root, dirs, files in os.walk(imageDir):
        for f in files:
            tags = get_image_tags(image=os.path.join(root, f))
            for tag in tags:
                data.setdefault(tag, []).append(os.path.join(root, f))
    try:
        data.pop("")
    except KeyError:
        pass
    print(data)
    categories = list(data.keys())
    if not categories:
        print("No Tags found in reference images.")
    random.shuffle(categories)
    categorie = categories.pop()
    images = data[categorie]
    random.shuffle(images)
    image = images[0]
    print(categorie)
    print(image)