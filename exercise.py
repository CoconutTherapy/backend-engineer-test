import os
import json
from typing import Union

from lib import skill_duration
from lib import schema_validator


def get_json(filename: str) -> Union[object, None]:
    """
    Load json from file
    """
    if not os.path.isfile(filename):
        print("File does not exists")

    with open(filename) as f:
        try:
            data = json.load(f)
        except ValueError:
            return None
        return data


def main():
    freelancer_file = 'exercise/freelancer.json'
    schema = 'exercise/freelancer_schema.json'

    # load data
    freelance = get_json(freelancer_file)
    schema = get_json(schema)

    # validations
    if not freelance or not schema_validator.is_valid(freelance=freelance, schema=schema):
        return

    # process
    output = skill_duration.process_freelance(freelance)

    print(output)


if __name__ == '__main__':
    main()
