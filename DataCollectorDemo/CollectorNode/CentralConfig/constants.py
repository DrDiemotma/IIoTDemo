from enum import StrEnum

class Namespaces(StrEnum):
    FileConfigs: str = "FileConfigurations"
    ConfigEdit: str = "ConfigEdit"
    Client: str = "ClientFrame"

class ExchangeEntry(StrEnum):
    SelectedConfigFile: str = "SelectedConfigFile",
    GlobalClientConfigDirectory: str = "configs"


DEFAULT_TUPLES: dict[str, dict[str, str | float | int | bool | list[str | float | int | bool]]] = {
    Namespaces.FileConfigs: {
        ExchangeEntry.SelectedConfigFile: "",
        ExchangeEntry.GlobalClientConfigDirectory: "configs"
    },
    Namespaces.Client: {
        ExchangeEntry.SelectedConfigFile: ""
    }
}