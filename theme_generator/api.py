import random
import os
import logging

logging.basicConfig()
log = logging.getLogger('theme_generator')
log.setLevel(logging.INFO)

basics = ['compositing', 'value', 'color', 'formlanguage/design', 'anatomy', 'perspective', 'shadowConstruction']
time = ["medival", "future", "now"]
culture = ['european', 'greek', 'rome empire', 'viking', 'african', 'japanese', 'hightech', 'tribe']


def theme_selector():
    """Generates a painting theme of the given set of posibilities."""
    tmpBasics, tmpTime, tmpCulture = basics[:], time[:], culture[:]
    random.shuffle(tmpBasics)
    random.shuffle(tmpTime)
    random.shuffle(tmpCulture)
    themes = (tmpBasics.pop(), tmpTime.pop(), tmpCulture.pop())
    log.info("\n\tExcercise: {exercise}\n\t\tTime: {time}\n\tCulture: {culture}".format(exercise=themes[0],
                                                                                        topic=themes[1],
                                                                                        time=themes[2],
                                                                                        culture=themes[3])
             )
    return themes
