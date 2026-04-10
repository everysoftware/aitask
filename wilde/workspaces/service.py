from typing import Any

from wilde.base.pagination import Page, Pagination
from wilde.base.types import UUID
from wilde.base.use_case import UseCase
from wilde.db.dependencies import UOWDep
from wilde.users.models import User
from wilde.workspaces.models import Workspace
from wilde.workspaces.repositories import UserWorkspaceSpecification


class WorkspaceUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_many(self, user: User, pagination: Pagination) -> Page[Workspace]:
        return await self.uow.workspaces.get_many(UserWorkspaceSpecification(user.id), pagination)

    async def create(self, **kwargs: Any) -> Workspace:
        workspace = Workspace(**kwargs)
        await self.uow.workspaces.add(workspace)
        await self.uow.commit()
        return workspace

    async def get_one(self, todo_list_id: UUID) -> Workspace:
        return await self.uow.workspaces.get_one(todo_list_id)
