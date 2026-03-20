from typing import Annotated

from fast_depends import Depends

from aitask.stats.service import StatsUseCases

StatsServiceDep = Annotated[StatsUseCases, Depends(StatsUseCases)]
