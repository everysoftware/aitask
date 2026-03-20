from typing import Any

from aitask.ai.dependencies import AIDep
from aitask.base.pagination import Page, Pagination
from aitask.base.types import UUID
from aitask.base.use_case import UseCase
from aitask.db.dependencies import UOWDep
from aitask.tasks.models import Task
from aitask.tasks.repositories import TodoListTaskSpecification


class TaskUseCases(UseCase):
    def __init__(self, uow: UOWDep, ai: AIDep) -> None:
        self.uow = uow
        self.ai = ai

    async def get_many(self, todo_list_id: UUID, pagination: Pagination) -> Page[Task]:
        return await self.uow.tasks.get_many(TodoListTaskSpecification(todo_list_id), pagination)

    async def create(self, **kwargs: Any) -> Task:
        task = Task(**kwargs)
        await self.uow.tasks.add(task)
        await self.uow.commit()
        return task

    async def get_one(self, task_id: UUID) -> Task:
        return await self.uow.tasks.get_one(task_id)

    async def update(self, task_id: UUID, **kwargs: Any) -> Task:
        task = await self.uow.tasks.get_one(task_id)
        task.merge_attrs(**kwargs)
        return task

    async def solve(self, task_id: UUID) -> str:
        task = await self.uow.tasks.get_one(task_id)
        todo_list = await self.uow.todo_lists.get_one(task.todo_list_id)
        prompt = f"Todo list: {todo_list.name}. "
        if todo_list.description:
            prompt += f"Description: {todo_list.description}. "
        if todo_list.tags:
            prompt += f"Keywords: {todo_list.tags}. "
        prompt += f"Task: {task.name}. "
        if task.description:
            prompt += f"Description: {task.description}. "
        prompt += "Solve the task"
        return await self.ai.complete(prompt)

    async def delete(self, task_id: UUID) -> None:
        task = await self.uow.tasks.get_one(task_id)
        await self.uow.tasks.remove(task)
        await self.uow.commit()
