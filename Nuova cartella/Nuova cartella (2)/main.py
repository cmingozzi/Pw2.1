from database import SQLiteWriter
from excel import ExcelWriter
from generator import DataGenerator


if __name__ == "__main__":

    # Inizializzazione Excel
    excel_writer = ExcelWriter()

    # Inizializzazione Sqlite
    sqlite_writer = SQLiteWriter()

    # Lista che conterrà i dati generati
    persone = []

    while True:
        print("\n--- MENU ---")
        print("1. Genera 10 persone casuali")
        print("2. Salva persone su Excel")
        print("3. Copia dati Excel su database Sql")
        print("4. Stampa persone dal database")
        print("5. Stampa persone dal file Excel")
        print("6. Confronta i file Excel e Sql e stampa entrambi")
        print("7. Elimina tutte le persone dal database sql")
        print("8. Elimina file excel e sql")
        print("9. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
           # Genera dati
            generator = DataGenerator(count=10)
            persone = generator.generate_data()
            print(f"✅ Sono state generate {len(persone)} persone.")

        elif scelta == "2":
            if persone:
                excel_writer.write_to_excel(persone)
            else:
                print("⚠️ Prima devi generare delle persone!")

        elif scelta == "3":
            if excel_writer.excel_exists():
                sqlite_writer.delete_all_data()
                sqlite_writer.create_table()
                excel_writer.read_from_excel_and_insert_to_sql()
                print("✅ Dati copiati da Excel a database SQLite.")
            else:
                print("⚠️ Prima devi generare il file excel!")

        elif scelta == "4":
            sqlite_writer.read_from_db()

        elif scelta == "5":
            excel_writer.read_from_excel()

        elif scelta == "6":
            if excel_writer.excel_exists():
                if sqlite_writer.db_exists():
                    excel_writer.compare_excel_with_sql()
                    print("\n📌 Contenuto Excel:")
                    excel_writer.read_from_excel()
                    print("\n📌 Contenuto Database:")
                    sqlite_writer.read_from_db()
                else:
                    print("⚠️ Prima devi generare il file Sql!")
            else:
               print("⚠️ Prima devi generare il file excel!")

        elif scelta == "7":
           sqlite_writer.delete_all_data()

        elif scelta == "8":
            excel_writer.delete_excel_and_db()

        elif scelta == "9":
            print("✅ Programma terminato.")
            break

        elif scelta == "10":
            if excel_writer.excel_exists():
                excel_writer.crypto_excel()
            else:
                print("⚠️ Prima devi generare il file Excel!")

        elif scelta == "11":
            excel_writer.decrypto_excel()

        elif scelta == "12":
            sqlite_writer.crypto_db()

        elif scelta == "13":
            sqlite_writer.decrypto_db()

        elif scelta == "14":
            excel_writer.compare_encrypted_excel_db()

        else:
            print("⚠️ Scelta non valida, riprova.")
