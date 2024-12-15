from flask import Flask, render_template, request, send_from_directory,\
current_app, redirect, url_for
import os
from datetime import date
from openpyxl import load_workbook
from main.routes import read_routes
from main.mywriter import write_to_excel
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()


with app.app_context():
	downloads_path = os.path.join(current_app.root_path, 'downloads')

def routings():
	filename = f'FF LOG {date.today().strftime('%d.%m.%Y')}.xlsx'

	schedule = read_routes()
	wb = load_workbook('main/log.xlsx')
	sheet = wb['FF']

	write_to_excel(schedule, sheet, 5)
	path = f'downloads/{filename}'

	wb.save(path)
	# print(f'saved to {path}')
	return filename

	


@app.get('/download/<path:filename>')
def download(filename):
	print(downloads_path + '/' + filename)
	return send_from_directory(downloads_path, filename)


@app.get('/')
def home():
	return render_template('home.html')


@app.post('/')
def generate_routings():
	content = request.form.get('routes')
	# print(content)
	with open('routings.txt', 'w') as f:
		f.write(content)
	
	routes_file = routings()
	return redirect(url_for('download', filename=routes_file))


@app.get('/help')
def help():
	return render_template('help.html')


if __name__ == '__main__':
	app.run()