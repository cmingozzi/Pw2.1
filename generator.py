from faker import Faker

class DataGenerator:
    """
    Classe per generare dati (nome, cognome, indirizzo, email, telefono),
    sia automaticamente tramite la libreria Faker, sia manualmente tramite input da terminale.
    Attributi:
        count (int): Numero di persone da generare automaticamente.
        fake (Faker): Istanza di Faker configurata per la localizzazione italiana ("it_IT").
    """

    def __init__(self, count=10):
        """
        Inizializza la classe DataGenerator con il numero di persone da generare.
        Args:
            count (int, optional): Numero di persone da generare automaticamente. Default = 10.
        """
        self.fake = Faker("it_IT")
        self.count = count

    def generate_data(self):
        """
        Genera una lista di dizionari contenenti dati casuali di persone con indirizzi italiani.
        Returns:
           list[dict]: Una lista di `count` elementi. Ogni dizionario contiene:
           'nome': Nome della persona
           'cognome': Cognome della persona
           'indirizzo': Indirizzo completo in formato "<via> <numero>, <CAP> <città> <provincia>"
           'email': Indirizzo email fittizio
           'telefono': Numero di telefono fittizio
        """
        data = []

        for _ in range(self.count):
            nome = self.fake.first_name()
            cognome = self.fake.last_name()
            via = self.fake.street_name()
            numero = self.fake.building_number()
            cap = self.fake.postcode()
            città = self.fake.city()
            provincia = self.fake.state_abbr()
            email = self.fake.free_email()

            person = {
                "nome": nome,
                "cognome": cognome,
                "indirizzo": f"{via} {numero}, {cap} {città} {provincia}",
                "email": email,
                "telefono": self.fake.phone_number(),
            }
            data.append(person)
        return data

    def _inserisci_persona(self):
        """
        Chiede all'utente di inserire manualmente i campi per una persona.
        Returns:
            dict: Un dizionario contenente i dati inseriti manualmente nei campi corretti.
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
        Permette l'inserimento manuale interattivo di una o più persone tramite terminale.
        Per ogni persona:
        - Viene chiesta l'autorizzazione all'inserimento.
        - Se autorizzato, viene chiamato il metodo interno`_inserisci_persona()` per inserire i dati.
        - Dopo ogni inserimento, viene chiesto se si vuole continuare o terminare.
        Returns:
          list[dict]: Una lista di dizionari, ciascuno contenente i dati di una persona
          inserita manualmente. Se non viene autorizzato alcun inserimento, ritorna una lista vuota.
       """
       data = []

       while True:
           # Ripete la richiesta fino a risposta valida
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