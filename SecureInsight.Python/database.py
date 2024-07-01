# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for declarative models
Base = declarative_base()

# Define the LSTMmetrics model
class LSTMmetrics(Base):
    __tablename__ = 'LSTMmetrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mode = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)

# Define the MLPmetrics model
class MLPmetrics(Base):
    __tablename__ = 'MLPmetrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mode = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)

# Define the CNNmetrics model
class CNNmetrics(Base):
    __tablename__ = 'CNNmetrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mode = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)

def get_engine(database_url):
    return create_engine(database_url)

def get_session(database_url):
    engine = get_engine(database_url)
    Base.metadata.create_all(bind=engine)  # Ensure tables are created
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Create an engine and ensure tables are created when this script runs directly
if __name__ == "__main__":
    #DATABASE_URL = 'sqlite:///SecureInsight.db'
    
    save_model_path = r'C:\00\model'
    DATABASE_URL = f'sqlite:///{save_model_path}\SecureInsight.db'
    engine = get_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
