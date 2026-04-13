from enum import StrEnum, auto

from pydantic import ConfigDict

from aitask.base.schemas import BaseModel


class VoiceCommand(StrEnum):
    create_task = auto()
    show_tasks = auto()
    unknown = auto()


class VoiceResponse(BaseModel):
    speech_text: str
    cmd: VoiceCommand

    model_config = ConfigDict(extra="allow")
