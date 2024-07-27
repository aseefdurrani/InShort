from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import make_transient

# Set up SQLAlchemy
engine = create_engine('sqlite:///news.db')
Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    content = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Delete all rows from the table
session.query(NewsArticle).delete()
session.commit()

print("All rows deleted from the table successfully.")
