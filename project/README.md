Консольна утиліта та WebSocket-чат для отримання курсів валют ПриватБанку.

Technologies
Python 3.14+
aiohttp
asyncio
websockets
aiofile
aiopath
Installation
poetry add aiohttp websockets aiofile aiopath
Console Usage

Отримати курс за 2 дні:

python main.py 2

Отримати курс EUR, USD та PLN:

python main.py 2 EUR USD PLN
WebSocket Server

Запуск сервера:

python websocket_server.py

Сервер запускається на:

ws://localhost:8080
WebSocket Commands

Курс за сьогодні:

exchange

Курс за 5 днів:

exchange 5

Курс за 3 дні для EUR та USD:

exchange 3 EUR USD
Logs

Усі команди логуються у файл:

logs/exchange.log