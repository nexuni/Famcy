from gevent.pywsgi import WSGIServer
from Famcy import create_app

app = create_app('test',False)

if __name__ == "__main__":
	http_server = WSGIServer(('0.0.0.0', 8888), app)
	http_server.serve_forever()