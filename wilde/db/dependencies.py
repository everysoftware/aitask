from collections.abc import AsyncIterator
from typing import Annotated

from fast_depends import Depends

from wilde.db.connection import session_factory
from wilde.db.uow import SQLAlchemyUOW


async def get_uow() -> AsyncIterator[SQLAlchemyUOW]:
    async with SQLAlchemyUOW(session_factory) as uow:
        yield uow


UOWDep = Annotated[SQLAlchemyUOW, Depends(get_uow)]
