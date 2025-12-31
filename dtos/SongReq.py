from pydantic import BaseModel, Field


class SongReq(BaseModel):
	name: str = Field(default='曲名',max_length=10)
	album: str = Field(default='专辑名')
	year: int = Field(..., gt=2000, description='发布年份，2000年以后的')
