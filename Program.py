from flask import Flask, jsonify, render_template, request
import ccxt
import locale
import time

Program = Flask(__name__)

# ------------ CONFIGURAÇÕES -------------

def BuscaPrecoBtc():
  try:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    Binance = ccxt.binance()

    Ticker = Binance.fetch_ticker('BTC/BRL')
    PrecoAtual = Ticker['last']

    TrintaDias = int((time.time() - 30 * 24 * 60 * 60) * 1000)

    Ohlcv = Binance.fetch_ohlcv('BTC/BRL', timeframe='1d', since=TrintaDias)
    PrecoAntigo = Ohlcv[0][4] if Ohlcv else PrecoAtual

    return PrecoAtual, PrecoAntigo
  except Exception as e:
    print("Erro ao obter preço: ", e)
    return None

@Program.route('/preco')  
def PrecoBtc():
  Atual, Antigo = BuscaPrecoBtc()
  if Atual is None or Antigo is None:
    return jsonify({'error': 'Erro ao obter cotação'}), 500
  return jsonify({
    'btc_atual': float(Atual),
    'btc_mes_passado': float(Antigo)
  })

@Program.route('/calcula/<valorPossuidoPeloUsuario>/<valorBitcoin>', methods=['GET'])
def calculaBTC(valorPossuidoPeloUsuario, valorBitcoin):
  try:
    Soma = float(valorPossuidoPeloUsuario) / float(valorBitcoin)
    return jsonify({'result': Soma})
  except Exception as e:
    return jsonify({'error': 'Erro ao calcular', 'detalhe': str(e)}), 400

# ------------- ROTAS -------------

@Program.route('/')
def index():
  return render_template('index.html')

@Program.route('/ConverteReal.html')
def brlParaBtc():
  return render_template('ConverteReal.html')

if __name__ == '__main__':
  Program.run(debug=True)