import json

class ConfigUtils(object):
	def __init__(self, config_file_path) -> None:
		self.config_file_path = config_file_path
		self._load_configs()


	def _load_configs(self):
		# I am thinking on dynamically adding each of the fields in the JSON as a
		# property for each object.
		with open(self.config_file_path, 'r') as f:
			self.json_dict = json.load(f)
		pass


	def update_config_value(self, property, value):
		# Statement here for editing dynamic properties
		self.json_dict[property] = value
		with open(self.config_file_path, 'w') as f:
			json.dump(self.json_dict, f, indent=2)