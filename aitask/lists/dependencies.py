from typing import Annotated

from fast_depends import Depends

from aitask.lists.service import TodoListUseCases

TodoListServiceDep = Annotated[TodoListUseCases, Depends(TodoListUseCases)]
