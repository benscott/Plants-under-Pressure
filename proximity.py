import pandas as pd
import datetime
from sqlalchemy import and_

from base import Session, Page, TraitView
from ocr import OCR

start = datetime.datetime.now()
print(f"start time: {start}")

session = Session()

for trait in session.query(TraitView).limit(2):
    ocr_image = OCR(trait.image_url)
    print(ocr_image.text)


end = datetime.datetime.now()
print(f"start time: {end}")
print(f"duration: {end - start}")
