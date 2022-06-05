from beanie import Document, PydanticObjectId
from datetime import datetime

class Articles(Document):
    id: PydanticObjectId | None = None
    title: str
    body: str
    user: str
    date: datetime | None = None

class Comments(Document):
    article: PydanticObjectId | None = None
    body: str
    user: str
    date: datetime | None = None
