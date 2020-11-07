#TIP: use random.randint to get a random word from the list
import random


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    return lines


def select_random_word(words):
    length_of_list = len(words)
    new_word = words[random.randint(0, length_of_list-1)]
    length_of_word = len(new_word)
    missing_letter = random.randint(0, length_of_word-2)
    guess_word = new_word[:missing_letter] + "_" + new_word[missing_letter+1:]
    print("Guess the word: "+guess_word)
    return new_word



def get_user_input():
    guess = input("Guess the missing letter: ")
    return guess


def run_game(file_name):
    """
    This is the main game code. You can leave it as is and only implement steps 1 to 3 as indicated above.
    """
    words = read_file(file_name)
    word = select_random_word(words)
    answer = get_user_input()
    print('The word was: '+word)


if __name__ == "__main__":
    run_game('short_words.txt')

