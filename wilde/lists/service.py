from typing import Any

from wilde.base.pagination import Page, Pagination
from wilde.base.types import UUID
from wilde.base.use_case import UseCase
from wilde.db.dependencies import UOWDep
from wilde.lists.models import TodoList
from wilde.lists.repositories import UserTodoListSpecification
from wilde.users.models import User


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
