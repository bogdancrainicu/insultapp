class Insulter:

    def __init__(self):
        pass

    def insult(self):
        return "Though {}!".format(self._generate_insult())

    def named_insult(self, name):
        return "{0}, though {1}".format(name.capitalize(), self._generate_insult())

    def _generate_insult(self):
        return "banana"

