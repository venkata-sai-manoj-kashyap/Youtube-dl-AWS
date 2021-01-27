from flask import Flask, request, render_template, send_file, session
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
    return render_template('format.html', available_formats=available_formats, link=link)


@app.route('/download_link', methods=['POST'])
def gen_download_link():
    format_code = request.form['Input_Num']
    link = session['link']
    download_link = download_file_from_link(link, format_code)
    return send_file(download_link, as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)