from dataclasses import asdict, dataclass
from typing import Self


@dataclass(frozen=True)
class Config:
    lock_duration_minutes: int = 20
    prayer_reminder_minutes: int = 10
    lock_offset_minutes: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> Self:
        validated_config = _validate(cls, data)
        return cls(**validated_config)

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


def _validate(klass: type[Config], data: dict[str, int]) -> dict[str, int]:
    # We get the default options with it's values for comparison.
    defaults = klass().to_dict()

    unvalid_options = set(data) - set(defaults)
    if unvalid_options:
        raise ValueError(f"Unvalid config options: {sorted(unvalid_options)}")

    LDM: int = data.get("lock_duration_minutes", defaults["lock_duration_minutes"])
    if LDM < 1:
        raise ValueError("Lock Duration must be larger than 0 minutes.")

    PRM: int = data.get("prayer_reminder_minutes", defaults["prayer_reminder_minutes"])
    if PRM < 1:
        raise ValueError("Prayer Reminder must be larger than 0 minutes.")

    LOM: int = data.get("lock_offset_minutes", defaults["lock_offset_minutes"])
    if LOM < 0:
        raise ValueError("Locker Offset must be a positive value.")

    return {
        "lock_duration_minutes": LDM,
        "prayer_reminder_minutes": PRM,
        "lock_offset_minutes": LOM,
    }
