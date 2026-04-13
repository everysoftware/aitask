from aiogram import Router

from aitask.lists.router import router as checklists_router
from aitask.stats.router import router as stats_router
from aitask.tasks.router import router as tasks_router
from aitask.users.router import router as start_router
from aitask.voice.router import router as voice_router
from aitask.workspaces.router import router as devices_router

routers = [
    start_router,
    checklists_router,
    tasks_router,
    devices_router,
    stats_router,
    voice_router,
]

main_router = Router()
main_router.include_routers(*routers)
