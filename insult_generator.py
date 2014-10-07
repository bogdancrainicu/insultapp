class Insulter:
    def __init__(self, choice):
        self.choice = choice

    def insult(self):
        return "Though {}!".format(self._generate_insult())

    def named_insult(self, name):
        return "{0}, though {1}".format(name.capitalize(), self._generate_insult())

    def _generate_insult(self):
        return "{0} {1} {2}".format(
            self.choice(["artless", "foolish", "festering"]),
            self.choice(["bat-fowling", "boil-brained", "beetle-headed"]),
            self.choice(["barnacle", "bladder", "boar-pig"])
        )

