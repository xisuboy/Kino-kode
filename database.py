import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

    def execute(self, sql, *args, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    db.commit()
                if fetchone:
                    return cursor.fetchone()
                if fetchall:
                    return cursor.fetchall()

    # Users Table Methods
    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY
        )
        '''
        self.execute(sql, commit=True)

    def save_user(self, telegram_id):
        sql = '''INSERT INTO users (telegram_id) VALUES (%s) ON CONFLICT DO NOTHING'''
        self.execute(sql, telegram_id, commit=True)

    def get_user_count(self):
        sql = "SELECT COUNT(telegram_id) FROM users"
        return self.execute(sql, fetchone=True)[0]

    def get_user_ids(self):
        sql = "SELECT telegram_id FROM users"
        return self.execute(sql, fetchall=True)

    # Channels Table Methods
    def create_channels_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS channels (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL
        )
        '''
        self.execute(sql, commit=True)

    def add_channel(self, channel_name):
        sql = '''INSERT INTO channels (username) VALUES (%s) ON CONFLICT DO NOTHING'''
        self.execute(sql, channel_name, commit=True)

    def delete_channel(self, channel_name):
        sql = '''DELETE FROM channels WHERE username = %s'''
        self.execute(sql, channel_name, commit=True)

    def get_channel_list(self):
        sql = '''SELECT username FROM channels'''
        return [channel[0] for channel in self.execute(sql, fetchall=True)]

    # Kino Table Methods
    def create_kino_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS kino (
            id SERIAL PRIMARY KEY,
            kod VARCHAR(50) UNIQUE NOT NULL,
            nomi VARCHAR(255) NOT NULL,
            yili INTEGER,
            janr VARCHAR(100),
            tili VARCHAR(50),
            video_file_id VARCHAR(255) NOT NULL,
            views INTEGER DEFAULT 0
        )
        '''
        self.execute(sql, commit=True)

    def insert_kino(self, nomi, kod, yili, janr, tili, video_file_id):
        sql = '''INSERT INTO kino (nomi, kod, yili, janr, tili, video_file_id) 
                 VALUES (%s, %s, %s, %s, %s, %s)'''
        self.execute(sql, nomi, kod, yili, janr, tili, video_file_id, commit=True)

    def update_kino(self, nomi, yili, janr, tili, video_file_id, kod):
        sql = '''UPDATE kino SET nomi = %s, yili = %s, janr = %s, tili = %s, video_file_id = %s 
                 WHERE kod = %s'''
        self.execute(sql, nomi, yili, janr, tili, video_file_id, kod, commit=True)

    def delete_kino_by_kod(self, kod):
        sql = '''DELETE FROM kino WHERE kod = %s'''
        self.execute(sql, kod, commit=True)

    def get_kino_by_kod(self, kod):
        sql = '''SELECT id, kod, nomi, yili, janr, tili, video_file_id FROM kino WHERE kod = %s'''
        return self.execute(sql, kod, fetchone=True)

    def increment_kino_views(self, kod):
        sql = '''UPDATE kino SET views = views + 1 WHERE kod = %s'''
        self.execute(sql, kod, commit=True)

    def get_kino_count(self):
        sql = "SELECT COUNT(id) FROM kino"
        return self.execute(sql, fetchone=True)[0]

    def get_all_kino(self):
        sql = '''SELECT kod, nomi FROM kino'''
        return self.execute(sql, fetchall=True)


# Initialization
db = DataBase()
db.create_users_table()
db.create_channels_table()
db.create_kino_table()
