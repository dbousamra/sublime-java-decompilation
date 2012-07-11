import sublime, sublime_plugin, subprocess, platform, urllib, os
from zipfile import ZipFile

class DecompileJavaCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		filename = self.view.file_name()
		self.acquire_jad()
		decompiled = self.decompile(filename)[0]
		self.push_to_new_window(edit, decompiled, filename)

	def decompile(self, filename):
		executable = self.get_jad_exec()[2]
		command = [executable, '-o', '-p', filename]
		return self.exec_command(command)

	def exec_command(self, command):
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()
		return (out, err)

	def push_to_new_window(self, edit, contents, filename):
		new_view = self.view.window().new_file()
		new_view.set_name(self.get_new_filename(filename))
		new_view.insert(edit, 0, contents)
		new_view.set_syntax_file('Packages/Java/Java.tmLanguage')

	def get_new_filename(self, filename):
		return filename.replace("class", "java")

	def get_jad_exec(self):
		os_alias = platform.system().lower()
		jad_location = self.view.settings().get('jad_location')
		if 'win32' in os_alias:
			return ('jad.exe', jad_location, 'jad.exe')
		elif 'linux' in os_alias:
			return ('jad', jad_location, './jad')
		elif 'darwin' in os_alias:
			return ('jad', jad_location, './jad')

	def acquire_jad(self):
		exec_filename = self.get_jad_exec()[0]
		if not self.file_exists(exec_filename):
			if not self.file_exists('jad.zip'):
				download_url = self.get_jad_exec()[1]
				webFile = urllib.urlretrieve(download_url, tempfile.gettempdir() + "jad.zip")
				zipper = ZipFile('jad.zip')
			 	zipper.extract(exec_filename, os.getcwd())
		os.chmod(exec_filename, 0755)


	def file_exists(self, filename):
		try:
			with open(filename) as f: return True
		except IOError as e: return False
