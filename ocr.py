
import os
import configparser
import requests
import requests_cache
import pytesseract
from PIL import Image
from io import BytesIO


from config import config
from bhl_image import BHLImage


class OCR(object):

    def __init__(self, image_url):
        self.image = BHLImage(image_url)

    @property
    def text(self):
        return pytesseract.image_to_string(self.image())

    @property
    def data(self):
        return pytesseract.image_to_data(self.image())

    @property
    def hocr(self):
        return pytesseract.image_to_pdf_or_hocr(self.image(), extension='hocr')
