import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase

class Comments(SqlAlchemyBase):
    __tablename__ = 'Comments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    author = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.String, nullable=False)
    articleId = sa.Column(sa.Integer, sa.ForeignKey('Articles.id'))

    articles = orm.relation("Articles")