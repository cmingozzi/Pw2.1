import sqlite3
import mysql.connector

class SQLiteWriter:
    def __init__(self, db_name="persone.sql"):
        """Inizializza la connessione al database SQLite"""
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """Crea la tabella se non esiste già"""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS persone (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cognome TEXT,
            indirizzo TEXT,
            email TEXT,
            telefono TEXT
        )
        """)
        self.connection.commit()

    def write_to_db(self, data):
        """Inserisce i dati nella tabella"""
        for person in data:
            self.cursor.execute("""
            INSERT INTO persone (nome, cognome, indirizzo, email, telefono)
            VALUES (?, ?, ?, ?, ?)
            """, (person["nome"], person["cognome"], person["indirizzo"], person["email"], person["telefono"]))
        self.connection.commit()
        print("Dati salvati nel database SQLite")

    def read_from_db(self):
        self.cursor.execute("SELECT * FROM persone")
        persone = self.cursor.fetchall()
        if persone:
            print("\n--- Contenuto del Database ---")
            for pers in persone:
                print(pers)
        else:
            print("Il Database è vuoto.")

    def delete_all_data(self):
      #  self.cursor.execute("DELETE FROM persone")
      # Svuota la tabella
        self.cursor.execute("DELETE FROM persone;")

      # Resetta l'AUTOINCREMENT
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='persone';")
        self.connection.commit()
        print("Tutte le persone sono state eliminate dal database!")

    def truncate_table(self):
        self.cursor.execute("TRUNCATE TABLE persone")
        self.connection.commit()
        print("Tutte le persone sono state eliminate dal database e gli indici resettati!")


    def close(self):
        """Chiude la connessione al database"""
        self.connection.close()
        print("Connessione SQLite chiusa")


class MySQLWriter:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        print("Connesso al database MySQL")

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS persone (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50),
            cognome VARCHAR(50),
            indirizzo TEXT,
            email VARCHAR(100),
            telefono VARCHAR(20)
        )
        """)
        self.connection.commit()
        print("Tabella 'persone' creata (se non esiste già)")

    def write_to_db(self, data):
        cursor = self.connection.cursor()
        for person in data:
            cursor.execute("""
            INSERT INTO persone (nome, cognome, indirizzo, email, telefono)
            VALUES (%s, %s, %s, %s, %s)
            """, (person["nome"], person["cognome"], person["indirizzo"], person["email"], person["telefono"]))
        self.connection.commit()
        print("Dati salvati nel database MySQL")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connessione al database MySQL chiusa")


    # Scrive su database MySQL
    # mysql_writer = MySQLWriter(
    #     host="localhost",
    #     user="tuo_utente",
    #     password="tua_password",
    #     database="tuo_database"
    # )
    # try:
    #     mysql_writer.connect()
    #     mysql_writer.create_table()
    #     mysql_writer.write_to_db(persone)
    # finally:
    #     mysql_writer.close()