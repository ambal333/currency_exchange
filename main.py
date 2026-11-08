from http.server import HTTPServer
from database.db_connection import DatabaseConnection
from http_requests.server import RequestServer

if __name__ == '__main__':
    host, port = 'localhost', 8000
    server = HTTPServer((host, port), RequestServer)
    database = DatabaseConnection()
    server.database = database
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        database.close()

