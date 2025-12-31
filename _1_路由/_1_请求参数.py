from fastapi import APIRouter, Path, Query

from dtos.SongReq import SongReq

"""
	定义模块路由实例APIRouter，此外部文件的路由定义，需在 main.py 中进行注册，否则FastAPI主应用无法访问404
"""
song_api_router = APIRouter(prefix='/song', tags=['曲目'])

"""
	1. 路径请求参数
			a.参数校验：fastapi - Path
					范围校验（gt、lt、ge、le）、长度校验、字段描述、pattern
	
	2. Query请求参数
			a. 参数校验： fastapi - Query
					范围校验（gt、lt、ge、le）、长度校验、字段描述、pattern
	
	3. 请求体参数
			a. 自定义类需继承 BaseModel ,  pydantic - BaseModel
			b. 自定义类的属性校验，pydantic - Field
"""


@song_api_router.get('/{song_id}/{album_name}')
async def path_request(song_id: int = Path(..., gt=0, lt=100),
                       album_name: str = Path(..., max_length=5, description='专辑名称')):
	return {"id": song_id, "album_name": album_name}


@song_api_router.get('/list_sones')
async def list_sones(page: int = Query(default=1, lt=100, description='页码'),
                     size: int = Query(default=10, lt=100, description='默认每页10条，最大不超过100')):
	return {'page': page, 'size': size}


@song_api_router.post('/save')
async def save_sone(song_req: SongReq):
	return song_req