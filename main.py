from database import SQLiteWriter
from excel import ExcelWriter
from generator import DataGenerator



if __name__ == "__main__":
    # Genera dati
    generator = DataGenerator(count=10)
    # Inizializzazione database SQLite
    sqlite_writer = SQLiteWriter()
    sqlite_writer.create_table()
    # Inizializzazione Excel
    excel_writer = ExcelWriter()

    # Lista che conterrà i dati generati
    persone = []

    while True:
        print("\n--- MENU ---")
        print("1. Genera persone casuali")
        print("2. Salva persone su Excel")
        print("3. Salva persone su SQLite")
        print("4. Leggi persone dal database")
        print("5. Elimina tutte le persone dal database")
        print("9. Esci")
        print("10 Excel to Sql")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            persone = generator.generate_data()
            print(f"Sono state generate {len(persone)} persone.")

        elif scelta == "2":
            if persone:
                excel_writer.write_to_excel(persone)
            else:
                print("Prima devi generare delle persone!")

        elif scelta == "3":
            if persone:
                sqlite_writer.write_to_db(persone)
            else:
                print("Prima devi generare delle persone!")

        elif scelta == "4":
            sqlite_writer.read_from_db()

        elif scelta == "5":
            if persone:
                sqlite_writer.delete_all_data()
            else:
                print("Prima devi generare delle persone!")

        elif scelta == "9":
            print("Programma terminato.")
            sqlite_writer.close()
            break

        elif scelta == "10":
            excel_writer.read_from_excel_and_insert_to_sql()

        else:
            print("Scelta non valida, riprova.")



