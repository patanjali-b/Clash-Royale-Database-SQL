# SQL Operations with Descriptions

## Insert Operations
- `add_players(user_name, email, trophies, level, clan_id, highest_trophies)`: Inserts a new player into the database.
- `add_cards(card_id, hp, damage, elixit, level, rarity)`: Adds a new card entry with its attributes.
- `add_clan(ClanID, Clan_Name, Clan_Trophies, Description, Clan_Leader)`: Inserts a new clan with relevant details.
- `add_deck(player_id, card1, card2, card3, card4, deck_name)`: Adds a new deck associated with a player.

## Delete Operations
- `delete_card(card_id)`: Removes a specific card from the database.
- `del_clan(ClanID)`: Deletes a clan based on the ClanID.
- `del_player(PlayerID)`: Removes a player from the database.
- `del_battle(BattleID)`: Deletes a battle record based on BattleID.

## Update Operations
- `update_card(CardID, new_level)`: Updates a card's level to a new value.
- `update_email(PlayerID, new_email)`: Modifies a player's email address with a new one.
- `update_clan_leader(ClanID, PlayerID)`: Updates the leader of a clan to a new player.
- `change_clan(PlayerID, ClanID)`: Changes a player's associated clan.
- `inc_player_trophies(WinnerID)`: Increases trophies for a winning player.
- `dec_player_trophies(LoserID)`: Decreases trophies for a losing player.

## Selection Operations
- `select_player(player_name)`: Retrieves player details by their name.
- `select_card(card_id)`: Retrieves card details using the card's ID.
- `select_clan(clan_name)`: Fetches clan information based on the clan's name.
- `select_deck(deck_id)`: Retrieves a player's deck by its ID.

## Projection Operations
- `select_player_above_trophies(trophies, clan_name)`: Retrieves players above a certain trophy count within a specific clan.
- `select_cards_deck(hp, deck_id)`: Fetches cards' hitpoints within a particular deck.

## Aggregate Operations
- `count_players(clan_name)`: Counts the number of players in a specific clan.
- `avg_trophies_clan(clan_name)`: Calculates the average trophies for a particular clan.

## Search Operations
- `search_player(player_name)`: Searches for a player by their name.
- `search_clan(clan_name)`: Searches for a clan by its name.

## Analysis Operations
- `success_rate(player_id)`: Calculates the success rate of a player based on their battles.
