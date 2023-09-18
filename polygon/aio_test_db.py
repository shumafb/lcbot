from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import Session
from sqlalchemy import select
import asyncio




engine = create_async_engine("sqlite+aiosqlite:///polygon///testdb.sqlite", echo=True)


class Base(DeclarativeBase):
    pass

class Imei(Base):
    __tablename__ = "imei"

    imei_tac = Column(Integer, primary_key=True)
    device = Column(String)

async_session = Session(bind=engine, expire_on_commit=False)


async def main():
    async with async_session() as session:
        q = session.ex



if __name__ == "__main__":
    asyncio.run(main())