import datetime

from aitask.base.types import UUID
from aitask.base.use_case import UseCase
from aitask.db.dependencies import UOWDep
from aitask.stats.heat_map import paint_heat_map
from aitask.stats.pie import paint_pie_plot


class StatsUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def plot_by_statuses(self, user_id: UUID) -> str:
        stats = await self.uow.tasks.get_test_stats(user_id)
        return paint_pie_plot(stats, title="Тестов за все время: {count}")

    async def plot_by_days(
        self,
        user_id: UUID,
        from_dt: datetime.datetime,
        to_dt: datetime.datetime,
    ) -> str:
        stats = await self.uow.tasks.get_task_stats(user_id, from_dt, to_dt)
        return paint_heat_map(stats, title="Выполненных задач за последний год: {count}")
