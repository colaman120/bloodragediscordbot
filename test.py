import pandas
import numpy as np

card_counts = np.array([[22, 28, 36, 44],
                        [21, 27, 35, 43],
                        [21, 27, 35, 43]])

player_list = [0, 0, 0, 0]

def gen_hands(age: int):
    numbers = np.arange(card_counts[age - 1][len(player_list) - 2])
    to_return = np.random.choice(numbers, size=(len(player_list), 8), replace=False)
    return to_return.tolist()

def remove_cards():
    global cards, draft
    for i in range(np.size(cards, 0)):
        cards[i] = np.roll(cards[i], cards[i].size - np.where(cards[i] == draft[i])[0][0])

    cards = np.delete(cards, 0, 1)

temp = gen_hands(1)

a = [[0, 0], [0, 0]]
print(len(a))
print(temp)
print(type(temp))
