import random
import itertools
import json
class SakClass:
    """TODO: Η πληροφορία για το πόσα γράμματα παραμένουν στο σακουλάκι θα πρέπει να είναι γνωστή στον παίκτη. """
    greek_scrabble_info = {'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1],
                'Ζ': [1, 10], 'Η': [7, 1], 'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2],
                'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10], 'Ο': [9, 1],
                'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 2],
                'Φ': [1, 8], 'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 3]
                           }

    def __init__(self):
        self.num_letters = 104  # number of letters
        self.bag = []
        print("Ετοιμάζεται το σακουλάκι")

        for letter in self.greek_scrabble_info:  # loop through every letter

            for i in range(self.greek_scrabble_info[letter][0]):
                self.bag.append(letter)  # add this letter to the list as many times as the bag_info list says
            # self.bag looks like this... [A,A,A,A,A,A...,B,Γ,Γ...

    def randomize_sak(self):
        random.shuffle(self.bag)

    def putbackletters(self, player_letters: list):
        self.num_letters += len(player_letters)  # count how many new letters are given back and add to the count
        self.bag = self.bag + player_letters  # add the letters back into the list
        self.randomize_sak()  # reshuffles list

    def getletters(self, num_letters):
        self.num_letters -= num_letters  # remove the letters from the count
        ret = []  # list of letters that will be given
        for i in range(num_letters):
            ret.append(self.bag.pop())
        return ret


class Player:


    def __init__(self, name,score):
        self.name = name
        self.score = score
        self.letters = []
    def __repr__(self):
        return 'Player:{0}, Score:{1}'.format(self.name, self.score)

    def play_word(self,word: str,sak: SakClass):
            self.score += Game.scrabble_score(word)
            for letter in word:
                self.letters.remove(letter) #remove the letters from player

            self.letters = self.letters + sak.getletters(len(word))#adding letters





class Computer(Player):
    def __init__(self):
        Player.__init__(self,"Υπολογιστής",0)

    def play_word(self,word: str,sak: SakClass):
        Player.play_word(self,word,sak)

    def play(self, dictionary,mode:  int = 0 ):
        """0 is MIN-letters, 1 is MAX-letters, anything else is the SMART algorithm"""
        if mode==0: #MIN-Letters
            for i in range(2,8):
                for word in itertools.permutations(self.letters,i):
                    if ''.join(list(word)) in dictionary:
                        return ''.join(list(word))
        #END OF MIN-LETTERS

        #MAX-LETTERS
        elif mode==1:
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    if ''.join(list(word)) in dictionary:
                        return ''.join(list(word))
        #END OF MAX-LETTERS

        #SMART
        else:
            best_word = ""
            value =0
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    word_as_str = ''.join(list(word))
                    if word_as_str in dictionary and dictionary[word_as_str]>value:
                        #print(word_as_str)
                        best_word = word_as_str
                        value = dictionary[word_as_str]
            return best_word
        #END OF SMART


class Human(Player):

    def __init__(self,name,score):
        Player.__init__(self,name,score)
    def play_word(self,dictionary,word: str,sak: SakClass):
        """TODO: ASSUME PLAYER PLAYS CORRECTLY FOR NOW, CHECK DISTIONARY LATER"""
        if word in dictionary:#DO:and the the player has the letters that he used
            print("valid word")
        else:
            print("that's not a valid word")
        Player.play_word(self,word,sak)


    def play(self,dictionary,sak: SakClass):
        """TODO: this method should simulate how the player plays (e.g. inputs)"""
        print("play of human")
        print("Player:",self.name,self.letters)
        word = input("Πες λέξη:")
        self.play_word(dictionary,word,sak)
        print(self.letters)


class Game:
    @staticmethod
    def scrabble_score(word:str):
        score = 0
        for letter in word:
            score += SakClass.greek_scrabble_info[letter][1]

        return score
    def __init__(self):
        self.player1 = Human("matt",0)
        self.player2= Computer()
        self.sakoulaki = SakClass()
        self.sakoulaki.randomize_sak()
        self.word_dictionary = {}
        self.mode =0

    def setup(self):
        dict = {}
        # OPEN FILE AND LOAD WORDS IN DICT

        with open("greek7.txt", "r", encoding='utf-8') as dict_file:
            for line in dict_file:
                dict.update(
                    {line.strip(): self.scrabble_score(line.strip())})  # add each word along with its scrabble value
        self.word_dictionary = dict

    def run(self):
        """TODO: ARTEMIS"""
        #DRAW INITIAL LETTERS
        self.player1.letters = self.sakoulaki.getletters(7)
        self.player2.letters = self.sakoulaki.getletters(7)
        print("player= ",self.player1.letters)
        print("computer= ",self.player2.letters)
        WORD = self.player2.play(self.word_dictionary,2)
        print("computers choice is",WORD)
        #in play() for human
        self.player1.play(self.word_dictionary,self.sakoulaki)


    def end(self):
        """TODO:Keep stats in json file"""
        return "will save in the future"


#MAIN KAI KALA

if __name__ == "__main__":

            # load file
    newgame = Game()
    newgame.setup()
    newgame.run()
    """
    x = SakClass()
    x.randomize_sak()
    print(len(x.bag), x.bag)
    player = x.getletters(7)
    print(len(x.bag), x.bag)
    
    print(player)
    x.putbackletters(player)
    print(len(x.bag), x.bag)
    """