from func.main import terms_sign
import asyncio

import uvloop
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from hypercorn.asyncio import serve
from hypercorn.config import Config

app = Flask(__name__)


@app.route('/specialize', methods=['POST'])
async def load():
    print("Function load called")
    return ""


@app.route('/v2/specialize', methods=['POST'])
async def loadv2():
    print("Function loadv2 called")
    return ""


@app.route('/healthz', methods=['GET'])
async def healthz():
    print("Function healthz called")
    return "", 200


@app.route('/', methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE'])
async def f():
    print("Function f called")
    return await terms_sign()


asgi_app = WsgiToAsgi(app)
conf = Config()
conf.bind = f"0.0.0.0:8888"
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(serve(asgi_app, conf))
