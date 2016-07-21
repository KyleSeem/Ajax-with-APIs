from system.core.controller import *
from system.core.model import Model


class DeveopmentDBConfig(DBConfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = 'root'
    DB_DATABASE_NAME = 'myownapi'
    DB_HOST = 'localhost'
    DB_OPTIONS = {
        'unix_socket': 'Applications/MAMP/tmp/mysql/mysql.sock'
    }
    routes['default_controller'] = "Quotes";

class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('Quotes')

    def index(self):
        return self.load_view('quotes/index.html')

    def index_json(self):
        quotes = self.models['Quotes'].all()
        return jsonify(quotes=quotes)

    def index_html(self):
        quotes = self.models['Quotes'].all()
        return self.load_view('partials/quotes.html', quotes=quotes)    

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()
    def all(self):
        query = "SELECT * FROM quotes"
        return self.db.query_db(query)
