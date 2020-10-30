from yaml import load, dump, FullLoader
import sys, os

class QuietLoaders:

	def resource_path(self, relative):
		if hasattr(sys, "_MEIPASS"):
			return os.path.join(sys._MEIPASS, relative)
		return os.path.join(relative)

	def __init__(self):
		self.settings_path = self.resource_path(os.path.join('data', 'config/settings.yaml'))
		self.default_settings_path = self.resource_path(os.path.join('data', 'config/settings-default.yaml'))

	def load_settings_data(self, default=False):
		if not default:
			with open(self.settings_path, 'r') as some_config:
				return load(some_config, Loader=FullLoader)
		else:
			with open(self.default_settings_path, 'r') as some_config:
				return load(some_config, Loader=FullLoader)

	def store_settings_data(self, new_settings):
		with open(self.settings_path, 'w') as settings_config:
			dump(new_settings, settings_config)




