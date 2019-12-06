from afinn import Afinn


afinn = Afinn()

def sentiment(sentence):
    return afinn.score(sentence)

if __name__ == '__main__':
    with open("test_sent.txt", "r") as f:
        for i, line in enumerate(f):
            print(f"{sentiment(line)} {line}")