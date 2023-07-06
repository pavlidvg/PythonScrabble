import random
import itertools
import json
import math

#GLOBAL

#load
scoreboard = {"Vasilis":120,
              "Artemis":131}
with open("highscores.json","r") as loadfile:
    scoreboard = json.load(loadfile)
print("HIGHSCORES ΠΑΙΚΤΩΝ:")
print(scoreboard)

computer_mode = 1
class SakClass:

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
        #print("requested:",num_letters)
        ret = []  # list of letters that will be given
        if self.num_letters >= num_letters and len(self.bag)>= num_letters:
            self.num_letters -= num_letters  # remove the letters from the count
            for i in range(num_letters):
                ret.append(self.bag.pop())
            self.num_letters = len(self.bag)
            #print("AFTER PLAY",len(self.bag))
            return ret
        else:
            for i in range(len(self.bag)):
                ret.append(self.bag.pop())
            self.num_letters = 0
            #print("AFTER PLAY", len(self.bag))
            return ret


class Player:


    def __init__(self, name,score):
        self.name = name
        self.score = score
        self.letters = []
    def __repr__(self):
        return 'Player:{0}, Score:{1}'.format(self.name, self.score)

    def play_word(self,word: str,sak: SakClass):

        self.score += Game.scrabble_score(word)#updating score
        for letter in word:
            self.letters.remove(letter) #remove the letters from player

        if sak.num_letters>=len(word):
            self.letters = self.letters + sak.getletters(len(word))#adding letters




class Computer(Player):
    def __init__(self):
        Player.__init__(self,"Υπολογιστής",0)
        self.mode = 3

    def play_word(self,word: str,sak: SakClass):

        print("Computer: Διαθέσιμα Γράμματα",self.letters)
        Player.play_word(self, word, sak)
        print("Λέξη:",word,"Βαθμοι:",Game.scrabble_score(word),"Σκορ: ",self.score)
    def play(self, dictionary,mode:  int = 3 ):
        """1 is MIN-letters, 2 is MAX-letters, anything else is the SMART algorithm"""
        if self.mode==1: #MIN-Letters mode 1
            for i in range(2,8):
                for word in itertools.permutations(self.letters,i):
                    if ''.join(list(word)) in dictionary:
                        return ''.join(list(word))
            return "e"
        #END OF MIN-LETTERS

        #MAX-LETTERS mode 2
        elif self.mode==2:
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    if ''.join(list(word)) in dictionary:
                        return ''.join(list(word))
            return "e"
        #END OF MAX-LETTERS

        #SMART mode 4
        elif self.mode==4:
            best_word = ""
            value =0
            for i in range(8,2,-1):
                for word in itertools.permutations(self.letters,i):
                    word_as_str = ''.join(list(word))
                    if word_as_str in dictionary and dictionary[word_as_str]>value:
                        best_word = word_as_str
                        value = dictionary[word_as_str]
            #print("best word:"+best_word)
            if not best_word: #if the word is still empty
                return "e"

            return best_word

        #END OF SMART

        #SMART-FAIL mode 3
        elif self.mode==3:
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


            if len(sorted_words) > 1:
                for i in range(len(sorted_words)-1): #loop through every word, starting from the best
                    #print("checking ",sorted_words[i])
                    if random.randint(1,10) > 5:
                        return sorted_words[i][0] #you have a 50% chance of palying this word and stopping the algorithm
                return sorted_words[len(sorted_words)][0] #play the worst word, if you got unlucky
            else:
                try:
                    return sorted_words[0][0] #play the only playable word
                except:
                    print("O Υπολογιστής δεν βρήκε κάποια λέξη με τα γράμματά του")
                    return "e" #play if no word exists
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
            elif word=="p":
                return "p"
            elif word in dictionary:
                playable = True
                word = str(word)
                print(word)
                try:
                    testlist = []
                    testlist2 = self.letters.copy()

                    for letter in word:
                        if letter in testlist2:
                            testlist2.remove(letter)

                        else:
                            playable = False

                        #if there was an error,next two lines won't execute


                except:
                    #if there was an error, you dont have the letters
                    playable = False

                if not playable:
                    print("Δεν έχετε τα γράμματα για αυτή  την λέξη")
                else:
                    self.play_word(dictionary,word,sak)
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
        word = str(word)
        for letter in word:
            try:
                score += SakClass.greek_scrabble_info[letter][1]
            except:
                score+=1
                print("A word with a non greek letter appeared:",letter)



        return score
    def __init__(self,name):
        self.player1 = Human(name,0)
        self.player2= Computer()
        self.sakoulaki = SakClass()
        self.sakoulaki.randomize_sak()
        self.word_dictionary = {}


    def setup(self):

        dict = {}
        # OPEN FILE AND LOAD WORDS IN DICT

        with open("greek7.txt", "r", encoding='utf-8') as dict_file:
            for line in dict_file:
                dict.update(
                    {line.strip(): self.scrabble_score(line.strip())})  # add each word along with its scrabble value
        self.word_dictionary = dict


    def run(self):

        #DRAW INITIAL LETTERS
        self.player1.letters = self.sakoulaki.getletters(7)
        self.player2.letters = self.sakoulaki.getletters(7)
        while True:

            #PLAYER2
            print("--------------------")
            WORD = self.player2.play(self.word_dictionary,self.player2.mode)
            if WORD=="e":
                self.sakoulaki.putbackletters(self.player2.letters)
                if self.sakoulaki.num_letters >= 7:

                    self.player2.letters = self.sakoulaki.getletters(7)
                else:
                    self.end()
                    return
            else:
                self.player2.play_word(WORD,self.sakoulaki)
                if len(WORD) > self.sakoulaki.num_letters:
                    self.end()
                    return
            print("Γράμμματα που έμειναν στο σακουλάκι:",self.sakoulaki.num_letters)
            print("--------------------")

            #PLAYER1
            Word=self.player1.play(self.word_dictionary,self.sakoulaki)
            if Word=="e" or Word=="q":
                break
            if Word == "p":
                if self.sakoulaki.num_letters <7:
                    self.end()
                    return
                self.sakoulaki.putbackletters(self.player1.letters)
                self.player1.letters = self.sakoulaki.getletters(7)
            print("Γράμματα που έμειναν στο σακουλάκι:", self.sakoulaki.num_letters)
            if self.sakoulaki.num_letters<len(Word):
                self.end()
                return


        if Word=="e" or Word=="q":#e=if the human can't create a word, "q"=quit the game and return to the menu
            return Word





    def end(self):
        print("---------")
        print("Τέλος παιχνιδιου")
        print("---------")
        full_score = self.player1.score
        if self.player1.score>self.player2.score:
            print("Κέρδισες τον Υπολογιστή!")
            full_score= full_score + (full_score * (self.player2.mode/10))
        elif self.player1.score<self.player2.score:
            print("Κέρδισε ο Υπολογιστής :(")
        else:
            print("Είστε ισοπαλία")
        try:
            if scoreboard[self.player1.name]<full_score: #if the player got a new highscore
                scoreboard[self.player1.name] = full_score #update the leaderboard, else do nothing
        except:
            scoreboard[self.player1.name] = full_score #if this name doesn't exist, add it on the leaderboard

        open("highscores.json","w").close() #delete previous file contents
        with open("highscores.json","w") as save:
            json.dump(scoreboard,save)

        return "will save in the future"
    def replay(self):
        """Runs all resets in order for a new game to be played"""
        self.sakoulaki = SakClass()
        self.player1.score = self.player2.score = 0


#MAIN KAI KALA

if True:

    player_name = input("Δώστε το όνομα του παίκτη σας. Αν είχατε παίξει παλαιότερα με άλλο όνομα, μπορείτε να το χρησιμοποιήσετε για να προσπεράσετε τα σκορ σας:")

    newgame = Game(player_name)#to vazoume afto ekei pou ksekinaei to paixnidi?
    newgame.setup()#kai afto?

    while True:
        print("***** SCRABBLE *****\n--------------------\n1: Σκορ\n2: Ρυθμίσεις\n3: Παιχνίδι\nq: Έξοδος\n--------------------")
        menou=input("Επίλεξε 1,2,3 ή q απο το μενού\n")
        if menou=="1":
            try:
                print("Highscore:",scoreboard[player_name])
            except:
                print("Highscore:0")
        elif menou=="2":
            print("Διάλεξε επίπεδο του υπολογιστή\n1:MIN\n2:MAX\n3:SMART-FAIL(50% να χάσει μία λέξη)\n4:SMART\n Παίρνεις περισσότερους πόντους, όσο μεγαλύτερο mode διαλέξεις, αλλά μόνο αν κερδίσεις!\nmode:")
            mode=input()
            try:
                newgame.player2.mode = int(mode)
            except:
                newgame.player2.mode = 3
                print("Λανθασμένη ένδειξη. Επιλέχθηκε ο αλγόριθμος SMART-FAIL για την καλύτερη εμπειρία παιχνιδιού")
        elif menou=="3":
            print("The game starts")
            end= newgame.run()
            newgame.replay()
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