from dataclasses import dataclass
from typing import Any

from aitask.base.specification import ISpecification
from aitask.base.types import UUID
from aitask.db.repository import SQLAlchemyRepository
from aitask.lists.models import TodoList


@dataclass
class UserTodoListSpecification(ISpecification):
    user_id: UUID
    workspace_id: UUID

    def apply(self, stmt: Any) -> Any:
        return stmt.where(
            TodoList.user_id == self.user_id,
            TodoList.workspace_id == self.workspace_id,
        )


class TodoListRepository(SQLAlchemyRepository[TodoList]):
    model_type = TodoList
