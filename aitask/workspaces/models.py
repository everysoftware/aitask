from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aitask.base.models import Entity
from aitask.base.types import UUID  # noqa: TCH001

if TYPE_CHECKING:
    from aitask.lists.models import TodoList
    from aitask.tasks.models import Task
    from aitask.users.models import User


class Workspace(Entity):
    __tablename__ = "workspaces"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="cascade"))

    user: Mapped[User] = relationship(back_populates="workspaces")
    todo_lists: Mapped[list[TodoList]] = relationship(back_populates="workspace")
    tasks: Mapped[list[Task]] = relationship(back_populates="workspace")
