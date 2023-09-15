from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///db///db.sqlite", echo=True)


class Base(DeclarativeBase):
    pass


class Imei(Base):
    __tablename__ = "imei"

    imei_tac = Column(Integer, primary_key=True)
    device = Column(String)


def check_imei(imei):
    with Session(autoflush=False, bind=engine) as db:
        imei_list = db.query(Imei).all()
        for imei in imei_list:
            if imei == imei.imei_tac:
                return imei.device

