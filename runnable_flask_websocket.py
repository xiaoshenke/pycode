from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/echo')
def echo_socket(ws):

    while True:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def hello():
    return \
'''
<html>

    <head>
        <title>Admin</title>

        <script type="text/javascript">
            var ws = new WebSocket("ws://" + location.host + "/echo");
            ws.onmessage = function(evt){ 
                    var received_msg = evt.data;
                    alert(received_msg);
            };

            ws.onopen = function(){
                ws.send("hello john");
            };
        </script>

    </head>

    <body>
        <p>hello world</p>
    </body>

</html>
'''

# refer:https://stackoverflow.com/questions/19899578/how-do-i-get-this-websocket-example-to-work-with-flask
# to run this code: gunicorn -k flask_sockets.worker module_name:app
if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
