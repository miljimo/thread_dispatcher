import setuptools
import os

READ_ME_FILE = "README.md"
long_description = "A simple thread dispatcher message queue implementation for operations"
if os.path.exists(READ_ME_FILE):
    with open(READ_ME_FILE, "r") as fh:
        long_description = fh.read()

setuptools.setup(name="dispatchers-jimobama",
                 version="0.1.00000",
                 description="A simple thread dispatcher for STA modelling",
                 long_description=long_description,
                 url="https://github.com/miljimo/dispatchers.git",
                 long_description_content_type="text/markdown",
                 author="Obaro I. Johnson",
                 author_email="johnson.obaro@hotmail.com",
                 packages=['dispatchers',],
                 install_requires=[
                     'events-jimobama @ git+https://github.com/miljimo/events.git'],
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",

                 ], python_requires='>=3.6')
