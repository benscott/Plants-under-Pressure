import logging
import pandas as pd
import datetime
from sqlalchemy import and_, exists
from itertools import product
import re

from base import Session, Page, TraitView, Proximity
from ocr import OCR

start = datetime.datetime.now()
print(f"start time: {start}")

session = Session()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def remove_line_breaks(text):
    return text.replace('\n', ' ').replace('\r', '')


def find_occurences_of_string(haystack_string, needle_string):
    # Find all occurences of needle string in haystack
    # Returning a list of indexes
    matches = re.finditer(needle_string, haystack_string, re.IGNORECASE)
    return [m.start(0) for m in matches]


def find_smallest_distance(trait_indexes, taxon_indexes):

    # Find the two closest occurences of trait and taxon
    trait_index, taxon_index = min(
        product(trait_indexes, taxon_indexes), key=lambda i: abs(i[0]-i[1]))
    return abs(trait_index - taxon_index)


session.begin()

for row in session.query(TraitView).filter(
    ~exists().where(
        and_(
            TraitView.trait_id == Proximity.trait_id,
            TraitView.page_id == Proximity.page_id,
            TraitView.pup_name_id == Proximity.pup_id,
        )
    )
).limit(1):

    logger.info('OCRing %s', row.image_url)

    ocr = OCR(row.image_url)
    ocr_text = remove_line_breaks(ocr.text)

    try:
        ocr_text.index(row.pup_name)
    except:
        genus, specific_epithet = row.pup_name.split(' ')
        taxon_name = f'{genus[0:1]}. {specific_epithet}'
    else:
        taxon_name = row.pup_name

    trait_indexes = find_occurences_of_string(ocr_text, row.trait_term)
    taxon_indexes = find_occurences_of_string(ocr_text, taxon_name)

    print(taxon_indexes)

    if trait_indexes and taxon_indexes:
        char_distance = find_smallest_distance(trait_indexes, taxon_indexes)
    else:
        # Trait or taxon cannot be found in the text
        char_distance = -1

    proximity = Proximity(
        citation_id=row.citation_id,
        trait_id=row.trait_id,
        page_id=row.page_id,
        pup_id=row.pup_name_id,
        char_distance=char_distance,
        taxon_indexes=','.join(map(str, taxon_indexes)),
        trait_indexes=','.join(map(str, trait_indexes)),
    )

    session.add(proximity)

session.commit()

end = datetime.datetime.now()
print(f"start time: {end}")
print(f"duration: {end - start}")
