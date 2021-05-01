# mysetup.py

from distutils.core import setup

import glob

import py2exe 

setup(
    console=["BeBarBall.py"],
    data_files=[("sound",
                 [
                     "bg.ogg",
                     "laugh.wav",
                     "nope.wav"]
                 ),
                ("font",
                 [
                     "arial.ttf",
                     "arialbd.ttf"]
                 )]
)
