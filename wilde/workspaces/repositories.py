from dataclasses import dataclass
from typing import Any

from wilde.base.specification import ISpecification
from wilde.base.types import UUID
from wilde.db.repository import SQLAlchemyRepository
from wilde.workspaces.models import Workspace


@dataclass
class UserWorkspaceSpecification(ISpecification):
    user_id: UUID

    def apply(self, stmt: Any) -> Any:
        return stmt.where(Workspace.user_id == self.user_id)


class WorkspaceRepository(SQLAlchemyRepository[Workspace]):
    model_type = Workspace
