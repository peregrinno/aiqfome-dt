from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import database_settings

engine = create_engine(database_settings.URL)

Session = sessionmaker(engine)