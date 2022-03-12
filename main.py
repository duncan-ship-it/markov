from markovchain import MarkovChain


def main():
    markov = MarkovChain(open("data.json", "r"))

    strings = open("input.txt", "r", encoding="utf-8").readlines()

    [markov.add_data(string) for string in strings]

    # markov.export("data")  # save graph as data.json

    print(markov.generate())


main()
