from typing import Annotated

from fast_depends import Depends

from aitask.voice.service import VoiceUseCases

VoiceServiceDep = Annotated[VoiceUseCases, Depends(VoiceUseCases)]
