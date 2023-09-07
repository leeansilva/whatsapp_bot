import pywhatkit
import requests
import pyautogui
from datetime import datetime
import time

target_symbol = "USDTARS"
url = 'https://api.binance.com/api/v3/ticker/price'
#Ya que estamos le metemos dolar bluee jajasjasj
url2 = 'https://api.bluelytics.com.ar/v2/latest'

#funcion para obtener precio
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

#funcion para mandar whatsapp
def send_whatsapp_message(price):
    try:
        #Para que no falle le ponemos minimo 60
        seconds = time.time() + 60
        date = datetime.fromtimestamp(seconds)
        #Mandamos el wpp
        pywhatkit.sendwhatmsg('+541135654619', f'Precio de USDT en ARS: ${price}', date.hour, date.minute)
        #Esperamos 10s y cerramos ventana
        time.sleep(10)
        pyautogui.hotkey('alt', 'f4')
    except Exception as e:
        print(f'Error al enviar el mensaje de WhatsApp: {str(e)}')

def main():
    #instaniamos el precio anterior en None como primer try
    previous_price = None
    
    #bucle infinito PA
    while True:
        #traemos el precio en la primer vuelta, que despues ya se transforma en el precio viejo
        price = get_price()
        
        #importante, si precio no es NONE entramos
        if price is not None:
            #si el precio viejo es diferente al precio que trajo get_price entramos
            if price != previous_price:
                #mandamos wpp con precio actual
                send_whatsapp_message(price)
            else: print('Mismo precio')
            #seteamos precio viejo y vuelve al principio del while
            previous_price = price
        
        # Esperamos 2 minutos antes de volver a verificar
        time.sleep(120)

if __name__ == "__main__":
    main()
