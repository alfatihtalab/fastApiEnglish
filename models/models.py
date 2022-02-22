from enum import Enum
from typing import Optional
import datetime as datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select

database_name = "englishdb"
database_path = "postgresql://{}:{}@{}/{}".format('postgres', '1773237*', 'localhost:5432', database_name)
engine = create_engine(database_path)
session = Session(engine)


def setup_db():
    SQLModel.metadata.create_all(engine)
    create_accounts()
    create_english_level()


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    phone: str
    imie: Optional[str] = None
    account_id: int = Field(default=None, foreign_key="account.id")
    level_id: int = Field(default=None, foreign_key="level.id")

    def insert(self):
        session.add(self)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


class AccountType(str, Enum):
    developer = "developer"
    admin = "admin"
    simple = "simple"


class EnglishLevel(str, Enum):
    beginner = "beginner"
    elementary = "elementary"
    pre_intermediate = "pre intermediate"
    intermediate = "intermediate"
    upper_intermediate = "upper intermediate"
    advance = "advance"


class Account(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: AccountType


class Level(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: EnglishLevel
    price: float = Field(nullable=True)


class Test(SQLModel, table=True):
    id: int = Field(primary_key=True)
    book_date: str = Field(nullable=False)
    completed: bool
    level_id: int = Field(default=None, foreign_key="level.id")


class SpecialCourse(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str


class SpecialCourseUser(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    spc_id: Optional[str] = Field(
        default=None, foreign_key="specialcourse.id", primary_key=True
    )


def create_accounts():
    acc1 = Account(id=1001, type=AccountType.developer)
    acc2 = Account(id=1002, type=AccountType.admin)
    acc3 = Account(id=1003, type=AccountType.simple)
    with Session(engine) as session:
        statement = select(Account)
        result = session.exec(statement)
        # print(result.all())
        if len(result.all()) == 0:
            try:
                session.add_all([acc1, acc2, acc3])
                session.commit()
            except:
                print('already founded')
            finally:
                session.close()
        else:
            session.commit()
            pass


def create_english_level():
    lev1 = Level(id=1, name=EnglishLevel.beginner, price="")
    lev2 = Level(id=2, name=EnglishLevel.elementary, price="")
    lev3 = Level(id=3, name=EnglishLevel.pre_intermediate, price="")
    lev4 = Level(id=4, name=EnglishLevel.intermediate, price="")
    lev5 = Level(id=5, name=EnglishLevel.upper_intermediate, price="")
    lev6 = Level(id=6, name=EnglishLevel.advance, price="")

    with Session(engine) as session:
        statement = select(Level)
        result = session.exec(statement)
        if len(result.all()) == 0:
            try:
                session.add_all([lev1, lev2, lev3, lev4, lev5, lev6])
                print('here')
            except:
                print('problem founded')
            finally:
                session.commit()
                session.close()
                print("drink your tea")
        else:
            session.close()
            pass
