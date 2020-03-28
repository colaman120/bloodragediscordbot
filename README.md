# Blood Rage Bot
This bot facilitates the play of Blood Rage, a game by Eric M. Lang and published by CMON Limited.
Currently, the bot can only assist in playing the game by allowing players to join and draft cards
for each age. Someone must own the board game and by able to display the game through camera in
order to play this game.

Please keep in mind that I started this like this week and it's my first time creating a bot.
I'm still in the process of fixing and adding a lot of things.

### Commands:
!join_game: This is the command that allows discord users to enter the ongoing game. Anyone that
wants to join must type this command. Keep in mind that this game only plays 2-4 (5 if you own the
expansion.)

!show_players: This command shows all players currently signed up for the game.

!clear_game: This command clears every player from the player list.

!start_age (age_number): This command begins the draft based on the number of players currently signed
up and the age that is input in the command. Without the age, it will not run.

!draft (card_number): Upon using the !start_age command, the bot will dm each player signed up and
send each a list of cards and the number associated to the card. The player must then respond to
the bot with the !draft command followed by the number of the card that they want to draft. After
all players have done so, the bot will automatically move the cards between players so that drafting
can continue. Please note that the special drafting case for 2 players has yet to be implemented, and
it will not work should you try to do anything about it.

All rights for the board game go to CMON Limited and Eric M Lang or however it works.

Bot created on 3/20/2020 during the Covid-19 panic.
