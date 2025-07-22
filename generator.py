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
            email = nome.lower() + "." + cognome.lower() +"@" + self.fake.free_email_domain()
            person = {
                "nome": nome,
                "cognome": cognome,
                "indirizzo": self.fake.address(),
                "email": email,
                "telefono": self.fake.phone_number(),
            }
            data.append(person)
        return data