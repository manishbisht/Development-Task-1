import os
import subprocess
from flask import Flask, request, render_template, url_for, send_from_directory
import compute
import glob

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['upload'] = 'upload'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/<filename>')
def show(filename):
    return send_from_directory(app.config['upload'], filename)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("home.html", error="sa")
    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            cmd = ['./processing.sh upload/' + file.filename]
            subprocess.call(cmd, shell=True)
            data = glob.glob("data/*.png")
            out = compute.compute(data, ['upload/' + file.filename.split('.')[0] + '.png'])
            inputt = url_for('show', filename=file.filename)
            return render_template('home.html', result=out, image=inputt, input=data)
        else:
            error = "File Not Found"
            return render_template('home.html', error=error)


if __name__ == '__main__':
    app.run()
