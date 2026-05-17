"""
	聚合计算： func.方法(模型类.属性)
		count:   session.execute(  select( func.count(BookModel.id) ).where(xxxx)  )
		avg:
		max:
		min:
		sum:
		distinct:
"""
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from ._1_建表 import BookModel
from ._2_查询 import get_session

group_search_router = APIRouter(prefix='/group_search')


@group_search_router.get('/func_test')
async def func_test(se: AsyncSession = Depends(get_session)):

	result = await se.execute(select(func.count(BookModel.id))) # 全部数量


	#  条件筛选后统计数量
	result_count = await se.execute(
		select(
			# func.count(BookModel.id)
			func.count(func.distinct(BookModel.author))
			# BookModel,
		).where(
			BookModel.create_time > datetime(2025, 12, 25),
			BookModel.price > 1.25
		)
	)
	return {
		"total": result.scalar(),
		'where_count': result_count.scalars().all()
	}
