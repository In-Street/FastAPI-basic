"""
	1.  安装ORM： 阿尔克米
			异步的sqlalchemy:  pip3 install "sqlalchemy[asyncio]"
			异步数据库驱动： pip3 install aiomysql

	2.  使用 create_async_engine  创建异步引擎，函数参数如下：
			a.  连接地址：  mysql+aiomysql://用户名:密码@ip:port/库名
			b.  echo = True  输出SQL日志
			c. pool_size    连接池中保持的持久连接数，默认5
			d.  max_overflow    连接池允许创建的超出pool_size的临时连接数，默认10
			e. pool_recycle    连接的最大存活时间(秒)，超时自动回收。默认-1 不回收，推荐3600
			f. pool_pre_ping    获取连接前自动检测连接有效性，发送心跳检测，避免使用无效连接。 默认False
			g. pool_timeout     获取连接时的最大等待时间（秒），超时抛出异常。默认30

	3. 定义模型类：
			a. 基类，继承 DeclarativeBase，设置通用属性字段：create_time、update_time
			b. 表对应的模型类，继承上面的基类，设置其他属性
					Mapped[xxx]:  约定属性类型 Mapped[int]
					mapped_column() : 映射字段
					字段名: Mapped[xx] = mapped_column(xxx)

	4. 定义建表函数，在 FastAPI 启动时调用建表函数

"""
from datetime import datetime

from sqlalchemy import DateTime, String, Float
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import now
from sqlalchemy import func

db_url = 'mysql+aiomysql://root:taylor18@localhost:3306/fastapi'

# 1. 创建异步引擎
async_db_engine = create_async_engine(
	url=db_url,
	pool_size=5,
	max_overflow=10,
	pool_recycle=3600,
	pool_timeout=30,
	echo=True,
	pool_pre_ping=True,
)


# 2. 定义模型类  /dɪˈklærətɪv/
class BaseModel(DeclarativeBase):
	# 前者python中datetime，后者 sqlalchemy中DateTime
	create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now, insert_default=func.now)
	update_time: Mapped[datetime] = mapped_column(DateTime, default=now, insert_default=now, onupdate=now)


class BookModel(BaseModel):
	__tablename__ = 'book'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(type_=String(100), comment='书名')
	author: Mapped[str] = mapped_column(String(5), comment='作者')
	price: Mapped[float] = mapped_column(Float, comment='价钱', nullable=True)
	publisher: Mapped[str] = mapped_column(String(10), comment="出版社")


# 3. 定义建表函数，在应用启动时创建表。  @app.on_event('startup')  被弃用，替换使用 lifespan
async def create_table(app_resource:dict):
	# 获取异步引擎 - 开启事物 - 建表
	async with async_db_engine.begin() as conn:
		await conn.run_sync(BaseModel.metadata.create_all)  # 模型类元数据创建

	import common
	app_resource[common.DB_ENGIN] = async_db_engine