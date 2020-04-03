import pandas
import numpy as np

card_counts = np.array([[22, 28, 36, 44],
                        [21, 27, 35, 43],
                        [21, 27, 35, 43]])

age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

print(age1_cards.at['Troll', 'Card Type'])
