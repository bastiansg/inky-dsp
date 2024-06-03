import yaml


def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def save_yaml(dict_data: dict, file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write(yaml.dump(dict_data))
