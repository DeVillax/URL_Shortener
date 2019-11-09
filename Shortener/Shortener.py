import sqlite3
import hashlib

class UrlShortener:

    def __init__(self, database='URLShortener', table_name = 'URLS', base_url='shortener.com/'):
        self.db = sqlite3.connect(f'{database}.db')
        self.cursor = self.db.cursor()
        self.table_name = table_name
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, short TEXT, full TEXT)')
        self.base = self._check_base(base_url)
        self.db.commit()

    def shorten(self, url, length=6):
        '''
        Shorten an URL
        :param url: (string) URL link to the website you wish to shorten
        :param length: (integer) length of the shorten URL for binding

        return: shortened URL
        '''
        if not self._check_top_level_domain(url):
            return 'The top level domain is not valid.'

        try:
            short = f"{self.base}{hashlib.sha256(url.encode('utf8')).hexdigest()[:length]}"
        except AttributeError:
            return 'The top level domain for the given base is not valid. Please enter a valid one.'
        
        self.cursor.execute(f'INSERT INTO {self.table_name} (short, full) VALUES  (?,?)', (short, url))
        self.db.commit()
        return short

    def original(self, short):
        '''
        Fetchs the original URL associated to a given shortened URL
        :param short: (string) shortened URL

        return: (string) original URL

        '''
        self.cursor.execute(f'SELECT full FROM {self.table_name} WHERE short = ?', (short,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            print('Binding not found')
            return 

    def close_connection(self):
        '''
        Close the connection to the database
        '''
        self.db.close()

    def _check_top_level_domain(self, url):
        '''
        Check whether the top level domain for a given URL exists

        :param url: (string) URL to be shortened
        
        return: boolean
        '''
        with open('topleveldomains.txt') as document:
            topleveldomain = url.split('//')[-1].split('/')[0].split('.')[-1]
            if topleveldomain.upper() not in document.read():
                return False
            return True
        
    def _check_base(self, base):
        '''
        Validates whether the given base is in the right format.
        The appropiate format should be as follow:
            base.topleveldomain/

        :param base: (string) Base URL for the shortener
        
        return: (string) formatted base
        '''
        if '/'in base:
            if base[-1] == '/':
                pass
            else:
                base.remove('/')
                base.append('/')
        
        if '/' not in base:
            base = f'{base}/'
        
        return base