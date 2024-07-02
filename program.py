import subprocess as sp
import getpass
import questionary
import random
import pymysql
from pprint import pprint
import datetime
# function to add new players


def add_players(user_name, email, trophies, level, clan_id, highest_trophies):
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the maximum PlayerID from the Player table
        cursor.execute("SELECT MAX(PlayerID) FROM Player;")
        result = cursor.fetchone()
        key = list(result.keys())[0]
        max_player_id = result[key]
        # Increment the maximum PlayerID to generate a new ID
        new_player_id = max_player_id + 1

        # SQL query to insert data into the Player table
        query = """
            INSERT INTO Player (PlayerID, User_Name, Date_Of_Join, Email, Current_Trophies, Level, ClanID, Highest_Trophies)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Tuple with the values for the query
        values = (new_player_id, user_name, date, email,
                  trophies, level, clan_id, highest_trophies)

        # Execute the query and commit the changes
        cursor.execute(query, values)
        con.commit()
        pprint("Player added successfully")

    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def add_cards(card_id, hp, damage, elixit, level, rarity):
    # check if card_id
    try:
        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (card_id))
        result = cursor.fetchone()
        if result is None:
            query = """
            INSERT INTO Cards (CardID, Card_Base_Hitpoints, Card_Base_Damage, Elixir_Cost, Card_Level, Card_Rarity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
            values = (card_id, hp, damage, elixit, level, rarity)
            cursor.execute(query, values)
            con.commit()
            pprint("Card added successfully")
        else:
            pprint("Card already exists")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def delete_card(card_id):
    try:
        # SQL query to delete a player from the Player table
        query = """
            DELETE FROM Cards
            WHERE CardID = %s
        """

        # Tuple with the value for the query
        values = (card_id)

        # Execute the query and commit the changes
        cursor.execute(query, values)
        con.commit()
        pprint("Card deleted successfully")

    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def add_clan(ClanID, Clan_Name, Clan_Trophies, Description, Clan_Leader):
    try:
        # check if the Clan_Leader is in the Player table, if not, show error
        cursor.execute(
            "SELECT * FROM Player WHERE User_Name = %s", (Clan_Leader))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan Leader not found")
            return
        cursor.execute("SELECT * FROM Clan WHERE ClanID = %s", (ClanID))
        result = cursor.fetchone()
        if result is None:
            query = """
            INSERT INTO Clan (ClanID, Clan_Name, Clan_Trophies, Description, Clan_Leader)
            VALUES (%s, %s, %s, %s, %s)
        """
            values = (ClanID, Clan_Name, Clan_Trophies,
                      Description, Clan_Leader)
            cursor.execute(query, values)
            con.commit()
            pprint("Clan added successfully")
        else:
            pprint("Clan already exists")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return

# add deck
def avg_tenure(clan_name):
    try:
        # Join Clan and Player tables, calculate average tenure
        query = """
            SELECT
                Clan.Clan_Name,
                AVG(DATEDIFF(CURDATE(), Player.Date_Of_Join)) AS AverageTenure
            FROM
                Player
            INNER JOIN
                Clan ON Player.ClanID = Clan.ClanID
            WHERE
                Clan.Clan_Name = %s
            GROUP BY
                Clan.Clan_Name;
        """

        cursor.execute(query, (clan_name,))
        result = cursor.fetchone()

        if result is None:
            print("Clan not found")
            return

        clan_name, average_tenure = result
        pprint(f"Clan: {clan_name}, Average Tenure: {(average_tenure, 2)} days")

    except pymysql.Error as err:
        print(f"Error: {err}")

    return

def add_deck(player_id, card1, card2, card3, card4, deck_name):
    # forst check if player and all the cards exist
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (player_id))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (card1))
        result = cursor.fetchone()
        if result is None:
            pprint("Card1 not found")
            return
        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (card2))
        result = cursor.fetchone()
        if result is None:
            pprint("Card2 not found")
            return
        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (card3))
        result = cursor.fetchone()
        if result is None:
            pprint("Card3 not found")
            return
        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (card4))
        result = cursor.fetchone()
        if result is None:
            pprint("Card4 not found")
            return
        # get max deck id
        cursor.execute("SELECT MAX(DeckID) FROM Deck;")
        result = cursor.fetchone()
        key = list(result.keys())[0]
        max_deck_id = result[key]
        # Increment the maximum PlayerID to generate a new ID
        new_deck_id = max_deck_id + 1
        # inset into deck, DeckID, PlayerID, Deck_name;
        query = """
            INSERT INTO Deck (DeckID, PlayerID, Deck_name)
            VALUES (%s, %s, %s)
        """
        values = (new_deck_id, player_id, deck_name)
        cursor.execute(query, values)
        con.commit()
        # now add deck_id, Card1_ID, Card2_ID, Card3_ID, Card4_ID into Deck_Cards
        query = """
            INSERT INTO Deck_Cards (DeckID, Card1_ID, Card2_ID, Card3_ID, Card4_ID)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (new_deck_id, card1, card2, card3, card4)
        cursor.execute(query, values)
        con.commit()
        pprint("Deck added successfully")

    except pymysql.Error as err:
        pprint(f"Error: {err}")


def del_clan(ClanID):
    try:
        cursor.execute("SELECT * FROM Clan WHERE ClanID = %s", (ClanID))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
            return
        query = """
            DELETE FROM Clan WHERE ClanID = %s
        """
        cursor.execute(query, (ClanID))
        con.commit()
        pprint("Clan deleted successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def inc_player_trophies(WinnerID):
    # pick a random number between 26 and 30
    increase = random.randint(26, 30)
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (WinnerID))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        query = """
            UPDATE Player SET Current_Trophies = Current_Trophies + %s WHERE PlayerID = %s
        """
        cursor.execute(query, (increase, WinnerID))
        con.commit()
        pprint("Player trophies increased successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def dec_player_trophies(LoserID):
    # pick a random number between 26 and 30
    decrease = random.randint(12, 18)
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (LoserID,))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        # if the player trophies are less than 12, set it to 0
        if result["Current_Trophies"] < 12:
            query = """
                UPDATE Player SET Current_Trophies = 0 WHERE PlayerID = %s
            """
            cursor.execute(query, (LoserID,))
            con.commit()
            pprint("Player trophies decreased successfully")
            return
        query = """
            UPDATE Player SET Current_Trophies = Current_Trophies - %s WHERE PlayerID = %s
        """
        cursor.execute(query, (decrease, LoserID))
        con.commit()
        pprint("Player trophies decreased successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def add_battle(BattleID, Start_Time, End_Time, Arena, WinnerID, PlayerID):
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (PlayerID))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (WinnerID))
        result = cursor.fetchone()
        if result is None:
            pprint("Winner not found")
            return
        cursor.execute("SELECT * FROM Arena WHERE Arena_Name = %s", (Arena))
        result = cursor.fetchone()
        if result is None:
            pprint("Arena not found")
            return
        cursor.execute("SELECT * FROM Battle WHERE BattleID = %s", (BattleID))
        result = cursor.fetchone()
        if result is None:
            query = """
            INSERT INTO Battle (BattleID , Start_Time, End_Time, Arena, WinnerID , PlayerID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
            values = (BattleID, Start_Time, End_Time,
                      Arena, WinnerID, PlayerID)
            cursor.execute(query, values)
            con.commit()
            dec_player_trophies(PlayerID)
            inc_player_trophies(WinnerID)
            pprint("Battle added successfully")
        else:
            pprint("Battle already exists")
    except pymysql.Error as err:
        pprint(f"Error: {err}")

    return


def del_player(PlayerID):
    try:
        # check if the PlayerID is in the Player table, if not, show error
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (PlayerID,))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return

        cursor.execute(
            "SELECT User_Name FROM Player WHERE PlayerID = %s", (PlayerID,))
        player_name = cursor.fetchone()
        player_name = player_name["User_Name"]
        cursor.execute(
            "SELECT * FROM Clan WHERE Clan_Leader = %s", (player_name,))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
        else:
            query = """
                UPDATE Clan SET Clan_Leader = NULL WHERE Clan_Leader = %s
            """
            cursor.execute(query, (player_name,))
            con.commit()
            pprint("Clan_Leader updated successfully")

        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (PlayerID,))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        query = """
            DELETE FROM Player WHERE PlayerID = %s
        """
        cursor.execute(query, (PlayerID,))
        con.commit()
        pprint("Player deleted successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def del_battle(BattleID):
    try:
        cursor.execute("SELECT * FROM Battle WHERE BattleID = %s", (BattleID))
        result = cursor.fetchone()
        if result is None:
            pprint("Battle not found")
            return
        query = """
            DELETE FROM Battle WHERE BattleID = %s
        """
        cursor.execute(query, (BattleID))
        con.commit()
        pprint("Battle deleted successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def update_card(CardID, new_level):
    try:
        # if new_level - current_level > 1, show error
        if new_level > 14:
            pprint("Card level cannot be greater than 14, setting it to 14")
            new_level = 14

        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (CardID))
        result = cursor.fetchone()
        if result is None:
            pprint("Card not found")
            return
        current_level = result["Card_Level"]
        if new_level - current_level > 1:
            pprint("Card level cannot be increased by more than 1")
            return

        if new_level - current_level <= 0:
            pprint("Card level cannot be decreased")
            return

        if new_level < 1:
            pprint("Card level cannot be less than 1, setting it to 1")
            new_level = 1

        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (CardID))
        result = cursor.fetchone()
        if result is None:
            pprint("Card not found")
            return
        query = """
            UPDATE Cards SET Card_Level = %s WHERE CardID = %s
        """
        cursor.execute(query, (new_level, CardID))
        query = """
            UPDATE Cards SET Card_Base_Hitpoints = Card_Base_Hitpoints * 1.1 WHERE CardID = %s
        """
        cursor.execute(query, (CardID))
        query = """
            UPDATE Cards SET Card_Base_Damage = Card_Base_Damage * 1.1 WHERE CardID = %s
        """
        cursor.execute(query, (CardID))
        con.commit()
        pprint("Card updated successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def update_email(PlayerID, new_email):
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (PlayerID))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        query = """
            UPDATE Player SET Email = %s WHERE PlayerID = %s
        """
        cursor.execute(query, (new_email, PlayerID))
        con.commit()
        pprint("Email updated successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def update_clan_leader(ClanID, PlayerID):
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (PlayerID))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        # get the player name
        cursor.execute(
            "SELECT User_Name FROM Player WHERE PlayerID = %s", (PlayerID,))
        player_name = cursor.fetchone()
        player_name = player_name["User_Name"]

        # check if the player is in the given clanID, if not show error
        cursor.execute(
            "SELECT ClanID FROM Player WHERE PlayerID = %s", (PlayerID,))
        player_clan_id = cursor.fetchone()
        player_clan_id = player_clan_id["ClanID"]
        if player_clan_id != ClanID:
            pprint("Player is not in the given clan, You cannot make him the leader")
            return

        cursor.execute("SELECT * FROM Clan WHERE ClanID = %s", (ClanID))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
            return
        query = """
            UPDATE Clan SET Clan_Leader = %s WHERE ClanID = %s
        """
        cursor.execute(query, (player_name, ClanID))
        con.commit()
        pprint("Clan Leader updated successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def change_clan(PlayerID, ClanID):
    try:
        cursor.execute("SELECT * FROM Player WHERE PlayerID = %s", (PlayerID,))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        cursor.execute("SELECT * FROM Clan WHERE ClanID = %s", (ClanID))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
            return
        query = """
            UPDATE Player SET ClanID = %s WHERE PlayerID = %s
        """
        cursor.execute(query, (ClanID, PlayerID))
        con.commit()
        pprint("Clan updated successfully")
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return

# retrieval operations
# operation 1: selecttion


def select_player(player_name):
    try:
        cursor.execute(
            "SELECT * FROM Player WHERE User_Name = %s", (player_name))
        result = cursor.fetchone()
        if result is None:
            pprint("Player not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def select_card(card_id):
    try:
        cursor.execute("SELECT * FROM Cards WHERE CardID = %s", (card_id))
        result = cursor.fetchone()
        if result is None:
            pprint("Card not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def select_clan(clan_name):
    try:
        cursor.execute("SELECT * FROM Clan WHERE Clan_Name = %s", (clan_name))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def select_deck(deck_id):
    try:
        cursor.execute("SELECT * FROM Deck WHERE DeckID = %s", (deck_id))
        result = cursor.fetchone()
        if result is None:
            pprint("Deck not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return

# retrieval operations
# projection operations
# select all players above trophies x in clan clan_name


def select_player_above_trophies(trophies, clan_name):
    try:
        cursor.execute(
            "SELECT * FROM Player WHERE Current_Trophies > %s AND ClanID = (SELECT ClanID FROM Clan WHERE Clan_Name = %s)", (trophies, clan_name))
        result = cursor.fetchall()
        if result is None:
            pprint("Player not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return

# select all cards above certain hp in a deck_id


def select_cards_deck(hp, deck_id):
    try:
        cursor.execute(
            "SELECT * FROM Cards WHERE Card_Base_Hitpoints > %s AND CardID IN (SELECT Card1_ID FROM Deck_Cards WHERE DeckID = %s)", (hp, deck_id))
        result = cursor.fetchall()
        if result is None:
            pprint("Card not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return

# aggregate functions
# count the number of players in a clan


def count_players(clan_name):
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM Player WHERE ClanID = (SELECT ClanID FROM Clan WHERE Clan_Name = %s)", (clan_name))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return
# avg trophies of players in a clan


def avg_trophies_clan(clan_name):
    try:
        cursor.execute(
            "SELECT AVG(Current_Trophies) FROM Player WHERE ClanID = (SELECT ClanID FROM Clan WHERE Clan_Name = %s)", (clan_name))
        result = cursor.fetchone()
        if result is None:
            pprint("Clan not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return

# function to search for player beginning with a string using like


def search_player(player_name):
    try:
        cursor.execute(
            "SELECT * FROM Player WHERE User_Name LIKE %s", (player_name + "%"))
        result = cursor.fetchall()
        if result is None:
            pprint("Player not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return
# similar function for clan name


def search_clan(clan_name):
    try:
        cursor.execute(
            "SELECT * FROM Clan WHERE Clan_Name LIKE %s", (clan_name + "%"))
        result = cursor.fetchall()
        if result is None:
            pprint("Clan not found")
            return
        pprint(result)
    except pymysql.Error as err:
        pprint(f"Error: {err}")
    return


def success_rate(player_id):
    try:
        # Get number of battles won by player and number of battles played by player
        won = 0
        played = 0

        # Join Battle and Player tables
        query = """
            SELECT Battle.*, Player.User_Name
            FROM Battle
            INNER JOIN Player ON Battle.PlayerID = Player.PlayerID
            WHERE Battle.WinnerID = %s OR Battle.PlayerID = %s
        """

        cursor.execute(query, (player_id, player_id))
        result = cursor.fetchall()

        if not result:
            pprint("Player not found or has not participated in any battles.")
            return

        for row in result:
            played += 1
            if row["WinnerID"] == player_id:
                won += 1

        success_rate = (won / played) if played > 0 else 0
        pprint(
            f"Player ID: {player_id}, User Name: {result[0]['User_Name']}, Success Rate: {success_rate:.2%}")

    except pymysql.Error as err:
        pprint(f"Error: {err}")

    return


username = "root"
password = "Patanjali@2003"
con = pymysql.connect(host='localhost',
                      port=3306,
                      user=username,
                      password=password,
                      db='CR',
                      cursorclass=pymysql.cursors.DictCursor)
if (con.open):
    pprint("Connected")
else:
    pprint("Failed to connect")
cursor = con.cursor()
def call_insertion():
    pprint("Enter 1 to add a player")
    pprint("Enter 2 to add a card")
    pprint("Enter 3 to add a clan")
    pprint("Enter 4 to add a deck")
    pprint("Enter 5 to add a battle")
    pprint("Enter 6 to exit")
    choice = int(input())
    if choice == 1:
        user_name = input("Enter the user name: ")
        email = input("Enter the email: ")
        trophies = int(input("Enter the current trophies: "))
        level = int(input("Enter the level: "))
        clan_id = int(input("Enter the clan id: "))
        highest_trophies = int(input("Enter the highest trophies: "))
        add_players(user_name, email, trophies,
                    level, clan_id, highest_trophies)
    elif choice == 2:
        card_id = int(input("Enter the card id: "))
        hp = int(input("Enter the hp: "))
        damage = int(input("Enter the damage: "))
        elixit = int(input("Enter the elixit: "))
        level = int(input("Enter the level: "))
        rarity = input("Enter the rarity: ")
        add_cards(card_id, hp, damage, elixit, level, rarity)
    elif choice == 3:
        ClanID = int(input("Enter the clan id: "))
        Clan_Name = input("Enter the clan name: ")
        Clan_Trophies = int(input("Enter the clan trophies: "))
        Description = input("Enter the description: ")
        Clan_Leader = input("Enter the clan leader: ")
        add_clan(ClanID, Clan_Name, Clan_Trophies,
                 Description, Clan_Leader)
    elif choice == 4:
        player_id = int(input("Enter the player id: "))
        card1 = int(input("Enter the card1: "))
        card2 = int(input("Enter the card2: "))
        card3 = int(input("Enter the card3: "))
        card4 = int(input("Enter the card4: "))
        deck_name = input("Enter the deck name: ")
        add_deck(player_id, card1, card2, card3, card4, deck_name)
    elif choice == 5:

        BattleID = int(input("Enter the battle id: "))
        # Start_Time = input("Enter the start time: ")
        # End_Time = input("Enter the end time: ")
        Start_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # end time is 3 mins later
        End_Time = (datetime.datetime.now() +
                    datetime.timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")
        Arena = input("Enter the arena: ")
        WinnerID = int(input("Enter the winner id: "))
        PlayerID = int(input("Enter the player id: "))
        add_battle(BattleID, Start_Time, End_Time,
                   Arena, WinnerID, PlayerID)
    elif choice == 6:
        return
    else:
        pprint("Invalid choice")
        return

def call_deletion():
    pprint("Enter 1 to delete a player")
    pprint("Enter 2 to delete a card")
    pprint("Enter 3 to delete a clan")
    pprint("Enter 4 to delete a battle")
    pprint("Enter 5 to exit")
    choice = int(input())
    if choice == 1:
        PlayerID = int(input("Enter the player id: "))
        del_player(PlayerID)
    elif choice == 2:
        CardID = int(input("Enter the card id: "))
        delete_card(CardID)
    elif choice == 3:
        ClanID = int(input("Enter the clan id: "))
        del_clan(ClanID)
    elif choice == 4:
        BattleID = int(input("Enter the battle id: "))
        del_battle(BattleID)
    elif choice == 5:
        return
    else:
        pprint("Invalid choice")
        return
def call_updation():
    pprint("Enter 1 to update a card level")
    pprint("Enter 2 to update a player email")
    pprint("Enter 3 to update a clan leader")
    pprint("Enter 4 to change a clan")
    pprint("Enter 5 to  increase player trophies")
    pprint("Enter 6 to decrease player trophies")
    pprint("Enter 7 to exit")
    choice = int(input())
    if choice == 1:
        CardID = int(input("Enter the card id: "))
        new_level = int(input("Enter the new level: "))
        update_card(CardID, new_level)
    elif choice == 2:
        PlayerID = int(input("Enter the player id: "))
        new_email = input("Enter the new email: ")
        update_email(PlayerID, new_email)
    elif choice == 3:
        ClanID = int(input("Enter the clan id: "))
        PlayerID = int(input("Enter the player id: "))
        update_clan_leader(ClanID, PlayerID)
    elif choice == 4:
        PlayerID = int(input("Enter the player id: "))
        ClanID = int(input("Enter the clan id: "))
        change_clan(PlayerID, ClanID)
    elif choice == 5:
        WinnerID = int(input("Enter the winner id: "))
        inc_player_trophies(WinnerID)
    elif choice == 6:
        LoserID = int(input("Enter the loser id: "))
        dec_player_trophies(LoserID)
    elif choice == 7:
        return
    else:
        pprint("Invalid choice")
        return
def call_selection():
    pprint("Enter 1 to select a player")
    pprint("Enter 2 to select a card")
    pprint("Enter 3 to select a clan")
    pprint("Enter 4 to select a deck")
    pprint("Enter 5 to exit")
    choice = int(input())
    if choice == 1:
        player_name = input("Enter the player name: ")
        select_player(player_name)
    elif choice == 2:
        card_id = int(input("Enter the card id: "))
        select_card(card_id)
    elif choice == 3:
        clan_name = input("Enter the clan name: ")
        select_clan(clan_name)
    elif choice == 4:
        deck_id = int(input("Enter the deck id: "))
        select_deck(deck_id)
    elif choice == 5:
        return
    else:
        pprint("Invalid choice")
        return
def call_projection():
    pprint("Enter 1 to select all players above trophies x in clan clan_name")
    pprint("Enter 2 to select all cards above certain hp in a deck_id")
    pprint("Enter 3 to exit")
    choice = int(input())
    if choice == 1:
        trophies = int(input("Enter the trophies: "))
        clan_name = input("Enter the clan name: ")
        select_player_above_trophies(trophies, clan_name)
    elif choice == 2:
        hp = int(input("Enter the hp: "))
        deck_id = int(input("Enter the deck id: "))
        select_cards_deck(hp, deck_id)
    elif choice == 3:
        return
    else:
        pprint("Invalid choice")
        return
def call_aggregate():
    pprint("Enter 1 to count the number of players in a clan")
    pprint("Enter 2 to avg trophies of players in a clan")
    pprint("Enter 3 to exit")
    choice = int(input())
    if choice == 1:
        clan_name = input("Enter the clan name: ")
        count_players(clan_name)
    elif choice == 2:
        clan_name = input("Enter the clan name: ")
        avg_trophies_clan(clan_name)
    elif choice == 3:
        return
    else:
        pprint("Invalid choice")
        return
def call_search():
    pprint("Enter 1 to search for player beginning with a string using like")
    pprint("Enter 2 to similar function for clan name")
    pprint("Enter 3 to exit")
    choice = int(input())
    if choice == 1:
        player_name = input("Enter the player name: ")
        search_player(player_name)
    elif choice == 2:
        clan_name = input("Enter the clan name: ")
        search_clan(clan_name)
    elif choice == 3:
        return
    else:
        pprint("Invalid choice")
        return
def call_analysis():
    pprint("Enter 1 to find success rate of a player")
    pprint("Enter 2 for average tenure of a clan")
    pprint("Enter 3 to exit")
    choice = int(input())
    if choice == 1:
        player_id = int(input("Enter the player id: "))
        success_rate(player_id)
    elif choice == 2:
        clan_name = input("Enter the clan name: ")
        avg_tenure(clan_name)
    elif choice == 3:
        return
    else:
        pprint("Invalid choice")
        return

from pprint import pprint
def view_tables():
    pprint("Enter 1 to view Player table")
    pprint("Enter 2 to view Cards table")
    pprint("Enter 3 to view Clan table")
    pprint("Enter 4 to view Battle table")
    choice = int(input())
    if choice == 1:
        cursor.execute("SELECT * FROM Player")
        result = cursor.fetchall()
        pprint(result)
    elif choice == 2:
        cursor.execute("SELECT * FROM Cards")
        result = cursor.fetchall()
        pprint(result)
    elif choice == 3:
        cursor.execute("SELECT * FROM Clan")
        result = cursor.fetchall()
        pprint(result)
    elif choice == 4:
        cursor.execute("SELECT * FROM Battle")
        result = cursor.fetchall()
        pprint(result)
    else:
        pprint("Invalid choice")
        return


while(1):
    pprint("Enter 1 for insertion")
    pprint("Enter 2 for deletion")
    pprint("Enter 3 for updation")
    pprint("Enter 4 for selection")
    pprint("Enter 5 for projection")
    pprint("Enter 6 for aggregate")
    pprint("Enter 7 for search")
    pprint("Enter 8 for analysis")
    pprint("Enter 9 to view tables")
    pprint("Enter 10 to exit")
    choice = int(input())
    pprint("========================================================================================")
    if choice == 1:
        call_insertion()
    elif choice == 2:
        call_deletion()
    elif choice == 3:
        call_updation()

    elif choice == 4:
        call_selection()
    elif choice == 5:
        call_projection()
    elif choice == 6:
        call_aggregate()
    elif choice == 7:
        call_search()
    elif choice == 8:
        call_analysis()
    elif choice == 9:
        view_tables()
    elif choice == 10:
        break
    else:
        pprint("Invalid choice")
        continue
    pprint("--------------------------------------------------------------------------------------")
