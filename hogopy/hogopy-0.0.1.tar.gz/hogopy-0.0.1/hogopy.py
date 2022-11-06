# By: HCoder / Bogdan Tanov
# -*- coding: utf-8 -*-
from PIL import Image
from mss import mss
from gtts import gTTS
import os
import playsound
import geocoder
import threading
import requests
import colorama
from setuptools import setup, find_packages
setup(name='hogopy',
      version='0.0.1',
      url='https://github.com/HCoderHY/hogopy/',
      license='MIT',
      author='HCoder/Bogdan Tanov',
      author_email='playmister00@gmail.com',
      description='Hogopy - it is a library with various functions.',
      zip_safe=False)
def dos(url, isWriteMessage):
    try:
        requests.get(url)
        requests.post(url)
        if isWriteMessage:
            print("Request sent!") 
    except requests.exceptions.ConnectionError:
        if isWriteMessage:
            print("Connection error!") 
class hogopy:
    def conv_image(imageURLWithName, newImageURLWithName):
        img = Image.open(imageURLWithName)
        img.save(newImageURLWithName)
    def screenshot():
        with mss() as sc:
            sc.shot(mon=0)
    def say_message(isFileWithMessage=False, message="Sogopy", language="en", pathForSaveWithName="sound_file.mp3", messagePath=""):
        if isFileWithMessage == True:
            with open(messagePath,"r",encoding="utf-8") as file:
                message = file.read()
        voise = gTTS(message, lang=language)
        fvn = pathForSaveWithName
        voise.save(fvn)
        playsound.playsound(fvn)
    def geolocation(ip="me"):
        g = geocoder.ip(ip)
        return g.latlng
    def dos_attack(urlForDos, writeMessage=False):
        while True:
            dos(urlForDos, writeMessage)