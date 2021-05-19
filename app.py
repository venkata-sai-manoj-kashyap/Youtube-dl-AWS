from flask import Flask, request, render_template, send_file, session, redirect, url_for
from handl_resources import fetch_formats, download_file_from_link

app = Flask(__name__)
app.secret_key = "Youtube-ec2-user"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    link = request.form['YoutubeLink']
    session['link'] = link
    available_formats = fetch_formats(link)
    return render_template('format.html', available_formats=available_formats)


@app.route('/download_link', methods=['POST'])
def gen_download_link():
    format_code = request.form['Input_Num']
    link = session['link']
    download_link = download_file_from_link(link, format_code)
    session['download'] = download_link
    return render_template('download_or_stream.html')


@app.route('/download')
def download_file():
    if 'download' in session:
        return send_file(session['download'], as_attachment=True)
    else:
        return redirect(url_for('/', _method="GET"))


@app.route('/stream')
def stream_file():
    if 'download' in session:
        return render_template('stream.html', link=session['download'].rsplit("/")[-1])
    else:
        return redirect(url_for('/', _method="GET"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
