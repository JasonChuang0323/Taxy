class User:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

    def __repr__(self):
        return f"<User id={self.id} name={self.name} address={self.address}>"