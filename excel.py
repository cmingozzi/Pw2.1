from openpyxl import Workbook

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