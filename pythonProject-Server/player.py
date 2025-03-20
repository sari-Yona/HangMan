class Player:
    def __init__(self, name, Id, password):
        self.name = name
        self.Id = Id
        self.password = password
        self.gamesNum = 0
        self.words = set()
        self.win = 0

    def __str__(self):
        return f"name:{self.name},Id:{self.Id},password:{self.password},gamesNum:{self.gamesNum},words:{'{'+' '.join(self.words) + '}'},win:{self.win}"
