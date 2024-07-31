import os
import uuid
import pandas as pd
from flask import Flask, render_template, request, Response, send_file

app = Flask(__name__, template_folder='templates')

@app.route('/h', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'neuralnine' and password == "password":
            return 'Success'
        else:
            return 'Failure'

@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.content_type == 'text/plain':
                return file.read().decode()
            elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
                df = pd.read_excel(file)
                return df.to_html()
        return 'File not supported', 400
    return render_template('file_upload.html')

@app.route('/convert_to_csv', methods=['POST'])
def convert_to_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
                df = pd.read_excel(file)
                csv_filename = 'converted_file.csv'
                df.to_csv(csv_filename, index=False)
                return send_file(csv_filename, as_attachment=True)
        return 'File not supported', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)