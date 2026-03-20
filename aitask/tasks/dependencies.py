from typing import Annotated

from fast_depends import Depends

from aitask.tasks.service import TaskUseCases

TaskServiceDep = Annotated[TaskUseCases, Depends(TaskUseCases)]
