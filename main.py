import os
from http.server import HTTPServer

from dotenv import load_dotenv

from database.db_connection import DatabaseConnection
from handler.handler import RequestHandler


def main():
    load_dotenv()
    host, port = os.getenv('HOST'), int(os.getenv('PORT'))
    server = HTTPServer((host, port), RequestHandler)
    database = DatabaseConnection()
    server.database = database
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        database.close()


if __name__ == '__main__':
    main()
