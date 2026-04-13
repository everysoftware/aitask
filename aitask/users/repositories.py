from dataclasses import dataclass
from typing import Any

from aitask.base.specification import ISpecification
from aitask.db.repository import SQLAlchemyRepository
from aitask.users.models import User


class UserRepository(SQLAlchemyRepository[User]):
    model_type = User


@dataclass
class TelegramUserSpecification(ISpecification):
    telegram_id: int

    def apply(self, stmt: Any) -> Any:
        return stmt.where(User.telegram_id == self.telegram_id)
