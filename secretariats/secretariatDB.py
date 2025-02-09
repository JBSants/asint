import pickle

class Secretariat:
    def __init__(self, id, location, name, description, opening_hours):
        self.id = id
        self.location = location
        self.name = name
        self.description = description
        self.opening_hours = opening_hours

class SecretariatDB:
    dumpFile = "secretariatDump.db"
    def __init__(self):
        try:
            f = open(self.dumpFile, 'rb')
            self.secretariats = pickle.load(f)
            f.close()
        except IOError:
            self.secretariats = {}

    def dump(self):
        f = open(self.dumpFile, 'wb')
        pickle.dump(self.secretariats, f)
        f.close()

    def getAll(self):
        return self.secretariats.values()

    def get(self, id):
        try:
            return self.secretariats[id]
        except:
            return None

    def create(self, location, name, description, opening_hours):
        new_id = str(len(self.secretariats)) #TODO: change id cretion
        self.secretariats[new_id] = Secretariat(new_id, location, name, description, opening_hours)
        self.dump()
        return self.secretariats[new_id]

    def remove(self, id):
        try:
            del self.secretariats[id]
            self.dump()
            return True
        except:
            return False