from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aitask.base.models import Entity
from aitask.base.types import UUID  # noqa: TCH001
from aitask.tasks.schemas import TaskStatus, TestStatus

if TYPE_CHECKING:
    from aitask.lists.models import TodoList
    from aitask.users.models import User
    from aitask.workspaces.models import Workspace


class Task(Entity):
    __tablename__ = "tasks"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="cascade"))
    todo_list_id: Mapped[UUID] = mapped_column(ForeignKey("todo_lists.id", ondelete="cascade"))
    name: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.to_do)
    test_status: Mapped[TestStatus] = mapped_column(default=TestStatus.no_status)
    report_url: Mapped[str | None]

    user: Mapped[User] = relationship(back_populates="tasks")
    workspace: Mapped[Workspace] = relationship(back_populates="tasks")
    todo_list: Mapped[TodoList] = relationship(back_populates="tasks")
