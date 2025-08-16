"""
Modulo principale per l'interazione con il sistema di gestione dati personali.

Consente di:
- Generare persone casuali o inserire dati manualmente.
- Salvare i dati in un file Excel o in un database SQLite.
- Visualizzare, criptare, decriptare e confrontare i dati tra Excel e SQLite.
- Eliminare i file generati.

Il menu guida l'utente passo-passo attraverso tutte le funzionalità offerte.

Moduli necessari:
- generator.py: Generazione dati casuali o manuali
- excel.py: Scrittura/lettura/confronto file Excel e genera dal file Excel un database SQLite contenente gli stessi dati
- database.py: Scrittura/lettura/confronto database SQLite
"""
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
        print("2. Inserisci manualmente nominativi simulando richiesta autorizzazione")
        print("3. Salva persone su Excel")
        print("4. Copia dati Excel su Database Sql")
        print("5. Stampa persone dal Database")
        print("6. Stampa persone dal file Excel")
        print("7. Confronta i file Excel e Sql e stampa entrambi")
        print("8. Cripta file excel")
        print("9. Cripta database")
        print("10. Decripta file Excel")
        print("11. Decripta database")
        print("12. Elimina file Excel e Database")
        print("13. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
           # Genera dati casuali
            generator = DataGenerator(count=10)
            persone = generator.generate_data()
            print(f"✅ Sono state generate {len(persone)} persone.")

        elif scelta == "2":
            # Genera dati facendoli inserire manualmente all'utente
            generator = DataGenerator()
            persone = generator.generate_manual_person()

        elif scelta == "3":
            # Genera file excel con dati generati
            if persone:
                excel_writer.write_to_excel(persone)
            else:
                print("⚠️ Prima devi generare delle persone!")

        elif scelta == "4":
            # Importa i dati contenuti nel file excel in un Database
            sqlite_writer.read_from_excel_and_insert_to_sql()

        elif scelta == "5":
            # Stampa contenuto file db
            sqlite_writer.read_from_db()

        elif scelta == "6":
            # Stampa contenuto file excel
            excel_writer.read_from_excel()

        elif scelta == "7":
            # Confronta il contenuto del file excel e del file db, stampe le eventuali differenze ed entrambi i contenuti
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

        elif scelta == "8":
            excel_writer.crypto_excel()

        elif scelta == "9":
            sqlite_writer.crypto_db()

        elif scelta == "10":
            excel_writer.decrypto_excel()

        elif scelta == "11":
            sqlite_writer.decrypto_db()

        elif scelta == "12":
            excel_writer.delete_excel_and_db()

        elif scelta == "13":
            print("✅ Programma terminato.")
            break

        else:
            print("⚠️ Scelta non valida, riprova.")
