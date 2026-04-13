from collections.abc import AsyncIterator
from typing import Annotated

from fast_depends import Depends

from aitask.db.connection import session_factory
from aitask.db.uow import SQLAlchemyUOW


async def get_uow() -> AsyncIterator[SQLAlchemyUOW]:
    async with SQLAlchemyUOW(session_factory) as uow:
        yield uow


UOWDep = Annotated[SQLAlchemyUOW, Depends(get_uow)]
