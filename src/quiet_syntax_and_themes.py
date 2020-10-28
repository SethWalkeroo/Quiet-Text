import os
from pygments.lexers import (PythonLexer, RustLexer, CLexer, CppLexer, JavaLexer, MarkdownLexer, CssLexer,
         GoLexer, DockerLexer, YamlLexer, JavascriptLexer, HtmlDjangoLexer, SqlLexer,
         CoffeeScriptLexer, DartLexer, HaskellLexer)

class SyntaxAndThemes:

		def __init__(self, master):

			self.master = master

			self.monokaipro_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/monokai_pro.yaml'))
			self.monokai_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/monokai.yaml'))
			self.gruvbox_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/gruvbox.yaml'))
			self.solarized_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/solarized.yaml'))
			self.darkheart_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/dark-heart.yaml'))
			self.githubly_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/githubly.yaml'))
			self.dracula_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/dracula.yaml'))
			self.pumpkin_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/pumpkin.yaml'))
			self.material_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/material.yaml'))
			self.desert_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/desert.yaml'))
			self.rust_theme_path = master.parent.loader.resource_path(
			os.path.join('data', 'theme_configs/rust.yaml'))

		def load_monokai_pro(self):
			self.master.load_new_theme(self.monokaipro_theme_path)

		def load_monokai(self):
			self.master.load_new_theme(self.monokai_theme_path)

		def load_gruvbox(self):
			self.master.load_new_theme(self.gruvbox_theme_path)

		def load_rust(self):
			self.master.load_new_theme(self.rust_theme_path)

		def load_solarized(self):
			self.master.load_new_theme(self.solarized_theme_path)

		def load_darkheart(self):
			self.master.load_new_theme(self.darkheart_theme_path)

		def load_githubly(self):
			self.master.load_new_theme(self.githubly_theme_path)

		def load_dracula(self):
			self.master.load_new_theme(self.dracula_theme_path)

		def load_pumpkin(self):
			self.master.load_new_theme(self.pumpkin_theme_path)

		def load_material(self):
			self.master.load_new_theme(self.material_theme_path)

		def load_desert(self):
			self.master.load_new_theme(self.desert_theme_path)

		def load_python3_syntax(self):
			self.master.lexer = PythonLexer()
			self.master.initial_highlight()

		def load_c_syntax(self):
			self.master.lexer = CLexer()
			self.master.initial_highlight()

		def load_javascript_syntax(self):
			self.master.lexer = JavascriptLexer()
			self.master.initial_highlight()

		def load_cpp_syntax(self):
			self.master.lexer = CppLexer()
			self.master.initial_highlight()

		def load_html_syntax(self):
			self.master.lexer = HtmlDjangoLexer()
			self.master.initial_highlight()

		def load_css_syntax(self):
			self.master.lexer = CssLexer()
			self.master.initial_highlight()

		def load_go_syntax(self):
			self.master.lexer = GoLexer()
			self.master.initial_highlight()

		def load_markdown_syntax(self):
			self.master.lexer = MarkdownLexer()
			self.master.initial_highlight()

		def load_yaml_syntax(self):
			self.master.lexer = YamlLexer()
			self.master.initial_highlight()

		def load_java_syntax(self):
			self.master.lexer = JavaLexer()
			self.master.initial_highlight()

		def load_rust_syntax(self):
			self.master.lexer = RustLexer()
			self.master.initial_highlight()

		def load_docker_syntax(self):
			self.master.lexer = DockerLexer()
			self.master.initial_highlight()

		def load_sql_syntax(self):
			self.master.lexer = SqlLexer()
			self.master.initial_highlight()

		def load_coffeescript_syntax(self):
			self.master.lexer = CoffeeScriptLexer()
			self.master.initial_highlight()

		def load_dart_syntax(self):
			self.master.lexer = DartLexer()
			self.master.initial_highlight()

		def load_haskell_syntax(self):
			self.master.lexer = HaskellLexer()
			self.master.initial_highlight()
