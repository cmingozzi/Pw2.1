import os
import sqlite3
import pandas as pd
from cryptography.fernet import Fernet
from openpyxl import Workbook

class ExcelWriter:
    """
    Gestisce la creazione, crittografia, decrittografia e lettura di un file Excel
    contenente dati personali inoltre la sua comparazione con un database SQLite.
    Attributi:
        filename (str): Nome del file Excel da gestire. Default: "persone.xlsx"
    """
    def __init__(self, filename = "persone.xlsx"):
        """
        Inizializza un'istanza della classe ExcelWriter.
        Args:
            filename (str): Il nome del file Excel da gestire. Default: "persone.xlsx".
        """
        self.filename = filename

    def crypto_excel(self, path_key="key.key"):
        """
        Crittografa il file Excel associato all'istanza e salva il risultato come file `.enc`.
        Args:
            path_key (str): Percorso del file contenente la chiave di crittografia.
            Se non esiste, verrà generata e salvata.
        Comportamento:
            - Genera una chiave se non esiste.
            - Cripta il file Excel (`self.filename`) e salva un file `.enc`.
            - Chiede all'utente se eliminare il file originale dopo la crittografia.
        """
        if not os.path.exists(self.filename):
            print(f"⚠️ Il file Excel {self.filename} non esiste, impossibile crittografare.")
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

        # Leggi il contenuto del file excel
        with open(self.filename, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        # Salva il file crittografato con estensione .enc
        encrypted_filename = self.filename + ".enc"
        with open(encrypted_filename, "wb") as enc_file:
            enc_file.write(encrypted)

        print(f"✅ File crittografato salvato come {encrypted_filename}")

        # Chiede se eliminare il file originale
        while True:
            scelta = input(f"❓ Vuoi eliminare il file Excel originale {self.filename}? (S/N): ").strip().lower()
            if scelta == "s":
                try:
                    os.remove(self.filename)
                    print(f"🗑️ File {self.filename} eliminato.")
                except Exception as e:
                    print(f"❌ Errore durante l'eliminazione di {self.filename}: {e}")
                break
            elif scelta == "n":
                print(f"ℹ️ Il file {self.filename} è stato mantenuto.")
                break
            else:
                print("⚠️ Scelta non valida, riprova.")

    def decrypto_excel(self, path_key="key.key", suppress_prompt=False):
        """
        Verifica la presenza e Decrittografa un file Excel`.enc` generato da `crypto_excel()`
        dopodichè ripristina il file Excel originale.
        Args:
            path_key (str): Percorso del file contenente la chiave di crittografia.
            suppress_prompt (bool): Se True, non elimina il file `.enc` dopo la decrittografia.
        Comportamento:
            - Verifica la presenza di file Excel e chiave.
            - Se la chiave è corretta ripristina il file Excel.
            - Chiede se eliminare il file `.enc`.
        """
        encrypted_filename = self.filename + ".enc"

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

        with open(self.filename, "wb") as dec_file:
            dec_file.write(decrypted)
        print(f"✅ File decrittografato e salvato come {self.filename}")

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

    def excel_exists(self):
        """
        Verifica se il file Excel esiste nel percorso specificato.
        Returns:
            bool: True se il file esiste, False altrimenti.
        """
        return os.path.exists(self.filename)

    def write_to_excel(self, data):
        """
        Scrive una lista di persone in un file Excel.
        Args:
            data (list[dict]): Lista di dizionari, ciascuno contiene:
            - 'nome'
            - 'cognome'
            - 'indirizzo'
            - 'email'
            'telefono'
        Comportamento:
            - Crea un nuovo file Excel con intestazioni e dati.
            - Sovrascrive eventuali file con lo stesso nome.
        """
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Persone"
        # Scrive l'intestazione
        sheet.append(["Nome", "Cognome", "Indirizzo", "Email", "Telefono"])
        # Scrive i dati
        for person in data:
            sheet.append([person["nome"], person["cognome"], person["indirizzo"],person["email"], person["telefono"]])
        # Salva il file
        workbook.save(self.filename)
        print(f"✅ File Excel salvato come {self.filename}")

    def read_from_excel(self):
        """
        Legge e stampa a video il contenuto del file Excel riga per riga.
        Comportamento:
            - Verifica l'esistenza del file.
            - Legge il file con Pandas.
            - Stampa ogni riga.
        """
        if not os.path.exists(self.filename): # verifica se esiste il file Excel
            print(f"⚠️ Il file Excel {self.filename} non esiste.")
            return
        try:
            df = pd.read_excel(self.filename, dtype=str)
            df.columns = [col.strip() for col in df.columns]
            if not df.empty:
                print("\n--- Contenuto del File Excel ---")
                for index, row in df.iterrows():
                    print(f"{index + 1}, {tuple(row)}")
            else:
                print("⚠️ Il file Excel è vuoto.")
        except Exception as e:
            print(f"❌ Errore durante la lettura del file Excel: {e}")

    def compare_excel_with_sql(self, db_name="persone.db"):
        """
        Confronta i dati tra il file Excel e la tabella SQLite 'persone'.
        Args:
            db_name (str): Nome del database SQLite da confrontare.
        Comportamento:
            - Normalizza i nomi delle colonne.
            - Stampa le righe presenti solo in Excel o solo nel DB.
        """
        try:
            #controlla l'esistenza del database
            if not os.path.exists(db_name):
                print(f"⚠️ Il file {db_name} non esiste, impossibile confrontare con Excel.")
                return

            df_excel = pd.read_excel(self.filename, dtype=str)
            df_excel.columns = [col.strip() for col in df_excel.columns]
            conn = sqlite3.connect(db_name)
            df_db = pd.read_sql_query("SELECT * FROM persone", conn)
            df_db.columns = [col.strip() for col in df_db.columns]

            # Normalizza le colonne in minuscolo per confronto robusto
            df_excel.columns = [col.lower() for col in df_excel.columns]
            df_db.columns = [col.lower() for col in df_db.columns]
            missing_cols = [col for col in df_excel.columns if col not in df_db.columns]

            if missing_cols:
                print(f"⚠️ Attenzione: le seguenti colonne non sono presenti nel DB: {missing_cols}")
                return

            df_db = df_db[df_excel.columns]
            only_in_excel = pd.concat([df_excel, df_db, df_db]).drop_duplicates(keep=False)
            only_in_db = pd.concat([df_db, df_excel, df_excel]).drop_duplicates(keep=False)
            print("\n📄 Righe presenti solo in Excel:")
            print(only_in_excel)
            print("\n📄 Righe presenti solo nel DB:")
            print(only_in_db)

        except Exception as e:
            print(f"❌ Errore durante il confronto: {e}")

        finally:
            if 'conn' in locals():
                conn.close()

    def delete_excel_and_db(self, db_filename="persone.db"):
        """
        Elimina sia il file Excel che il database SQLite, se esistono.
        Args:
            db_filename (str): Nome del database SQLite da eliminare.
        Comportamento:
            - Elimina il file Excel se esiste.
            - Tenta di chiudere eventuali connessioni SQLite prima di rimuovere il file.
            - Gestisce errori e avvisi.
        """
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
                print(f"✅ File {self.filename} eliminato con successo.")
            else:
                print(f"⚠️ File {self.filename} non trovato.")

            if os.path.exists(db_filename):
                try:
                    # Tentativo di chiudere eventuali connessioni residue prima dell'eliminazione
                    try:
                        conn = sqlite3.connect(db_filename)
                        conn.close()
                    except Exception as e:
                        print(f"❌ Impossibile chiudere connessione residua: {e}")

                    os.remove(db_filename)
                    print(f"✅ File {db_filename} eliminato con successo.")
                except PermissionError as pe:
                    print(f"❌ Errore: il file {db_filename} è ancora in uso. Chiudi tutti i programmi che lo utilizzano e riprova.")
                except Exception as inner_e:
                    print(f"❌ Errore durante l'eliminazione di {db_filename}: {inner_e}")
            else:
                print(f"⚠️ File {db_filename} non trovato.")
        except Exception as e:
            print(f"❌ Errore durante l'eliminazione dei file: {e}")