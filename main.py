from fastapi import FastAPI, Path
from _1_路由._1_请求参数 import song_api_router
from _1_路由._2_响应体 import response_router

"""
	1. 路由是基于装饰器模式：
			app: FastAPI的实例名称
			get：请求方式
	
	2. 外部文件的路由实例APIRouter，需要注册到 main.py 中的FastAPI实例中，否则无法访问		
"""

app = FastAPI(title='初次见面FastAPI', version='1.0')  # FastAPI 实例

app.include_router(song_api_router, prefix="/songs")  # song api路由注册
app.include_router(response_router, prefix="/res")


@app.get("/")
async def root():
	return {"message": "Hello World"}
