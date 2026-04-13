from typing import Annotated

from fast_depends import Depends

from aitask.workspaces.service import WorkspaceUseCases

WorkspaceServiceDep = Annotated[WorkspaceUseCases, Depends(WorkspaceUseCases)]
