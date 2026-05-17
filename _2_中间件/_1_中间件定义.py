"""
	中间件： 每次进入FastAPI 应用时都会被执行的函数。在请求到达路由函数之前运行，并在响应返回给客户端之前再运行一次
		1. 函数装饰器，@app.middleware("http")
				中间件函数，参数：
					request : 请求
					call_next： 传递请求给路由函数， response = await call_next(request)

		2. 多个中间件顺序 看注册顺序：自下而上执行。如下定义两个函数，在register_middleware函数中将其注册到app FastAPI 实例中称为中间件函数。 先注册中间件2，再注册中间件1，   访问路由函数时，执行结果为：
				进入中间件-1 ->
				进入中间件-2->
				中间件-2 结束->
				中间件-1 结束

		3. 作用：为每个请求添加统一处理逻辑，如： 日志、身份认证、跨域、性能监控
"""

# from _4_ORM._5_分页查询 import page_router
# @page_router.middleware("http")

from main import app
from fastapi import Request, Response


# @app.middleware("http")  直接在单独文件中定义中间件是不会被执行的。因为main.py中并没有导入此文件，也就是中间件并未注册到app上
async def middleware_1(request: Request, call_next):

	print(f'进入中间件-1，请求路径：{request.url.path}')
	response = await call_next(request)
	print('中间件-1 结束')
	return response


async def middleware_2(request: Request, call_next):

	print(f'进入中间件-2，请求路径：{request.url.path}')
	response = await call_next(request)
	print('中间件-2 结束')
	return response


# 定义注册函数，由 main.py 主动调用（消除循环导入问题）
def register_middleware(app):
	app.middleware('http')(middleware_2)
	app.middleware('http')(middleware_1)
