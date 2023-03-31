import os
import orjson as json


class Config:
    def __init__(self, processor_name: str, config_filename: str):
        self._processor_name = processor_name
        self._config_filename = config_filename

        with open(config_filename, 'r') as file_desc:
            data = file_desc.read()
            self._properties = json.loads(data)

    @property
    def processor_name(self):
        return self._processor_name

    @property
    def class_name(self):
        return self.get(self._processor_name, 'class_name')

    @property
    def properties(self):
        return self._properties

    def get(self, section, key):
        value = os.getenv(section + '_' + key)
        if value is not None:
            print(f'{section} - {key} : overridden by environment variable: {value}')
            return value

        if key not in self._properties[section]:
            return None

        return self._properties[section][key]

    def get_parameters(self, section):
        return self._properties[section].keys()
