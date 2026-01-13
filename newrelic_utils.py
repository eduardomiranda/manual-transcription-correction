import configparser
from pathlib import Path

def set_newrelic_license_key(ini_path: str, license_key: str) -> None:
    """
    Adiciona ou atualiza a license_key no arquivo newrelic.ini
    """
    ini_file = Path(ini_path)

    config = configparser.ConfigParser()
    config.optionxform = str  # preserva maiúsculas/minúsculas

    if ini_file.exists():
        config.read(ini_file)

    if "newrelic" not in config:
        config["newrelic"] = {}

    config["newrelic"]["license_key"] = license_key

    with ini_file.open("w") as f:
        config.write(f)
