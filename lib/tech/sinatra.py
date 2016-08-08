import os
import shutil
import sys
import tarfile
import urllib.request
import configparser

from config import *
from lib.helper import *
from lib.tech.ruby import Ruby


class Sinatra (Ruby):
	techDescription = 'Sinatra is a DSL for quickly creating web applications in Ruby with minimal effort.'

	def __init__ (self, **kwargs):
		super (Sinatra, self).__init__ (**kwargs)

		self.nginxConf['server']['location'] = {
			'/'       :
				{
					'proxy_pass'      : 'http://unix:' + self.socket,
					'proxy_set_header': [
						'Host $http_host',
						'X-Real-IP $remote_addr',
						'X-Forwarded-Proto $scheme',
						'X-Forwarded-For $proxy_add_x_forwarded_for'
					]
				},
			'/static/': {
				'alias': CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['document_root'], 'static')
			}
		}

		self.techConf = {
			'bind'      : 'unix:' + self.socket,
			'workers'   : 4,
		}

		self.confFile = CreatePath (Config.serverRoot, self.serverName, Config.serverDirs['config'], 'gunicorn_config.py')

		self.serverStart = 'gunicorn -c {} -D {} --reload'.format (self.confFile, 'index:app')

	def load (self):
		try:
			if self.checkGunicorn ():
				demoIndexPage = '''from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Flask!"

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run()'''
				destinationDir = CreatePath (self.nginxConf['server']['root'])
				destinationFile = CreatePath (destinationDir, 'index.py')
				os.chdir (destinationDir)
				fw = open (destinationFile, "wt")
				fw.write (demoIndexPage)
				fw.close ()
				print ('Демонстрационный файл успешно создан!')
				os.system ('git clone https://github.com/phusion/passenger-ruby-sinatra-demo.git .')
				print ('Новая версия Flask успешно загружена!')
				return True
			else:
				print ('Ошибка! Не удалось загрузить Flask по причине отсутствия Gunicorn')
				return False
		except:
			print ('Ошибка загрузки Flask!')
			return False
