from collections.abc import AsyncIterator
from typing import Annotated

from fast_depends import Depends

from app.db.connection import session_factory
from app.db.uow import SQLAlchemyUOW


async def get_uow() -> AsyncIterator[SQLAlchemyUOW]:
    async with SQLAlchemyUOW(session_factory) as uow:
        yield uow


UOWDep = Annotated[SQLAlchemyUOW, Depends(get_uow)]
