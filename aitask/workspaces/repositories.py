from dataclasses import dataclass
from typing import Any

from aitask.base.specification import ISpecification
from aitask.base.types import UUID
from aitask.db.repository import SQLAlchemyRepository
from aitask.workspaces.models import Workspace


@dataclass
class UserWorkspaceSpecification(ISpecification):
    user_id: UUID

    def apply(self, stmt: Any) -> Any:
        return stmt.where(Workspace.user_id == self.user_id)


class WorkspaceRepository(SQLAlchemyRepository[Workspace]):
    model_type = Workspace
