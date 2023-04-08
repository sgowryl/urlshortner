import hashlib
from enum import Enum
from fastapi import FastAPI

# database init
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dataase over 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

# create a square endpoint which will return sqaure of a number
@app.get("/square/{number}")
async def square(number: int):
    return {"square": number*number}
    
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "jeez"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# url shortner
urls = {}

@app.get("/shorten/{url}")
async def shorten(url):
    short_url = hashlib.md5(url.encode('UTF-8')).hexdigest()[:5]
    urls[short_url] = url
    return {"original": url, 
            "short": short_url}

@app.get("/orginal_url/{short_url}")
async def expand_item(short_url):
        url = urls[short_url]
        return {"original": url, 
            "short": short_url}
