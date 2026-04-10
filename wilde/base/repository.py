from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from wilde.base.models import Entity
from wilde.base.pagination import LimitOffset, Page, Pagination
from wilde.base.sorting import Sorting
from wilde.base.specification import ISpecification
from wilde.base.types import UUID

T = TypeVar("T", bound=Entity)


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, model: T) -> T: ...

    @abstractmethod
    async def get(self, identity: UUID) -> T | None: ...

    @abstractmethod
    async def get_one(self, identity: UUID) -> T: ...

    @abstractmethod
    async def find(self, criteria: ISpecification) -> T | None: ...

    @abstractmethod
    async def find_one(self, criteria: ISpecification) -> T: ...

    @abstractmethod
    async def remove(self, model: T) -> T: ...

    @abstractmethod
    async def get_many(
        self,
        criteria: ISpecification | None = None,
        pagination: Pagination = LimitOffset(),
        sorting: Sorting = Sorting(),
    ) -> Page[T]: ...
