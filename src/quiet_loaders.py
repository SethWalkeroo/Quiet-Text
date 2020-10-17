import yaml
import sys, os


class QuietLoaders:

	def resource_path(self, relative):
		if hasattr(sys, "_MEIPASS"):
			return os.path.join(sys._MEIPASS, relative)
		return os.path.join(relative)

	def __init__(self):
		self.settings_path = self.resource_path(os.path.join('data', 'config/settings.yaml'))
		self.default_settings_path = self.resource_path(os.path.join('data', 'config/settings-default.yaml'))
		self.default_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/default.yaml'))
		self.default_theme_path = self.resource_path(os.path.join('data', 'theme_configs/default.yaml'))
		self.python3_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/python3.yaml'))
		self.javascript_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/javascript.yaml'))
		self.c_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/c.yaml'))
		self.cpp_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/cpp.yaml'))
		self.html_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/html-django.yaml'))
		self.css_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/css.yaml'))
		self.go_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/go.yaml'))
		self.md_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/md.yaml'))
		self.yaml_syntax_path = self.resource_path(os.path.join('data', 'syntax_configs/yaml.yaml'))


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

	def load_cpp_syntax(self):
		with open(self.cpp_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_html_syntax(self):
		with open(self.html_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_css_syntax(self):
		with open(self.css_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_go_syntax(self):
		with open(self.go_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_markdown_syntax(self):
		with open(self.md_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)

	def load_yaml_syntax(self):
		with open(self.yaml_syntax_path, 'r') as some_config:
			return yaml.load(some_config, Loader=yaml.FullLoader)






