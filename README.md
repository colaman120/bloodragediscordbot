# Blood Rage Bot
This bot facilitates the play of Blood Rage, a game by Eric M. Lang and published by CMON Limited.
Currently, the bot can only assist in playing the game by allowing players to join and draft cards
for each age. Someone must own the board game and by able to display the game through camera in
order to play this game.

Please keep in mind that I started this like this week and it's my first time creating a bot.
I'm still in the process of fixing and adding a lot of things.

#### Update (6/18/2020)
Wow. This bot came a long way. I put it down for a bit to focus on schoolwork but when summer break came it was all hands on deck. 

### General Commands:
**!join**: Allows discord users to enter the ongoing game. Anyone that wants to join must type this command. 

>Blood Rage
>>Keep in mind that this game only plays 2-4 (5 if you own the expansion.) (This bot does support the expansion, so yes, you can play with 5 players. However, it does not support the gods).

**!show_players**: Shows all players currently signed up for the game.

**!clear_game**: Clears every player from the player list.

**!add_score**: Increases or decreases the score of the player inputting the command. To decrease your score, simply enter a negative number.

**!show_score**: Displays the scores of all players currently in the game.

**!remove_player (username, discriminator)**: Allows any person to remove a player from the game. The parameters include username and discriminator, which are the name of the account and the numbers following the name, not including the #. 

**!add_stat (stat, delta)**: Increases or decreases the stat based on the stat that you input, the game that you are currently playing, and the delta input into the commands' parameters.

**!get_stats**: Displays the message author's stats.

**!get_hand**: Displays the message author's hand. If your hand is something that should be kept private, simply dm the bot and the bot will dm you back your hand, thus not allowing the information to be exposed.

**!show_board_image**: Shows an image of the board of the current game.

**!show_board**: Displays the most vital information of the board in a condensed form to make for ease of reading.

#### Blood Rage Specific:
**!create_br**: Sets the game to a Blood Rage game.

**!start_age (age_number)**: Begins the age based on the number of players currently signed up and the age that is input in the command.

**!draft (card_number)**: Upon using the !start_age command, the bot will dm each player signed up and send each a list of cards and the number associated to the card. The player must then respond to the bot with the !draft command followed by the number of the card that they want to draft. After all players have done so, the bot will automatically move the cards between players so that drafting can continue. Please note that the special drafting case for 2 players has yet to be implemented, and it will not work should you try to do anything about it.

**!set_upgrade (age, card, slot)**: Given the age and the card number of the upgrade card, as well as the desired slot to place the card in, this method gives the player the advantages of the upgrade card. Note that for warrior, leader, and ship upgrade cards, any number can be put into the slot parameter as this parameter is useless in those cases.

**!view_upgrades**: Shows the upgrades that you have played in the slot order that you have placed them

**!rag_check**: Randomly generates the next three provinces to ragnorok based on the provinces that were not ragnoroked to begin the game. Note that this is not consistent, so run the method once to begin and remember or record these provinces.

**!card (age, card)**: Given the age of the card and the card number, the bot will output all of the information about the card, excluding the picture.

**!remove_card (age, card)**: Removes a card from a player's hand given the age and the card number.

**!summon (unit, province)**: Summons the given unit in the given province, provided that both exist. Note that if the unit has a space in its name, i.e, Sea Serpent, the unit name must be put in quotation marks.

**!kill_piece (unit, province)**: Kills a unit given the unit name and province.

**!move (unit, num, province_from, province_to)**: Moves a number of units of the given name from one province to the other.

**!show_province (province)**: Shows all the details of a given province.

**!pillage_rewards**: Displays the pillage rewards for all provinces except for Yggdrasil.

**!add_rage (delta)**: Allows players to change their current rage counter.

**!get_rage**: Displays your current rage

**!get_quests:**: Displays the quests that you currently have in play.

**!set_quest (age, card)**: Play a quest based on the age of the card and its number.

**!ragnorok (province)**: Ragnoroks a province. This command should generally not be used and instead players should simply use the end_round method. However, if players do not trust me for whatever reason and wish to take more control, this will simply kill all of the units in a province and give glory per death.

**!end_round (province)**: Ends the current age given the province that is to be ragnoroked. This covers checking quests, ragnorok, and release of valhalla. It does not cover the addition of glory due to cards like Loki's Domain.

All rights for the board game go to CMON Limited and Eric M Lang or however it works.

Bot created on 3/20/2020 during the Covid-19 panic.

