from typing import Any

from aitask.base.pagination import Page, Pagination
from aitask.base.types import UUID
from aitask.base.use_case import UseCase
from aitask.db.dependencies import UOWDep
from aitask.lists.models import TodoList
from aitask.lists.repositories import UserTodoListSpecification
from aitask.users.models import User


class TodoListUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_many(
        self,
        user: User,
        workspace_id: UUID,
        pagination: Pagination,
        **kwargs: Any,
    ) -> Page[TodoList]:
        return await self.uow.todo_lists.get_many(
            UserTodoListSpecification(user.id, workspace_id),
            pagination,
            **kwargs,
        )

    async def create(self, **kwargs: Any) -> TodoList:
        checklist = TodoList(**kwargs)
        await self.uow.todo_lists.add(checklist)
        await self.uow.commit()
        return checklist

    async def get_one(self, checklist_id: UUID) -> TodoList:
        return await self.uow.todo_lists.get_one(checklist_id)
