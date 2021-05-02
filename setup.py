# setup.py

from setuptools import setup, find_packages

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
