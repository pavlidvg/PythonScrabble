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
            ret.append(self.bag.pop())#ToDo: check if you pop to an empty list
        return ret


class Player:


    def __init__(self, name,score):
        self.name = name
        self.score = score
        self.letters = []
    def __repr__(self):
        return 'Player:{0}, Score:{1}'.format(self.name, self.score)

    def play_word(self,word: str,sak: SakClass):
        #ToDo: check if the sak has letters
            self.score += Game.scrabble_score(word)#updating score
            for letter in word:
                self.letters.remove(letter) #remove the letters from player

            self.letters = self.letters + sak.getletters(len(word))#adding letters




class Computer(Player):
    def __init__(self):
        Player.__init__(self,"Υπολογιστής",0)

    def play_word(self,word: str,sak: SakClass):
        Player.play_word(self,word,sak)
        print("Computer: Διαθέσιμα Γράμματα",self.letters)#ToDo:hide computers letters
        print("Λέξη:",word,"Βαθμοι:",Game.scrabble_score(word),"Σκορ: ",self.score)
    def play(self, dictionary,mode:  int = 2 ):
        """0 is MIN-letters, 1 is MAX-letters, anything else is the SMART algorithm"""
        #ToDo: check if it can create letter, else return "e"
        if mode==1: #MIN-Letters mode 1
            for i in range(2,8):
                for word in itertools.permutations(self.letters,i):
                    if ''.join(list(word)) in dictionary:
                        return ''.join(list(word))
        #END OF MIN-LETTERS

        #MAX-LETTERS mode 2
        elif mode==2:
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    if ''.join(list(word)) in dictionary:
                        return ''.join(list(word))
        #END OF MAX-LETTERS

        #SMART mode 4
        elif mode==4:
            best_word = ""
            value =0
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    word_as_str = ''.join(list(word))
                    if word_as_str in dictionary and dictionary[word_as_str]>value:
                        best_word = word_as_str
                        value = dictionary[word_as_str]
            return best_word
        #END OF SMART

        #SMART-FAIL mode 3
        elif mode==3: #ToDo: complete it, how to convert list to dictionary??
            #START OF SMART
            words={}
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    word_as_str = ''.join(list(word))
                    if word_as_str in dictionary:
                       words[word_as_str]= dictionary[word_as_str]
            #END OF SMART
            sorted_words = sorted(words.items(), key=lambda x:x[1], reverse=True)
            #sortedwords=dict(sorted_words) #convert list to dictionary
            print(sorted_words)#ToDo:convert the list to dictionary and return the the word with value=(best value)-2
        #END OF SMART-FAIL


class Human(Player):

    def __init__(self,name,score):
        Player.__init__(self,name,score)
    def play_word(self,dictionary,word: str,sak: SakClass):
        Player.play_word(self,word,sak)
        #ToDo: check if the sak has letters. If it doesn't return "e"


    def play(self,dictionary,sak: SakClass):
        print("Παίκτης:",self.name,"Διαθέσιμα Γράμματα",self.letters, "Σκορ: ",self.score)

        while True:
            print("Πες λέξη ή γράψε q για έξοδο ή γράψε p για pass:")
            word=input("Λέξη: ")
            played=0
            if word=="q":
                print("Επιστροφή στο μενού")
                break
            elif word=="p":#ToDo:aftos leei kati allo gia to p???
                print("the player wants to pass")
                break
            elif word in dictionary:
                notInList=0
                for letter in word:
                  if letter not in self.letters:#ToDo:it passes even if you use the same letter twice when you don't have it
                    notInList=1
                if notInList==1:
                    print("Δεν έχεις αυτά τα γράμματα")
                else:
                    self.play_word(dictionary,word,sak)#ToDo: check if the sak has letters and he can play a valid word
                    print("Αποδεκτή Λέξη - Βαθμοί: ",Game.scrabble_score(word),"Σκορ: ",self.score)
                    played=1
                    break
            else:
                print("Μη αποδεκτή Λέξη")
        if played==0 and word!="p" and word!="q":
            return "e"
        else:
            return word



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
        self.mode =4#ToDo:put default 1,2,3 or 4

    def setup(self):
        dict = {}
        # OPEN FILE AND LOAD WORDS IN DICT

        with open("greek7.txt", "r", encoding='utf-8') as dict_file:
            for line in dict_file:
                dict.update(
                    {line.strip(): self.scrabble_score(line.strip())})  # add each word along with its scrabble value
        self.word_dictionary = dict

    def run(self):
        """TODO:add conditions to end the game"""
        #DRAW INITIAL LETTERS
        self.player1.letters = self.sakoulaki.getletters(7)
        self.player2.letters = self.sakoulaki.getletters(7)
        while True:
            print("--------------------")
            WORD = self.player2.play(self.word_dictionary,4)#ToDo:replace 4 with the actual mode or change it from menu
            if WORD=="e":#ToDo: make the computer return e when it can't create a word
                break
            self.player2.play_word(WORD,self.sakoulaki)
            print("--------------------")
            Word=self.player1.play(self.word_dictionary,self.sakoulaki)
            if Word=="e" or Word=="q":
                break

        if WORD=="e":#if the computer can't create a word
            return WORD
        elif Word=="e" or Word=="q":#e=if the human can't create a word, "q"=quit the game and return to the menu
            return Word
        #ToDO:If the computer or the player returns "e", to other player keeps going until he also returns "e", or "q" for the human


    def end(self):
        """TODO:Keep stats in json file"""
        return "will save in the future"


#MAIN KAI KALA

if __name__ == "__main__":

    newgame = Game()#to vazoume afto ekei pou ksekinaei to paixnidi?
    newgame.setup()#kai afto?
    #ToDo: name=input("Write your name\n") replace "matt" with the name
    while True:
        print("***** SCRABBLE *****\n--------------------\n1: Σκορ\n2: Ρυθμίσεις\n3: Παιχνίδι\nq: Έξοδος\n--------------------")
        menou=input("Επίλεξε 1,2,3 ή q απο το μενού\n")
        if menou=="1":
                print("score:")#ToDo:put the player's score
        elif menou=="2":
            print("Δίαλεξε επίπεδο του υπολογιστή\n1:μέτριος\n2:καλός\n3:έξυπνος\n4:πανέξυπνος")
            mode=input()#ToDo: set the self.mode
        elif menou=="3":
                print("The game starts")
                end= newgame.run()
                if end=="e":
                    print("Game over")
                elif end=="q":
                    print("you pressed quit")
        elif menou=="q":
                print("Έξοδος")
                break
        else:
            print("Δεν υπάρχει αυτή η επιλογή. Επίλεξε 1,2,3 ή q απο το μενού")


        # load file


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