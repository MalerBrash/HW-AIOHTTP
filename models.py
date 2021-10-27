import hashlib
from datetime import datetime
from aiohttp import web
import asyncpg
from gino import Gino
from errors import NotFound

db = Gino()


class ModelMixin:

    @classmethod
    async def create_instance(cls, *args, **kwargs):
        try:
            return (await cls.create(*args, **kwargs))
        except asyncpg.exceptions.UniqueViolationError:
            raise web.HTTPBadRequest

    @classmethod
    async def by_id(cls, object_id):
        resp = await cls.get(object_id)
        if resp:
            return resp
        else:
            raise NotFound(f'This ID has not exist in {cls.__tablename__}!')

    @classmethod
    async def update_model(cls, object_id, **kwargs):
        req = await cls.by_id(object_id)
        if kwargs.get('password', False):
            kwargs['password'] = hashlib.md5(kwargs['password'].encode()).hexdigest()
        await req.update(**kwargs).apply()
        response = await cls.by_id(object_id)
        return response

    @classmethod
    async def delete_model(cls, object_id):
        resp = await cls.by_id(object_id)
        if resp:
            await resp.delete()
            return object_id
        else:
            raise NotFound(f'This ID has not exist in {cls.__tablename__}!')


class User(db.Model, ModelMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(), nullable=False)

    _idx1 = db.Index('users_username', 'username', unique=True)
    _idx2 = db.Index('users_email', 'email', unique=True)

    @classmethod
    async def create_instance(cls, *args, **kwargs):
        kwargs['password'] = hashlib.md5(kwargs['password'].encode()).hexdigest()
        return await super().create_instance(*args, **kwargs)

    def to_dict(self):
        user_data = super().to_dict()
        user_data.pop('password')
        return user_data


class Article(db.Model, ModelMixin):
    __tablename__ = 'articles'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def to_dict(self):
        article_data = super().to_dict()
        article_data['pub_date'] = str(self.pub_date)
        return article_data
