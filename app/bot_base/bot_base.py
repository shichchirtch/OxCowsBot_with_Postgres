from sqlalchemy import Integer, BigInteger, String, ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

session_marker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

class User(Base):

    __tablename__ = 'users'
    index: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tg_us_id: Mapped[int] = mapped_column(BigInteger) # tg user id
    user_name: Mapped[str] = mapped_column(String(200), nullable=False)
    secret_kit: Mapped[str] = mapped_column(ARRAY(String), default=['0000'])
    total_games: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    wins: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    game_list: Mapped[list[list[str]]] = mapped_column(ARRAY(String), default=[], nullable=True)
    language: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    schritt: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    inline_user_kit: Mapped[str] = mapped_column(String, default='')
    start_time: Mapped[int] = mapped_column(BigInteger, default=0)

class VersusBot(Base):

    __tablename__ = 'with_bot'
    index: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    tg_us_id: Mapped[int] = mapped_column(BigInteger)  # tg user id
    user_name: Mapped[str] = mapped_column(String(200), nullable=False)
    bot_list: Mapped[list[list[str]]] = mapped_column(ARRAY(String), default=[], nullable=True)
    user_combo: Mapped[list[str]] = mapped_column(ARRAY(String), default=['setting_data'], nullable=True)
    bot_pobeda: Mapped[int] = mapped_column(Integer, default=0, nullable=True)

tallys_str_bot = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

four_bools = ["Ox", 'Ox', 'Ox', 'Ox']


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)