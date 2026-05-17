"""
		session.add(模型类实例)：
			1. 字段长度超过限制时，路由函数调用方无法获取到异常信息Data too long for column：
					原因：
						执行add()时不会触发任何数据库层面的校验（包括字段长度、主键冲突等）；
						路由函数执行完后才会回到yield后的代码执行commit()—— 此时 HTTP 响应已经发送给调用方，即便commit()抛出异常，也无法回传给调用方，只能在服务端日志中看到。

					解决：
						可在路由函数中，进行 flush \ commit

			2. flush() 与 refresh() 区别：
					flush():

					refresh():

		更新方式：
			1. 查出数据后，进行属性值更新，提交事务
			2.  update(模型类).where(xxx).values(book.dump(xxx))
					dump 方法参数：
						exclude_unset:  只提取请求中实际传入的字段（排除未传的字段，避免覆盖数据库原有值）
						exclude_none:  排除值为None的字段
						include:  允许更新的字段集合

		sqlalchemy-utils 高频使用方法：
				1. 

"""

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.BookReq import BookReq
from ._1_建表 import BookModel
from ._2_查询 import get_session

add_router = APIRouter(prefix='/add')


@add_router.post("/add_book")
async def add_book(book: BookReq, se: AsyncSession = Depends(get_session)):
	req_book = BookModel(**book.__dict__)
	se.add(req_book)
	await se.flush()  # 此处进行flush() ,  可提前触发数据库校验，如字段长度等。否则只能在路由函数执行完，执行yield后的commit才会暴露出问题，这样调用方是获取不到数据库报错信息


@add_router.post("/update_book/{book_id}")
async def update_book(book_id: int, book: BookReq, se: AsyncSession = Depends(get_session)):
	# 1. 先查询数据
	old_book = await se.get(entity=BookModel, ident=book_id)
	if old_book is None:
		raise HTTPException(status_code=404, detail="未找到数据")
	#  2. 更新属性
	old_book.author = book.author

	# await se.delete(old_book)  # 删除数据
	await se.flush()


@add_router.post("/update_book_2/{book_id}")
async def update_book_2(book_id: int, book: BookReq, se: AsyncSession = Depends(get_session)):

	update_ = (update(BookModel)
	           .where(BookModel.id == book_id)
	           .values(
		book.model_dump(exclude_unset=True, exclude_none=True, include={'author', 'name'}))  # 批量传入更新字段
	           .returning(BookModel))  # 可选，返回更新后的值

	update_result = await se.execute(update_)

	# delete_ = delete(BookModel).where(BookModel.id == book_id)
	# delete_result = await se.execute(delete_)

	return update_result.scalar_one_or_none()
