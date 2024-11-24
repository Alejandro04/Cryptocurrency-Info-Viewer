from flask import Flask, render_template
import requests

app = Flask(__name__)

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

@app.route('/')
def index():
    # Obtener datos de las criptomonedas
    criptomonedas = obtener_info_criptomonedas()
    return render_template('index.html', criptomonedas=criptomonedas)

if __name__ == '__main__':
    app.run(debug=True)
