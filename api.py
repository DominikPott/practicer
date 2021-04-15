import exercise_interface
import file_setup
import reference_images


def exercises():
    return exercise_interface.exercises()


def create(exercise):
    file_setup.create(exercise)


def references_images(exercise):
    path = r"Z:\referenzen\Fashion"
    collection = reference_images.crawl_images(root=path)
    print(collection)
    images = collection.get(exercise["categories"][1], [])
    return images
