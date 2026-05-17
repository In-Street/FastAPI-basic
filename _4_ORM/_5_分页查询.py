"""
		select(xx).where(xx).offset( (page-1)*size ).limit(size)
"""
from datetime import datetime

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ._1_建表 import BookModel
from ._2_查询 import get_session

page_router = APIRouter(prefix='/page')


@page_router.get("/search")
async def search(
		page: int = Query(default=1, gt=0),
		size: int = 10,
		se: AsyncSession = Depends(get_session),
):
	result = await se.execute(
		select(BookModel).where(BookModel.create_time > datetime(2022, 12, 25)).offset((page - 1) * size).limit(size)
	)
	return result.scalars().all()
