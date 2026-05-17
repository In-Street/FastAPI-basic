from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from _1_路由._1_请求参数 import song_api_router
from _1_路由._2_响应体 import response_router
from _3_依赖注入._1_依赖注入定义 import dependency_injection
from _4_ORM._1_建表 import create_table
from _4_ORM._2_查询 import search_router
from _4_ORM._3_条件查询 import where_search
from _4_ORM._4_聚合查询 import group_search_router
from _4_ORM._5_分页查询 import page_router
from _4_ORM._6_插入_更新_删除 import add_router

import common

"""
	1. 路由是基于装饰器模式：
			app: FastAPI的实例名称
			get：请求方式
	
	2. 外部文件的路由实例APIRouter，需要注册到 main.py 中的FastAPI实例中，否则无法访问		
	
	3. 在应用启动时进行建表，旧版 @app.on_event("startup") 已废弃，使用lifespan代替
"""

# 异步上下文， 同时存储可全局访问的内容
@asynccontextmanager
async def lifespan(app: FastAPI):
	print(f'应用启动（异步）：初始化数据库，创建表')
	common.app_resource['global_a'] = '一首歌的时间'
	await create_table(common.app_resource)
	yield
	print(f'应用关闭（异步）：释放资源')
	common.app_resource.clear()


app = FastAPI(title='初次见面FastAPI', version='1.0', lifespan=lifespan)  # FastAPI 实例

from _2_中间件._1_中间件定义 import register_middleware
register_middleware(app)  # 调用注册函数，将中间件绑定到app

app.include_router(song_api_router, prefix="/songs")  # song api路由注册
app.include_router(response_router, prefix="/res")
app.include_router(dependency_injection)
app.include_router(search_router)
app.include_router(where_search)
app.include_router(group_search_router)
app.include_router(page_router)
app.include_router(add_router)


@app.get("/")
async def root():
	return {"message": "Hello World"}

# @app.on_event('startup')
# @app.lifespan
# async def startup_event():
# 	print(f'应用启动（异步）：初始化数据库，创建表')
# 	app.state.db.pool = '初始化共享资源，全局可访问'
# 	await create_table()
# 	yield
# 	print(f'应用关闭（异步）：释放资源')
# 	app.state.db.pool = None
