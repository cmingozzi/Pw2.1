import os
import sqlite3
import pandas as pd
from openpyxl import Workbook
from cryptography.fernet import Fernet


class ExcelWriter:
    def __init__(self, filename = "persone.xlsx"):
        self.filename = filename

    def crypto_excel(self, path_key="key.key"):
        """
        Crittografa il file Excel self.filename e salva il file crittografato con estensione .enc.
        Chiede se eliminare il file Excel originale al termine.
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
        scelta = input(f"❓ Vuoi eliminare il file Excel originale {self.filename}? (S/N): ").strip().lower()
        if scelta == "s":
            try:
                os.remove(self.filename)
                print(f"🗑️ File {self.filename} eliminato.")
            except Exception as e:
                print(f"❌ Errore durante l'eliminazione di {self.filename}: {e}")
        else:
            print(f"ℹ️ Il file {self.filename} è stato mantenuto.")

    def decrypto_excel(self, path_key="key.key"):
        """
        Decrittografa il file Excel .enc e ricrea il file Excel originale.
        Chiede se eliminare il file .enc al termine.
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

        with open(encrypted_filename, "rb") as enc_file:
            encrypted = enc_file.read()

        try:
            decrypted = fernet.decrypt(encrypted)
        except Exception as e:
            print(f"❌ Errore nella decrittografia: {e}")
            return

        with open(self.filename, "wb") as dec_file:
            dec_file.write(decrypted)

        print(f"✅ File decrittografato e salvato come {self.filename}")

        # Chiede se eliminare il file .enc
        scelta = input(f"❓ Vuoi eliminare il file crittografato {encrypted_filename}? (S/N): ").strip().lower()
        if scelta == "s":
            try:
                os.remove(encrypted_filename)
                print(f"🗑️ File {encrypted_filename} eliminato.")
            except Exception as e:
                print(f"❌ Errore durante l'eliminazione di {encrypted_filename}: {e}")
        else:
            print(f"ℹ️ Il file {encrypted_filename} è stato mantenuto.")

    def excel_exists(self):
        """Controlla se il file Excel esiste"""
        return os.path.exists(self.filename)

    def write_to_excel(self, data):
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
        if not os.path.exists(self.filename):
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

    def read_from_excel_and_insert_to_sql(self, db_name="persone.db"):
        try:
            # Legge il file Excel
            df = pd.read_excel("persone.xlsx", sheet_name=0, dtype=str)

            # Rinomina colonne rimuovendo eventuali spazi invisibili
            df.columns = [col.strip() for col in df.columns]

            # Costruisce la query CREATE TABLE dinamica
            table_name = "persone"
            columns_sql = ", ".join([f'"{col}" TEXT' for col in df.columns])
            create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});'

            # Connessione al database
            conn = sqlite3.connect("persone.db")
            cursor = conn.cursor()

            # Crea la tabella con struttura identica all'Excel
            cursor.execute(create_table_sql)

            # Inserisce i dati in SQL
            df.to_sql("persone", conn, if_exists="append", index=False)

            conn.commit()
            conn.close()

            print(f"✅ Dati importati con successo in {db_name}")

        except Exception as e:
            print(f"❌ Errore durante la lettura/inserimento: {e}")

    def compare_excel_with_sql(self, db_name="persone.db"):
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
                    #FileUtils.force_close_file('persone.db')
                except Exception as inner_e:
                    print(f"❌ Errore durante l'eliminazione di {db_filename}: {inner_e}")
            else:
                print(f"⚠️ File {db_filename} non trovato.")
        except Exception as e:
            print(f"❌ Errore durante l'eliminazione dei file: {e}")