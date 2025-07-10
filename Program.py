from flask import Flask, jsonify, render_template
import ccxt
import locale
import time

Program = Flask(__name__)

def BuscaPrecoBtc():
  try:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    Binance = ccxt.binance()

    Ticker = Binance.fetch_ticker('BTC/BRL')
    PrecoAtual = Ticker['last']

    TrintaDias = int((time.time() - 30 * 24 * 60 * 60) * 1000)

    Ohlcv = Binance.fetch_ohlcv('BTC/BRL', timeframe='1d', since=TrintaDias)
    PrecoAntigo = Ohlcv[0][4] if Ohlcv else PrecoAtual

    PrecoAtual = locale.currency(PrecoAtual, grouping=True, symbol=False)
    PrecoAntigo =  locale.currency(PrecoAntigo, grouping=True, symbol=False)

    return PrecoAtual, PrecoAntigo
  except Exception as e:
    print("Erro ao obter preço: ", e)
    return None

@Program.route('/preco')  
def PrecoBtc():
  Atual, Antigo = BuscaPrecoBtc()
  return jsonify({
    'btc_atual': Atual,
    'btc_mes_passado': Antigo
  })

@Program.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  Program.run(debug=True)