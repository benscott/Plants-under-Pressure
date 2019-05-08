
import os
import configparser
import errno
import requests
import pytesseract
import logging
from PIL import Image
from io import BytesIO


from config import config


logger = logging.getLogger('leventis')


class BHLImage(object):

    def __init__(self, url):
        self.url = url
        self.cache_path = os.path.abspath(config['general']['cache_path'])
        self._create_cache_directory()
        self.image = self._open_or_download_image(url)

    def _create_cache_directory(self):
        try:
            os.makedirs(self.cache_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def _open_or_download_image(self, url):
        if os.path.isfile(self.file_path):
            return Image.open(self.file_path)
        else:
            logger.info("Downloading image {}".format(self.url))
            return self._download_remote_image()

    def _download_remote_image(self):
        r = requests.get(self.url)
        r.raise_for_status()
        image = Image.open(BytesIO(r.content))
        image.save(self.file_path)
        return image

    @staticmethod
    def _parse_image_id_from_url(url):
        # Extract last part of url
        # https://www.biodiversitylibrary.org/pageimage/27274329 -> 27274329
        return url.split("/")[-1]

    @property
    def file_id(self):
        return self._parse_image_id_from_url(self.url)

    @property
    def file_name(self):
        return '{}.jpg'.format(self.file_id)

    @property
    def file_path(self):
        return os.path.join(self.cache_path, self.file_name)

    def __call__(self):
        return self.image
