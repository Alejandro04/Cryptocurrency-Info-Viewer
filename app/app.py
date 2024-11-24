from flask import Flask, render_template
import requests

# Crear la aplicación Flask
app = Flask(__name__)

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
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error al consultar la API: {err}")
        return []

# Ruta principal
@app.route('/')
def index():
    criptomonedas = obtener_info_criptomonedas()
    return render_template('index.html', criptomonedas=criptomonedas)

# Punto de entrada para Vercel
def create_app():
    return app

# Punto de entrada para ejecutar localmente
if __name__ == '__main__':
    app.run(debug=True)
