from fastapi import FastAPI
from beanie import init_beanie, PydanticObjectId
import motor.motor_asyncio
from datetime import datetime
from models import Articles, Comments
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_headers=['*'],
    allow_methods=['*']
)

async def init():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://mongo:mongo123@cluster0.lii4f.mongodb.net/?retryWrites=true&w=majority")
    await init_beanie(database=client.forum, document_models=[Articles, Comments])

@app.on_event('startup')
async def startup_event():
    await init()

@app.get("/articles/{id}")
async def get_article(id:PydanticObjectId):
    articles = await Articles.find({"/articles/":id}).to_list()
    return articles

@app.get("/articles")
async def get_articles():
    articles = await Articles.find().to_list()
    return articles


@app.get("/comments/{id}")
async def get_comments(id:PydanticObjectId):
    comments = await Comments.find({"article":id}).to_list()
    return comments

    
@app.get("/comments")
async def get_comments():
    comments = await Comments.find().to_list()
    return comments

@app.post("/articles")
async def post_articles(article:Articles):
    article.date = datetime.now()
    await Articles.insert_one(article)
    return article

@app.post("/comments")
async def post_comments(comment:Comments):
    comment.date = datetime.now()
    await Comments.insert_one(comment)
    return comment

@app.delete("/articles/{id}")
async def delete_articles(article:Articles):
    await Articles.delete(article)
    return article

    