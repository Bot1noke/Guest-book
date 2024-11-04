import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase

class Articles(SqlAlchemyBase):
    __tablename__ = 'Articles'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    author = sa.Column(sa.String)

    comments = orm.relation("Comments", back_populates='articles', cascade='all, delete')
