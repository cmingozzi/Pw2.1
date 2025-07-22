import os
import sqlite3
import pandas as pd

from openpyxl import Workbook, load_workbook


class ExcelWriter:
    def __init__(self, filename = "persone.xlsx"):
        self.filename = filename

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
        print(f"File Excel salvato come {self.filename}")

    def read_from_excel_and_insert_to_sql(self, db_name="persone.sql"):
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
            conn = sqlite3.connect("persone.sql")
            cursor = conn.cursor()

            # Crea la tabella con struttura identica all'Excel
            cursor.execute(create_table_sql)

            # Inserisce i dati in SQL
            df.to_sql("persone", conn, if_exists="append", index=False)

            conn.commit()
            conn.close()

            print("Dati importati con successo.")

            # print(f"Dati importati correttamente in {db_name}")

        except Exception as e:
            print(f"Errore durante la lettura/inserimento: {e}")

        finally:
            conn.close()
