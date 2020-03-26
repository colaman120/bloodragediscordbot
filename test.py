import pandas
age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
print(age1_cards)

print(age1_cards.at[5, 'Name'])
