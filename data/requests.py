from typing import Sequence, overload, Optional

from sqlalchemy import desc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import update, select, delete

from data.database import async_session
from data.models import User, ModelType


class DB:
    def __init__(self, session: AsyncSession, model: type[ModelType], user_id: int):
        self.session = session
        self.model = model
        self.user_id = user_id

    async def _create(self, model_obj, user_id: int):
        if not await self.is_exists(user_id):
            self.session.add(model_obj)
            await self.session.commit()

            return model_obj

    async def get(
          self, user_id: int = None, sort_by: str = None,
          where_statement: str = None, descend: bool = False,
          select_blocked: bool = False
        ):
        if user_id:
            return await self._get_one(user_id)
        elif select_blocked:
            if self.model is User:
                return await self._get_blocked(sort_by, descend)
        elif sort_by:
            return await self._get_ordered_by(sort_by, descend)
        elif where_statement:
            return await self._get_where(where_statement)
        else:
            return await self._get_all()


    async def _get_one(self, user_id: int):
        user_id = user_id or self.user_id

        statement = select(self.model).where(self.model.user_id == user_id)
        model_obj = (await self.session.execute(statement)).scalar()

        return model_obj

    async def _get_all(self):
        model_objs = (await self.session.execute(select(self.model))).scalars().all()
        return model_objs

    async def _get_where(self, where_statement: str):
        statement = select(self.model).where(text(where_statement))

        model_objs = (await self.session.execute(statement)).scalars().all()
        return model_objs

    async def _get_ordered_by(self, sort_by: str, descend=False):
        valid_columns = {column.name for column in self.model.__table__.columns}
        join_user = False

        if sort_by in valid_columns:
            sort_column = getattr(self.model, sort_by)
        elif sort_by in {column.name for column in User.__table__.columns}:
            sort_column = getattr(User, sort_by)
            join_user = True
        else:
            raise ValueError(f"Column '{sort_by}' does not exist in '{self.model.__name__}' or 'User'.")

        sort_column = desc(sort_column) if descend else sort_column

        statement = select(self.model)

        if join_user:
            statement = statement.join(User, self.model.user_id == User.user_id).options(joinedload(self.model.user))

        statement = statement.order_by(sort_column)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def _get_blocked(self, sort_by: str = None, descend: bool = False) -> Sequence[User]:
        statement = select(User).where(User.is_blocked == True)

        if sort_by in {column.name for column in User.__table__.columns}:
            sort_column = getattr(User, sort_by)
            sort_by = desc(sort_column) if descend else sort_column
            statement = statement.order_by(sort_by)

        blocked_users = (await self.session.execute(statement)).scalars().all()
        return blocked_users

    async def _update(self, user_id: int, **kwargs):
        user_id = user_id or self.user_id
        valid_columns = {column.name for column in self.model.__table__.columns}
        update_data = {key: value for key, value in kwargs.items() if key in valid_columns}

        if update_data:
            statement = update(self.model).where(self.model.user_id == user_id).values(update_data)
            await self.session.execute(statement)
            await self.session.commit()

        return await self._get_one(user_id)

    async def delete(self, user_id: int):
        user_id = user_id or self.user_id
        model_obj = await self._get_one(user_id)

        statement = delete(self.model).where(self.model.user_id == user_id)
        await self.session.execute(statement)

        return model_obj

    async def is_exists(self, user_id: int = None) -> bool:
        user_id = user_id or self.user_id
        statement = select(self.model).where(self.model.user_id == user_id).limit(1)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None


class Users(DB):
    def __init__(self, session: AsyncSession, user_id: int = None):
        super().__init__(session, User, user_id)

    async def create(self, user_id: int, full_name: str) -> Optional[User]:
        user = User(user_id=user_id, full_name=full_name)
        return await self._create(user, user_id)

    @overload
    async def update(self, user_id: int = None, full_name: str = None): ...  # Need for tips on kwargs

    async def update(self, user_id: int = None, **kwargs) -> User:
        return await self._update(user_id, **kwargs)

    async def set_block(self, user_id: int = None, status: bool = True):
        user_id = user_id or self.user_id
        statement = update(User).where(User.user_id == user_id).values(is_blocked=status)
        await self.session.execute(statement)
        await self.session.commit()

    async def is_blocked(self, user_id: int = None) -> bool:
        user_id = user_id or self.user_id
        statement = select(User.is_blocked).where(User.user_id == user_id)
        blocked_status = (await self.session.execute(statement)).scalar()

        return blocked_status
