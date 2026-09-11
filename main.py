import argparse
import yaml
from yaml import CLoader as Loader

from modules.json_export import JsonExportModule
from scraper import Scraper

try:
    from modules.ics_export import IcsExportModule
except ModuleNotFoundError as exc:
    if exc.name != "ics":
        raise
    IcsExportModule = None

available_modules = {"json": JsonExportModule}
if IcsExportModule:
    available_modules["ics"] = IcsExportModule


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Specify config location")
    args = parser.parse_args()

    config_file = "config.yml"

    if args.c:
        config_file = args.c

    print("UMinho Schedule tool")

    with open(config_file) as f:
        config = yaml.load(f.read(), Loader)

    scraper = Scraper(config["scraper"])

    for export_method in config["export"].keys():
        if export_method == "ics" and IcsExportModule is None:
            raise ModuleNotFoundError(
                "ICS export requires the optional dependency 'ics'. "
                "Install it with `uv sync --extra ics`."
            )
        if export_method in available_modules.keys():
            export_module = available_modules[export_method](
                config["export"][export_method]
            )
            export_module.export(scraper.lessons)

    print("Finished")


if __name__ == "__main__":
    main()
