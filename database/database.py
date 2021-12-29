import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm

DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/todos"
# DATABASE_URL = "sqlite:///./database.db"

engine = sql.create_engine(DATABASE_URL)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative.declarative_base()
