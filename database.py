import os
import sqlite3
from cryptography.fernet import Fernet

class SQLiteWriter:
    """
    Gestisce un database SQLite per l'archiviazione, la crittografia e la gestione di dati personali.
    Attributi:
        db_name (str): Nome del file database SQLite. Default: "persone.db".
    """

    def __init__(self, db_name="persone.db"):
        """
        Inizializza un'istanza della classe SQLiteWriter.
        Args:
            db_name (str): Nome del file database SQLite da gestire. Default: "persone.db".
        """
        self.db_name = db_name

    def crypto_db(self, path_key="psw.key"):
        """
        Crittografa il file SQLite (`.db`) e salva il risultato in un file `.enc`.
        Args:
            path_key (str): Percorso del file contenente la chiave di crittografia. Se non esiste, viene generata.
        Comportamento:
            - Crittografa il contenuto del database.
            - Salva il file crittografato come "<db_name>.enc".
            - Chiede all'utente se eliminare il file `.db` originale.
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

    def decrypto_db(self, path_key="psw.key", suppress_prompt=False):
        """
        Verifica la presenza e Decrittografa un database SQlite `.enc` generato da `crypto_excel()`
        dopodichè ripristina il file SQLite originale.
        Args:
            path_key (str): Percorso del file contenente la chiave di crittografia.
            suppress_prompt (bool): Se True, non elimina il file `.enc` dopo la decrittografia.
        Comportamento:
            - Legge la chiave dal file.
            - Decritta il contenuto e sovrascrive il file `.db`.
            - Chiede se eliminare il file `.enc`.
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

        with open(encrypted_filename, "rb") as file_enc:
            encrypted = file_enc.read()

        try:
            decrypted = fernet.decrypt(encrypted)
        except Exception as e:
            print(f"❌ Errore nella decrittografia: {e}")
            return

        with open(self.db_name, "wb") as dec_file:
            dec_file.write(decrypted)
        print(f"✅ File decrittografato e salvato come {self.db_name}")

        if suppress_prompt:
            return

        # Chiede se eliminare il file .enc al termine
        while True:
            scelta = input(f"❓ Vuoi eliminare il file crittografato {encrypted_filename}? (S/N): ").strip().lower()
            if scelta == "s":
                try:
                    os.remove(encrypted_filename)
                    print(f"🗑️ File eliminato.")
                except Exception as e:
                    print(f"❌ Errore durante l'eliminazione di {encrypted_filename}: {e}")
                break
            elif scelta == "n":
                print(f"ℹ️ Il file è stato mantenuto.")
                break
            else:
                print("⚠️ Scelta non valida, riprova.")

    def db_exists(self):
        """
        Controlla se il file del database SQLite esiste.
        Returns:
            bool: True se il file esiste, False altrimenti.
        """
        return os.path.exists(self.db_name)

    def connect(self):
        """
            Apre, quando è necessario, una connessione al database SQLite e inizializza il cursore.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        """
        Se non esiste già, crea la tabella `persone` nel database.
        La struttura, che deve essere uguale al file Excel, include:
           - id (intero, autoincrement)
           - nome
           - cognome
           - indirizzo
           - email
           - telefono
        """
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
        """
        Inserisce una lista di persone nella tabella `persone` del database.
        Args:
            data (list[dict]): Lista di dizionari contenenti i campi:
            - 'nome', 'cognome', 'indirizzo', 'email', 'telefono'
        Comportamento:
            - Apre la connessione al database.
            - Inserisce ogni dizionario come una nuova riga nella tabella `persone`.
            - Salva le modifiche (commit) e chiude la connessione.
            - Stampa un messaggio di conferma al termine dell'inserimento.
        """
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
        """
        Legge e stampa tutte le persone presenti nella tabella `persone`.
        Comportamento:
            - Verifica se il database e la tabella esistono.
            - Stampa tutte le righe trovate o un messaggio se vuoto.
        """
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
        """
        Elimina tutti i dati dalla tabella `persone` e resetta l'autoincrement.
        Comportamento:
            - Rimuove tutte le righe dalla tabella.
            - Reimposta il contatore ID a 1.
        """
        if not os.path.exists(self.db_name):
           return

        try:
            self.connect()
            self.cursor.execute("DELETE FROM persone;")
            self.cursor.execute("DELETE FROM sqlite_sequence WHERE name='persone';")
            self.connection.commit()
            self.connection.close()
          #  print("✅ Tutte le persone sono state eliminate dal database!")

        except Exception as e:
            print(f"❌ Errore durante l'eliminazione dei dati: {e}")

def close(self):
        """
        Chiude la connessione al database se esiste
        """
        if hasattr(self, 'connection'):
            self.connection.close()
            print("✅ Connessione SQLite chiusa")
