from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an engine that stores data in the local directory's sqlite.db file
engine = create_engine('sqlite:///data/pages.db', echo=True)

# Declare a Base object for your classes to inherit from
Base = declarative_base()


# Define a User class which will be mapped to a users table
class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, Sequence('page_id'), primary_key=True)
    link = Column(String(200))

    def __repr__(self):
        return f"<Page(id={self.id}, name={self.link})>"


# Create all tables by issuing CREATE TABLE commands to the DB
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

# Create new users
page1 = Page(link='abcde')
page2 = Page(link='sldgfhaedkvhadk')

# Add the new users to the session
session.add(page1)
session.add(page2)

# Commit the session to the database
session.commit()

# Query the database
for page in session.query(Page).all():
    print(page)
