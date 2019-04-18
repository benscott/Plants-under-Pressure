import pandas as pd
from base import Session, Page, Trait, TraitPage
import datetime
from sqlalchemy import and_

start = datetime.datetime.now()
print(f"start time: {start}")

session = Session()
pages = list(session.query(Page))
traits = list(session.query(Trait))

for page in pages:
    # Empty list to hold TraitPage objects
    trait_pages = []

    # Check if the trait term is found
    for trait in traits:
        trait_page = page.trait_search(trait)
        if trait_page is not None:
            trait_pages.append(trait_page)

    # Write to db.trait_page
    if len(trait_pages) > 0:
        print(trait_pages)
        result = session.add_all(trait_pages)
        session.flush()

session.close()

end = datetime.datetime.now()
print(f"start time: {end}")
print(f"duration: {end - start}")
