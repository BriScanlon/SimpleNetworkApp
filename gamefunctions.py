# define all game functions here
import random

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " "]
points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0]
tilecounts = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1, 2]
player_to_words = {}
letter_to_points = {letters: points for letters, points in zip(letters, points)}
letter_to_tilecounts = {letters: tilecounts for letters, tilecounts in zip(letters, tilecounts)}
player_to_points = {}
gameState = True
setup = True


# function that acts as a 6 sided dice
def d6():
    dice_roll = random.randint(0, 6)+1
    return dice_roll


# function to create new player
def newplayer(playername):
    player_to_words[playername] = []


# function to return word score
def score_word(word):
    point_total = 0
    for letter in word:
        point_total += letter_to_points.get(letter, 0)
    return point_total


# function to update player played words
def play_word(player, word):
    player_to_words[player].append(word)


# function to track player scores
def update_print_totals(playerp):
    player_points = 0
    for playerp, words in player_to_words.items():
        for word in words:
            player_points += score_word(word)
    player_to_points[playerp] = player_points
    return player_points

