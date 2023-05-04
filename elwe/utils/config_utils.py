import json


class ConfigUtils(object):
	def __init__(self, config_file_path) -> None:
		self.config_file_path = config_file_path
		self._load_configs()


	def _load_configs(self):
		with open(self.config_file_path, 'r') as f:
			self.json_dict = json.load(f)
		
		for k, v in self.json_dict.items():
			setattr(self, k, v)


	def update_config_value(self, property, value):
		self.json_dict[property] = value
		setattr(self, property, value)

		with open(self.config_file_path, 'w') as f:
			json.dump(self.json_dict, f, indent=2)

if __name__ == '__main__':
	cu = ConfigUtils('config/metacritic.json')
	print(cu.last_import_title)