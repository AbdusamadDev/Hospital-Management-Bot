import sqlite3, datetime
from main import path_normalizer


class QueueModel:
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    def __init__(self, username=None, body=None):
        self.username = username
        self.body = body

    def create(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS queue 
            (id INTEGER, username TEXT, body TEXT, phone INTEGER, time TEXT, PRIMARY KEY ("id"))""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS feedbacks 
            (id INTEGER, username TEXT, body TEXT, time TEXT, PRIMARY KEY ("id"))""")
        self.connection.commit()

    def retrieve_data(self) -> list:
        model = self.cursor.execute("""SELECT * FROM queue""")
        model_list = model.fetchall()
        return model_list

    def add(self):
        if (self.username and self.body) is None:
            return None

        self.cursor.execute(
            """INSERT INTO queue (username, body, time) VALUES (?, ?, ?)""", 
            (self.username, self.body, str(datetime.datetime.now())))
        self.connection.commit()
    
    def cancel_queue(self):
        if (self.username and self.body) is None:
            return None

        query = self.cursor.execute("""SELECT COUNT(*) FROM queue""")
        data_id = int(query.fetchall()[0][0])
        self.cursor.execute("""DELETE FROM queue WHERE id=?""", (data_id,))
        self.connection.commit()
    
    def clear(self):
        self.cursor.execute("""DELETE FROM queue;""")
        self.connection.commit()  

class FeedbacksModel(QueueModel):
    def add(self):
        self.cursor.execute(
            """INSERT INTO feedbacks (username, body, time) VALUES (?, ?, ?)""", 
            (self.username, self.body, str(datetime.datetime.now())))
        self.connection.commit()

    def retrieve_data(self) -> list:
        model = self.cursor.execute("""SELECT * FROM feedbacks""")
        model_list = model.fetchall()
        return model_list

    def clear(self):
        self.cursor.execute("""DELETE FROM feedbacks;""")
        self.connection.commit()        

if __name__ == "__main__":
    obj = QueueModel(
        username="Abdusamad", 
        body="ASDFASDFASDFAsdfasdfasDFASDFASDFASDFasdfasdf"
    )
    obj.create()
    print(obj.cancel_queue())
