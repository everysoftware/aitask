from typing import Any

from aitask.base.pagination import Page, Pagination
from aitask.base.types import UUID
from aitask.base.use_case import UseCase
from aitask.db.dependencies import UOWDep
from aitask.users.models import User
from aitask.workspaces.models import Workspace
from aitask.workspaces.repositories import UserWorkspaceSpecification


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
