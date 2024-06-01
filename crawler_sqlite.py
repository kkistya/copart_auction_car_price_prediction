from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/pages.db', echo=True)

Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, Sequence('page_id'), primary_key=True)
    link = Column(String(200))
    html = Column(String)

    def __repr__(self):
        return f"<Page(id={self.id}, link={self.link})>"


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def add_page(link: str, html: str):
    existing_page = session.query(Page).filter_by(link=link).first()
    if existing_page is None:
        new_page = Page(link=link, html=html)
        session.add(new_page)
        session.commit()
        return True
    return False


# print(add_page("akfdjvksdfhaefgs", "html_lsghdkghdskg"))
# print(add_page("skjfskufhvakfdjvksdfhaefgs", "html_lsghdkghdskskgfhskufh usfvhg"))
# print(add_page("sskkjrfhkjfskufhvakfdjvksdfhaefgs", "html_lsghdkghdskskgfhskufh usfvhg"))

for page in session.query(Page).all():
    print(page)

session.close()