from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import requests
import pyautogui
import time

target_symbol = "USDTARS"
url = 'https://api.binance.com/api/v3/ticker/price'

# Configuración de Selenium para modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')  # Habilita el modo headless

# Ruta al controlador de Chrome (ajusta la ruta según tu ubicación)
driver_path = 'C:\msedgedriver.exe'

# Función para obtener el precio
def get_price():
    response = requests.get(url)
    if response.status_code == 200:
        #si la respuesta es ok, guardamos en data
        data = response.json()
        #mapeamos data
        for item in data:
            #si matchea con USDTARS returnamos el precio del item
            if item["symbol"] == target_symbol:
                return item['price']
    else:
        print(f'Error al realizar la solicitud. Código de estado: {response.status_code}')
        return None

# Función para enviar un mensaje de WhatsApp
def send_whatsapp_message(price):
    try:
        # Para que no falle le ponemos un mínimo de 60 segundos
        seconds = time.time() + 60
        date = datetime.fromtimestamp(seconds)
        # Mandamos el mensaje de WhatsApp
        # Reemplaza 'tu_url' con la URL que deseas abrir en WhatsApp Web
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        driver.get('https://web.whatsapp.com')
        time.sleep(10)  # Espera para escanear el código QR
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.write(f'https://wa.me/tu_url')
        pyautogui.press('enter')
        time.sleep(5)  # Espera a que se cargue la conversación
        pyautogui.write(f'Precio de USDT en ARS: ${price}')
        pyautogui.press('enter')
        time.sleep(5)  # Espera antes de cerrar el navegador
        driver.quit()
    except Exception as e:
        print(f'Error al enviar el mensaje de WhatsApp: {str(e)}')

def main():
    # Inicializamos el precio anterior en None como primer intento
    previous_price = None
    
    while True:
        price = get_price()
        
        if price is not None:
            if price != previous_price:
                send_whatsapp_message(price)
            else:
                print('Mismo precio')
            previous_price = price
        
        # Esperamos 2 minutos antes de volver a verificar
        time.sleep(120)

if __name__ == "__main__":
    main()
