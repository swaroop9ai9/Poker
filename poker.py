import random
from collections import Counter
from collections import defaultdict
import os

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class Deck:
    def __init__(self):
        self.cards = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in range(2, 15):
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Hand(Card):
    def __init__(self):
        self.cards = []
        self.ranks = []
        self.suits = []

    def addCard(self, card):
        self.cards.append(card)

    def isFlush(self, suits):
        return len(set(suits)) == 1

    def isStraight(self, ranks):
        A = 14
        if len(set(ranks)) == 5 and (ranks[-1] - ranks[0] == 4):
            return True # With A being 14
        if A in ranks:
            return sum(ranks) - 13 == 15 # With A being 1
        return False


    def isTwoPair(self, ranks):
        pairs = Counter(ranks)
        unique = [i for i,j in pairs.items() if j==2]
        if len(unique) == 2:
            return True
        else:
            return False

    def isOnePair(self, ranks):
        pairs = Counter(ranks)
        unique = [i for i,j in pairs.items() if j==2]
        if len(unique) == 1:
            return True
        else:
            return False

    def getCombination(self):
        self.ranks = [card.rank for card in self.cards]
        self.suits = [card.suit for card in self.cards]
        self.ranks.sort(reverse=True)

        if self.isFlush(self.suits):
            return "Flush"
        elif self.isStraight(self.ranks):
            return "Straight"
        elif self.isTwoPair(self.ranks):
            return "Two Pair"
        elif self.isOnePair(self.ranks):
            return "One Pair"
        else:
            return "High Card"

class Compare(Hand):
    def __init__(self,hand1,hand2):
        self.hand1 = hand1
        self.hand2 = hand2
        self.beat = {'Flush':5,'Straight':4,'Two Pair':3,'One Pair':2,'High Card':1}
        self.cat1 = self.hand1.getCombination()
        self.cat2 = self.hand2.getCombination()
    # We could just calculate the difference and see which one is higher as both ranks are already sorted.
    def higherFlush(self,rank1,rank2):
        for i in range(len(rank1)):
            if rank1[i] - rank2[i] > 0:
                return "Hand1 Wins!"
            elif rank1[i] - rank2[i] < 0:
                return "Hand2 Wins!"
            else:
                pass
        return "Split Pot!"
    # As both are Straight, and ranks are sorted, we can check the last value and decide which hand wins.
    def higherStraight(self,rank1,rank2):
        if rank1[-1] > rank2[-1]:
            return "Hand1 wins!"
        elif rank1[-1] < rank2[-1]:
            return "Hand2 Wins!"
        else:
            return "Split Pot!"

    # As we need to omit two pairs and one pair, if the function is called from there. 
    # We only compare Cards with count == 1, we remove elements if they are same and check for second maxs
    def higherFace(self,rank1,rank2):
        p1 = Counter(rank1)
        p2 = Counter(rank2)
        unique1 = [i for i,j in p1.items() if j==1]
        unique2 = [i for i,j in p2.items() if j ==1]
        print(unique1)
        print(unique2)
        while unique1 and unique2:
            if max(unique1) > max(unique2):
                return "Hand1 Wins!"
            elif max(unique1) < max(unique2):
                return "Hand2 Wins!"
            else:
                unique1.remove(max(unique1))
                unique2.remove(max(unique2))

    # Use Counter to append the two pairs, check based of rank of both hands, if both pairs have same ranks,
    # We find hand with higher rank card.
    def higherTwoPair(self,rank1,rank2):
        p1 = Counter(rank1)
        p2 = Counter(rank2)
        pairs1 = [i for i,j in p1.items() if j==2]
        pairs2 = [i for i,j in p2.items() if j ==2]
        print(pairs1)
        print(pairs2)
        if pairs1[0] > pairs2[0]:
            return "Hand1 Wins!"
        elif pairs1[0] < pairs2[0]:
            return "Hand2 Wins!"
        else:
            if pairs1[1] > pairs2[1]:
                return "Hand1 Wins!"
            elif pairs1[1] < pairs2[1]:
                return "Hand2 Wins!"
            else:
                return self.higherFace(self,rank1,rank2)

    # Similar to two pair. 
    def higherPair(self,rank1,rank2):
        p1 = Counter(rank1)
        p2 = Counter(rank2)
        unique1 = [i for i,j in p1.items() if j==2]
        unique2 = [i for i,j in p2.items() if j ==2]
        if unique1[0] > unique2[0]:
            return "Hand 1 Wins"
        elif unique1[0] < unique2[0]:
            return "Hand 2 Wins"
        else:
            return self.higherFace(self,rank1,rank2)

    # Checks if there is a easy combination beat, if both hands have same combination.
    # We check the higher combination        
    def priority(self):
        print("Ranks of Hand 1: ",self.hand1.ranks)
        print("Ranks of Hand 2: ",self.hand2.ranks)
        print("Suits of Hand 1: ",self.hand1.suits)
        print("Suits of Hand 2: ",self.hand2.suits)
        print("\n")
        if self.beat[self.cat1] > self.beat[self.cat2]:
            return "Hand1 Wins!"
        elif self.beat[self.cat1] < self.beat[self.cat2]:
            return "Hand2 Wins!"
        else:
            # Flush
            if(self.cat1 == 'Flush' and self.cat2 == 'Flush'):
                return self.higherFlush(self.hand1.ranks,self.hand2.ranks)
            # Straight Case
            elif(self.cat1 == 'Straight' and self.cat2 == 'Straight'):
                return self.higherStraight(self.hand1.ranks,self.hand2.ranks)
            # Two Pair
            elif(self.cat1 == 'Two Pair' and self.cat2 == 'Two Pair'):
                return self.higherTwoPair(self.hand1.ranks,self.hand2.ranks)
            # Pair
            elif(self.cat1 == 'One Pair' and self.cat2 == 'One Pair'):
                return self.higherPair(self.hand1.ranks,self.hand2.ranks)
            else:
                return self.higherFace(self.hand1.ranks,self.hand2.ranks)

        
        

if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    hand1 = Hand()
    hand2 = Hand()
    print("\n"*2)
    for i in range(5):
        hand1.addCard(deck.deal())
        hand2.addCard(deck.deal())
    comparer = Compare(hand1,hand2)
    print(str("Hand1 Combination: "+str(hand1.getCombination())).center(os.get_terminal_size().columns))
    print(str("Hand2 Combination: "+str(hand2.getCombination())).center(os.get_terminal_size().columns))
    print("\n"*2)
    print("*"*20)
    print(str(comparer.priority()).center(os.get_terminal_size().columns))
    print("*"*20)
    print("\n"*2)




