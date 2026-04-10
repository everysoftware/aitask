from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wilde.base.models import Entity
from wilde.base.types import UUID  # noqa: TCH001

if TYPE_CHECKING:
    from wilde.tasks.models import Task
    from wilde.users.models import User
    from wilde.workspaces.models import Workspace


class TodoList(Entity):
    __tablename__ = "todo_lists"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    workspace_id: Mapped[UUID] = mapped_column(ForeignKey("workspaces.id", ondelete="cascade"))
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    tags: Mapped[str] = mapped_column(default="")

    user: Mapped[User] = relationship(back_populates="todo_lists")
    workspace: Mapped[Workspace] = relationship(back_populates="todo_lists")
    tasks: Mapped[list[Task]] = relationship(back_populates="todo_list")
