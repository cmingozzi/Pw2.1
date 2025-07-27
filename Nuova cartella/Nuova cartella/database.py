import os
import sqlite3
from cryptography.fernet import Fernet

class SQLiteWriter:
    def __init__(self, db_name="persone.db"):
        """Inizializza la connessione al database SQLite"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def crypto_db(self, path_key="key.key"):
        """
        Crittografa il file SQLite .db e crea un file .enc.
        Chiede all'utente se eliminare il file .db originale dopo la crittografia.
        """
        if not os.path.exists(self.db_name):
            print(f"⚠️ Il file {self.db_name} non esiste, impossibile crittografare.")
            return

        # Genera la key se non esiste
        if not os.path.exists(path_key):
            key = Fernet.generate_key()
            with open(path_key, "wb") as key_file:
                key_file.write(key)
            print(f"🔐 Key generata e salvata in {path_key}")
        else:
            with open(path_key, "rb") as key_file:
                key = key_file.read()

        fernet = Fernet(key)

        # Legge il contenuto del file .db
        with open(self.db_name, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        encrypted_filename = self.db_name + ".enc"
        with open(encrypted_filename, "wb") as enc_file:
            enc_file.write(encrypted)

        print(f"✅ File crittografato salvato come {encrypted_filename}")

        scelta = input(f"❓ Vuoi eliminare il file DB originale {self.db_name}? (S/N): ").strip().lower()
        if scelta == "s":
            try:
                os.remove(self.db_name)
                print(f"🗑️ File {self.db_name} eliminato.")
            except Exception as e:
                print(f"❌ Errore durante l'eliminazione di {self.db_name}: {e}")
        else:
            print(f"ℹ️ Il file {self.db_name} è stato mantenuto.")

    def decrypto_db(self, path_key="key.key"):
        """
        Decrittografa il file SQLite .enc e ricrea il file .db.
        Chiede all'utente se eliminare il file .enc dopo la decrittografia.
        """
        encrypted_filename = self.db_name + ".enc"
        if not os.path.exists(encrypted_filename):
            print(f"⚠️ Il file crittografato {encrypted_filename} non esiste.")
            return

        if not os.path.exists(path_key):
            print(f"⚠️ Il file della key {path_key} non esiste, impossibile decrittografare.")
            return

        with open(path_key, "rb") as key_file:
            key = key_file.read()

        fernet = Fernet(key)

        with open(encrypted_filename, "rb") as enc_file:
            encrypted = enc_file.read()

        try:
            decrypted = fernet.decrypt(encrypted)
        except Exception as e:
            print(f"❌ Errore nella decrittografia: {e}")
            return

        with open(self.db_name, "wb") as dec_file:
            dec_file.write(decrypted)

        print(f"✅ File decrittografato e salvato come {self.db_name}")

        scelta = input(f"❓ Vuoi eliminare il file crittografato {encrypted_filename}? (S/N): ").strip().lower()
        if scelta == "s":
            try:
                os.remove(encrypted_filename)
                print(f"🗑️ File {encrypted_filename} eliminato.")
            except Exception as e:
                print(f"❌ Errore durante l'eliminazione di {encrypted_filename}: {e}")
        else:
            print(f"ℹ️ Il file {encrypted_filename} è stato mantenuto.")

    def db_exists(self):
        """Controlla se il file db esiste"""
        return os.path.exists(self.db_name)

    def connect(self):
        """Connette al database solo quando necessario"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """Crea la tabella se non esiste già"""
        self.connect()
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
        self.connection.close()

    def write_to_db(self, data):
        """Inserisce i dati nella tabella"""
        self.connect()
        for person in data:
            self.cursor.execute("""
            INSERT INTO persone (nome, cognome, indirizzo, email, telefono)
            VALUES (?, ?, ?, ?, ?)
            """, (person["nome"], person["cognome"], person["indirizzo"], person["email"], person["telefono"]))
        self.connection.commit()
        self.connection.close()
        print("✅ Dati salvati nel database SQLite")

    def read_from_db(self):
        """Legge e stampa le persone dal database se esistono"""
        if not os.path.exists(self.db_name):
            print(f"⚠️ Il file {self.db_name} non esiste. Non ci sono dati da leggere.")
            return

        try:
            self.connect()

            # Controllo che la tabella esista
            self.cursor.execute("""
                    SELECT name FROM sqlite_master WHERE type='table' AND name='persone';
                    """)
            table_exists = self.cursor.fetchone()

            if not table_exists:
                print("⚠️ La tabella 'persone' non esiste nel database.")
                self.connection.close()
                return

            self.cursor.execute("SELECT * FROM persone")
            persone = self.cursor.fetchall()
            if persone:
                print("\n--- Contenuto del Database ---")
                for pers in persone:
                    print(pers)
            else:
                print("❌ Il Database è vuoto.")

            self.connection.close()

        except Exception as e:
            print(f"❌ Errore durante la lettura dal database: {e}")

    def delete_all_data(self):
        """Svuota la tabella e resetta l'autoincrement"""
        if not os.path.exists(self.db_name):
            print(f"⚠️ Il file {self.db_name} non esiste. Nulla da eliminare.")
            return

        try:
            self.connect()
            self.cursor.execute("DELETE FROM persone;")
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='persone';")
            self.connection.commit()
            self.connection.close()
            print("✅ Tutte le persone sono state eliminate dal database!")

        except Exception as e:
            print(f"❌ Errore durante l'eliminazione dei dati: {e}")

def close(self):
        """Chiude la connessione al database"""
        if hasattr(self, 'connection'):
            self.connection.close()
            print("✅ Connessione SQLite chiusa")
