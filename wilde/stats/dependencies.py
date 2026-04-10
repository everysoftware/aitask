from typing import Annotated

from fast_depends import Depends

from wilde.stats.service import StatsUseCases

StatsServiceDep = Annotated[StatsUseCases, Depends(StatsUseCases)]
