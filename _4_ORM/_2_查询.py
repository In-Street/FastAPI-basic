"""
	1. 创建异步会话工厂
			a. async_sessionmaker 返回的是一个可调用对象AsyncSessionLocal，是一个工厂。每次调用 AsyncSessionLocal() 会调用到 __call__实例方法，创建出一个AsyncSession新实例

			b. 工厂模式： 不直接创建对象，通过工厂方法创建对象，可统一配置和管理对象的创建。
					通过 AsyncSessionLocal() 创建出的实例都包含工厂中的基础配置【引擎、不过期等配置】
					也可进行定制,覆盖工厂中的配置项： session_1 = AsyncSessionLocal(expire_on_commit = True)

			c.  expire_on_commit =False: 影响的是在 session.commit() 调用之后对对象访问的行为
					执行 yield session，会将session传递到路由函数，路由函数中执行查询获取到user，缓存结果，即使手动session.commit 后缓存不会过期，在路由函数中属性访问 user.xxx 都会使用之前查询得到的user，不会触发新的数据库查询；
					若 expire_on_commit =True，则 在commit 提价事务后 所有从数据库加载的ORM对象都会被标记为过期，访问属性 user.name 会自动重新执行查询，从数据库中加载最新的数据，虽然确保了数据的一致性，但产生额外的库查询。

					expired_on_commit=False时，路由函数中执行第二次查询仍然是用的第一次的缓存结果，获取新数据使用 session.refresh(user) 或 session.expire(user) ，session.expire 使缓存结果失效但是不会立即查询新数据，当访问属性时才会触发新查询，
					或者绕过缓存populate_existing=True： select(User).where(User.id == 1).execution_options(populate_existing=True). 即使对象已在缓存中，也强制从数据库重新加载，并用数据库中的最新数据更新（覆盖）这个已存在对象的属性。

	2. 创建依赖项，从会话工厂中获取数据库会话
			a.  使用  yield session 返回，不能使用return
					若使用return，那么在执行完 return session 后，会立即执行 async with 上下文管理的 __aexit__ 方法，其中包含 session.close()。那么调用方得到是一个已关闭的会话，无法使用。

					若使用 yield ，在执行完 yield session，会暂停，不退出async with 块，FastAPI 将session传递给路径操作函数来使用此session，
					当路径操作函数执行完毕后，返回到 async with 块中 执行 yield后面的代码，最后退出async with 块。

	3. 在接口参数中指定依赖项，进行数据库操作
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
import common
from ._1_建表 import BookModel,async_db_engine

search_router = APIRouter(prefix='/search',tags=['书本查询'])

# 1. 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
	bind=async_db_engine,  # 绑定异步引擎
	expire_on_commit=False,  # 会话对象不过期
	class_=AsyncSession
)

# 2. 创建依赖项
async def get_session():
	async with AsyncSessionLocal() as db_session:
		try:
			yield db_session   # 此处使用 yield 返回，原因看上面文档注释第二点
			await db_session.commit()
		except:
			await db_session.rollback()
			raise
		# finally:
		# 	await db_session.close()  #  finally 块冗余，在 async with 上下文管理中，会自动调用close()


# 路径函数使用依赖项
@search_router.get('/books')
async def book_list(db: AsyncSession = Depends(get_session)):

	result = await db.execute(select(BookModel))
	all_books = result.scalars().all()  # 获取所有
	first_book = result.scalars().first() # 获取单条
	get_by_id = db.get(BookModel, 1) # 根据主键，获取单条
	return


