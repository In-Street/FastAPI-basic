"""
		select(模型类).where(模型类.属性 ==  >=   <= )

			1. 条件组装：
					BookModel.create_time > xxx
					BookModel.id.in_
					and_(条件1, 条件2)
					or_(条件1, 条件2)
				最后进行条件拼装： Select(BookModel).where(xxx)。若是通过列表形式存储的条件，需要解包  .where(*list_a)

			2. 模糊查询 like()
					%  :  0个、1个、多个字符
					_  : 匹配单个字符

			3.  条件位运算：
					&  ：  and_
					|  :   or_
					~  :   not_

"""
from datetime import datetime

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import Select, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ._1_建表 import BookModel
from ._2_查询 import get_session

where_search = APIRouter(prefix='/where_search')


@where_search.get('/by_id/{book_id}')
async def get_book(ids: int,
                   create_time: datetime = None,
                   price: float = None,
                   se: AsyncSession = Depends(get_session)):
	# 最终sql效果：   id in (xx) or (create_time> xx and price > xx)
	select_ = Select(BookModel)
	id_conditions = BookModel.id.in_([ids, 22])
	time_price_conditions = None

	if create_time and price:
		time_price_conditions = and_(
			BookModel.create_time > create_time,
			BookModel.price > price
		)
	elif price:
		time_price_conditions = BookModel.price > price
	elif create_time:
		time_price_conditions = BookModel.create_time > create_time

	# 组装最后的查询条件
	if time_price_conditions is not None:
		select_ = select_.where(
			or_(
				id_conditions, time_price_conditions
			)
		)
	else:
		select_ = select_.where(id_conditions)  # 注意此处要将 select_ 重新赋值，否则将会丢掉where条件

	# func.date(BookModel.create_time) == create_time   # 使用date() 将日期忽略时间部分
	# func.extract('hour',BookModel.create_time) == hour # 只时间部分进行比较

	res = await se.execute(select_)
	# book = res.scalars().one_or_none()
	book = res.scalars().all()
	return book


@where_search.get('/likes')
async def like_book(book_name: str, se: AsyncSession = Depends(get_session)):
	# name_ = await se.execute(Select(BookModel).where(BookModel.name.like(f'{book_name}_')))  # 匹配单个字符

	name_ = await se.execute(Select(BookModel).where(
		(BookModel.name.like(f'{book_name}%'))
		& (BookModel.create_time.between(datetime(2017, 1, 2, 10, 12), datetime(2024, 8, 16, 23, 00)))
	)
	)
	return name_.scalars().all()
