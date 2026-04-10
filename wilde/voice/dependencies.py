from typing import Annotated

from fast_depends import Depends

from wilde.voice.service import VoiceUseCases

VoiceServiceDep = Annotated[VoiceUseCases, Depends(VoiceUseCases)]
