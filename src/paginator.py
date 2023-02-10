import json
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate, LimitOffsetPage
from file_storage import read
from pydantic import BaseModel
from validator import MessageSchema

app = FastAPI()


@app.get('/messages', response_model=LimitOffsetPage[MessageSchema])
async def get_messages():
    messages_list = [json.loads(elem) for elem in read()]
    messages_schemas = [MessageSchema(**elem) for elem in messages_list]
    return paginate(messages_schemas)


add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app)
