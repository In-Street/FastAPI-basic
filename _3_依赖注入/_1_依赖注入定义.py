"""
	依赖注入系统：
		1. 作用： 抽取可复用的组件，实现代码复用、解耦
		2. 创建依赖项：通常为函数
		3. 导入Depends ： fastapi - Depends
		4. 声明依赖项：Depends(依赖项函数名称)
"""
from fastapi import Query, APIRouter, Depends


dependency_injection = APIRouter(prefix='/di', tags=['依赖注入'])


#  创建依赖项，抽取分页参数
async def common_params(
		page: int = Query(default=1, lt=100),
		size: int = Query(default=10, lt=200)
):
	return {'page': page, 'size': size}


# 声明依赖项
@dependency_injection.get('/news_list')
async def news_list(com=Depends(common_params)):
	from common import app_resource
	return {'com': com, ' global': app_resource.get('global_a')}


@dependency_injection.get('/news_list_2')
async def news_list_2():
	return 'DI'
