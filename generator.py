from faker import Faker

class DataGenerator:
   def __init__(self, count=10):
        self.fake = Faker("it_IT")
        self.count = count

   def generate_data(self):

        data = []

        for _ in range(self.count):
            nome = self.fake.first_name()
            cognome = self.fake.last_name()
            email = self.fake.free_email()
            # nome.lower() + "." + cognome.lower() +"@" + self.fake.free_email_domain()
            person = {
                "nome": nome,
                "cognome": cognome,
                "indirizzo": self.fake.address(),
                "email": email,
                "telefono": self.fake.phone_number(),
            }
            data.append(person)
        return data

   def _inserisci_persona(self):
        """
        Chiede all'utente di inserire manualmente i campi per una persona.
        """
        person = {}
        campi = ["nome", "cognome", "indirizzo", "email", "telefono"]
        print("\n👤 Inserisci i dati della persona:\n")
        for campo in campi:
            valore = input(f"Inserisci {campo}: ").strip()
            person[campo] = valore
        return person

   def generate_manual_person(self):
       """
       Consente l'inserimento manuale di una o più persone.
       Chiede autorizzazione per ogni persona.
       Ritorna una lista di dizionari con i dati inseriti.
       """
       data = []

       while True:
           # Ripeti la richiesta fino a risposta valida
           autorizza = ""
           while autorizza not in ["s", "n"]:
               autorizza = input("\n🔒 Autorizzi l'inserimento dei dati per una persona? (S/N): ").strip().lower()
               if autorizza not in ["s", "n"]:
                    print("⚠️ Scelta non valida. Inserisci 'S' per sì o 'N' per no.")

           if autorizza == "s":
               person = self._inserisci_persona()
               data.append(person)
               print("✅ Persona aggiunta.")
           else:
               print("❌ Inserimento non autorizzato.")
               break

           # Anche qui: validazione dell'input per continuare
           continua = ""
           while continua not in ["s", "n"]:
               continua = input("\n❓ Vuoi inserire un'altra persona? (S/N): ").strip().lower()
               if continua not in ["s", "n"]:
                    print("⚠️ Scelta non valida. Inserisci 'S' per sì o 'N' per no.")
               elif continua == "n":
                   print("ℹ️ Inserimento manuale terminato.")
                   return data
               elif continua == "s":
                   break  # Torna all'inizio del ciclo

       return data