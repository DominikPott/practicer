from setuptools import setup

setup(
    name='practicer',
    version='0.11',
    packages=['practicer.gui', 'practicer.gui.pyside', 'practicer.gui.pyside.widgets', 'tests', 'practicer',
              'practicer.exercise_stats'],
    url='https://github.com/DominikPott/practicer/',
    license='MIT',
    author='Dominik',
    author_email='dominikpott@gmail.com',
    description='A Collection of Painting Exercises',
    python_requires=">=3"
)
