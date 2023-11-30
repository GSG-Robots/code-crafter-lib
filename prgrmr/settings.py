import enum
import pathlib
from typing import Any, Union

from .utils.default_settings import DEFAULT_SETTINGS


class SettingsFileType(enum.Enum):
    JSON = enum.auto()
    YAML = enum.auto()


class Settings:
    def __init__(self):
        self.settings = {}

    def update(self, settings: dict):
        self.settings.update(settings)

    def import_from(self, filepath: pathlib.Path, filetype: SettingsFileType):
        raise NotImplementedError()

    def export_to(self, filepath: pathlib.Path, filetype: SettingsFileType):
        raise NotImplementedError()

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.settings[key] = value

    def __delitem__(self, key: str) -> None:
        del self.settings[key]

    def __contains__(self, key: str) -> bool:
        return key in self.settings

    def __iter__(self):
        return iter(self.settings)

    def __len__(self) -> int:
        return len(self.settings)

    def __repr__(self) -> str:
        return repr(self.settings)

    def __str__(self) -> str:
        return str(self.settings)

    def __eq__(self, other: Any) -> bool:
        return self.settings == other

    def __ne__(self, other: Any) -> bool:
        return self.settings != other

    def __call__(self, key: Union[str, None] = None, value: Union[Any, None] = None):
        if key == None:
            return self.settings
        elif value == None:
            return self.settings[key]
        else:
            self.settings[key] = value


settings = Settings()
settings.update(DEFAULT_SETTINGS)
