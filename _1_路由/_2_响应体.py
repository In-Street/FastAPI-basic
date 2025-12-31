"""
	FastAPI 会将函数返回的 Python 对象【字典、列表、pydantic 模型等】，由 jsonable_encoder 转换为JSON格式，包装为 JSONResponse 返回；
	FastAPI 提供的响应类型：
			JSONResponse :  默认JSON格式

			HTMLResponse： 返回 HTML内容
					两种方式实现：
							在装饰器中，指定： response_class=HTMLResponse 、 response_model=pydantic 模型自定义响应类
							返回值类型，指定： return HTMLResponse(xxx)

			PlainTextResponse：返回纯文本
			FileResponse：返回文件下载
			StreamResponse：流式响应
			RedirectResponse：重定向
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from dtos.SongReq import SongReq

response_router = APIRouter(prefix='', tags=['响应体'])  # 定义此模块的路由实例，注册到main.py中


@response_router.get('/html', response_class=HTMLResponse)
async def html_response():
	return '<h1>这是标题</h1>'


@response_router.get('/html_v2')
async def html_response():
	return HTMLResponse(content='<h1>这是标题</h1>')


@response_router.get('/file')
async def file_response():
	file_path = '/Users/chengyufei/Downloads/dmg/common/pictures/082302.png'
	return FileResponse(file_path)


@response_router.get('/custom', response_model=SongReq)
async def custom_response():
	# response_custom = SongReq(name='', album='最伟大的作品', year=2011)
	response_custom = SongReq(album='', year=2001)
	if response_custom.year > 2010:
		raise HTTPException(status_code=500, detail='数据不存在')
	return response_custom
