import random
import os
import logging
from config import REF_DIR

logging.basicConfig()
log = logging.getLogger('theme_generator')
log.setLevel(logging.INFO)

basics = ['compositing', 'value', 'color', 'formlanguage/design', 'anatomy', 'perspective', 'shadowConstruction']
topic = os.listdir(REF_DIR)
time = ["medival", "future", "now"]
culture = ['european', 'greek', 'rome empire', 'viking', 'african', 'japanese', 'hightech', 'tribe']


def theme_selector():
    """Generates a painting theme of the given set of posibilities."""
    tmpBasics, tmpTopic, tmpTime, tmpCulture = basics[:], topic[:], time[:], culture[:]
    random.shuffle(tmpBasics)
    random.shuffle(tmpTopic)
    random.shuffle(tmpTime)
    random.shuffle(tmpCulture)
    themes = (tmpBasics.pop(), tmpTopic.pop(), tmpTime.pop(), tmpCulture.pop())
    log.info("\n\tExcercise: {exercise}\n\tTopic: {topic}\n\tTime: {time}\n\tCulture: {culture}".format(exercise=themes[0],
                                                                                                               topic=themes[1],
                                                                                                               time=themes[2],
                                                                                                               culture=themes[3])
             )
    return themes


def scan_dirs(themes):
    ref_dirs = []
    for root, dirs, files in os.walk(REF_DIR):
        for topic in themes:
            if topic in dirs:
                topic_dir = os.path.join(root, topic)
                ref_dirs.append(topic_dir)
    log.debug("Directorys {ref_dirs}".format(ref_dirs=ref_dirs))
    return ref_dirs


def select_reference(ref_dirs):
    images = []
    for ref in ref_dirs:
        for root, dirnames, filenames in os.walk(ref):
            log.debug("Dirnames: {dirnames}".format(dirnames=dirnames))
            files = [os.path.join(root, f) for f in filenames if os.path.isfile(os.path.join(root, f))]
        if not files:
            continue
        random.shuffle(files)
        images.append(files.pop())
    return images


def open_reference(images):
    """Opens reference matching the seleted themes."""
    for image in images:
        os.startfile(image)


def generate_theme():
    """Select themes and opens possible refernce images."""
    themes = theme_selector()
    r = scan_dirs(themes)
    i = select_reference(r)
    open_reference(i)


if __name__ == '__main__':
    while(True):
        generate_theme()
        i = input("e=exit, key=new theme:")
        if i == "e":
            break