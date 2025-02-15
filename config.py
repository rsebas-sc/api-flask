from sqlmodel import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

postgres_url = os.getenv("DATABASE_URL")


engine = create_engine(postgres_url, echo=True)