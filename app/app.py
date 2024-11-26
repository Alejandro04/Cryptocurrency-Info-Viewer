from flask import Flask, render_template
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import time
import threading

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración del servidor SMTP
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Crear la aplicación Flask
app = Flask(__name__)

# Función para enviar correo
def enviar_alerta(precio_bitcoin):
    try:
        mensaje = MIMEMultipart()
        mensaje['From'] = EMAIL_ADDRESS
        mensaje['To'] = EMAIL_ADDRESS
        mensaje['Subject'] = 'Alerta: Precio de Bitcoin ha bajado'
        cuerpo = f"El precio de Bitcoin ha bajado a ${precio_bitcoin:.2f}."
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, mensaje.as_string())
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para obtener información de las criptomonedas
def obtener_info_criptomonedas():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parametros = {
        'vs_currency': 'usd',
        'ids': 'bitcoin,ethereum,tether,solana,binancecoin,dogecoin,usd-coin,xrp,cardano,tron',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false'
    }

    try:
        response = requests.get(url, params=parametros)
        response.raise_for_status()
        datos = response.json()

        # Verificar si Bitcoin está por debajo de $95,000 y enviar correo si es necesario
        for moneda in datos:
            if moneda['id'] == 'bitcoin' and moneda['current_price'] < 91000:
                enviar_alerta(moneda['current_price'])

        return datos
    except requests.exceptions.RequestException as err:
        print(f"Error al consultar la API: {err}")
        return []

# Job automático para ejecutar obtener_info_criptomonedas cada 1 minuto
def job_automatico():
    while True:
        print("Ejecutando job automático...")
        obtener_info_criptomonedas()
        time.sleep(60)  # Esperar 1 minuto

# Ruta principal
@app.route('/')
def index():
    criptomonedas = obtener_info_criptomonedas()
    if not criptomonedas:
        error = "No se pudo obtener información de las criptomonedas."
        return render_template('index.html', criptomonedas=[], error=error)
    return render_template('index.html', criptomonedas=criptomonedas, error=None)

# Punto de entrada principal
if __name__ == '__main__':
    # Crear un hilo para el job automático
    job_thread = threading.Thread(target=job_automatico, daemon=True)
    job_thread.start()

    # Iniciar el servidor Flask
    app.run(debug=True)
