import configparser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


with open('auth.txt', 'r') as f:
    PWD, USR, DB, HOST = f.read().splitlines()

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USR}:{PWD}@{HOST}/{DB}?charset=utf8"


# Create session
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, autocommit=True)
Base = declarative_base(engine)


class Page(Base):
    __tablename__ = 'bhl_ocr_text'

    page_id = Column(Integer, primary_key=True, autoincrement=True)
    ocr_text_raw = Column(String)
    ocr_text_cleaned = Column(String)

    # Look for a specific trait_term in the cleaned ocr text. If found, return as TraitPage object
    def trait_search(self, trait):
        if trait.trait_term in self.ocr_text_cleaned:
            print(f"{trait.trait_term} was found...")
            return TraitPage(page_id=self.page_id, trait_id=trait.trait_id)


class Trait(Base):
    __tablename__ = 'pup_traits'

    trait_id = Column(Integer, primary_key=True, autoincrement=True)
    trait_term = Column(String)


class TraitPage(Base):
    __tablename__ = 'trait_page'

    trait_page_id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer)
    trait_id = Column(Integer)

    def get_values(self):
        return self.trait_page_id, self.page_id, self.trait_id


class TraitView(Base):

    __tablename__ = 'vw_trait_sp_pg'
    __table_args__ = {'autoload': True}

    page_id = Column(Integer, primary_key=True)


class Proximity(Base):

    __tablename__ = 'proximity'

    proximity_id = Column(Integer, primary_key=True)
    citation_id = Column(Integer)
    trait_id = Column(Integer)
    page_id = Column(Integer)
    pup_id = Column(Integer)
    char_distance = Column(Integer)
    trait_indexes = Column(String)
    taxon_indexes = Column(String)
