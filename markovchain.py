import json
from random import choices


class MarkovChain:
    def __init__(self, file):
        data = json.load(file)             # get json describing weighted graph
        self.leads = data["leads"]         # distribution of starting words
        self.follows = data["follows"]     # distribution of possible following words

        # print(f"Leads: {self.leads}")
        # print(f"follows: {self.follows}")

    # check if word definition already exists in dictionary
    # increment if so, else, define it
    @staticmethod
    def add(d, word):
        if word in d:
            d[word] += 1
        else:
            d[word] = 1

    def add_data(self, string):
        words = string.replace('\n', '').split(" ")  # sanitise and convert to array of words

        for count, word in enumerate(words):
            if word not in self.follows:
                self.follows[word] = {}  # make new node in graph if doesn't exist

            if count == 0:
                self.add(self.leads, word)  # increment/define starting word
            else:
                self.add(self.follows[words[count-1]], word)  # increment/define under previous word in string

    def export(self, filename="out"):
        with open(f"{filename}.json", "w+", encoding="utf-8") as f:
            f.write(json.dumps({"leads": self.leads, "follows": self.follows}, indent=4))

    def get_start(self):
        return choices(list(self.leads.keys()), weights=list(self.leads.values()))[0]

    def get_next(self, word):
        next_words = list(self.follows[word].keys())
        return choices(next_words, weights=list(self.follows[word].values()))[0]

    def generate(self, max_count=100):
        current = self.get_start()
        sentence = current

        count = 0
        while self.follows[current] != {} and count <= max_count:
            current = self.get_next(current)
            sentence += " " + current
            count += 1

        return sentence
