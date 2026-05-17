from pydantic import BaseModel


class BookReq(BaseModel):
	name: str = None
	author: str = None
	price: float = None
	publisher: str = None