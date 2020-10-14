import yaml


class QuietLoaders:

	def __init__(self):
		self.settings_path = 'config/settings.yaml'
		self.default_settings_path = 'config/settings-default.yaml'
		self.default_syntax_path = 'syntax_configs/default.yaml'
		self.default_theme_path = 'theme_configs/default.yaml'
		self.python3_syntax_path = 'syntax_configs/python3.yaml'
		self.javascript_syntax_path = 'syntax_configs/javascript.yaml'
		self.c_syntax_path = 'syntax_configs/c.yaml'


	def load_settings_data(self, default=False):
		if not default:
			with open(self.settings_path, 'r') as some_config:
				return yaml.load(some_config, Loader=yaml.FullLoader)
		else:
			with open(self.default_settings_path, 'r') as some_config:
				return yaml.load(some_config, Loader=yaml.FullLoader)

	def store_settings_data(self, new_settings):
		with open(self.settings_path, 'w') as settings_config:
			yaml.dump(new_settings, settings_config)

	def load_default_theme(self):
		with open(self.default_theme_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_default_syntax(self):
		with open(self.default_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_python3_syntax(self):
		with open(self.python3_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_javascript_syntax(self):
		with open(self.javascript_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_c_syntax(self):
		with open(self.c_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)






