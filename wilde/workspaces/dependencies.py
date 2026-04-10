from typing import Annotated

from fast_depends import Depends

from wilde.workspaces.service import WorkspaceUseCases

WorkspaceServiceDep = Annotated[WorkspaceUseCases, Depends(WorkspaceUseCases)]
