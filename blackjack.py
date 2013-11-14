#!/usr/local/bin/python

from Tkinter import *
import random

class Card:
	def __init__(self, rank, suit):
		self.suit = suit
		self.rank = rank

   	def __str__(self):
   		return "[ %s %s ]" % (self.rank, self.suit[0])

   	def __repr__(self):
   		return "[ %s of %s ]" % (self.rank, self.suit)

   	def __cmp__(self, other):
   		return self.rank - other.rank


class Deck:
	"""class containing 52 cards and methods to manipulate them
	"""

	SUITS = ["Hearts", "Clubs", "Diamonds", "Spades"]
   	RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

   	def __init__(self):
		""" initialise deck object. makes 52 Cards from suits and ranks"""
		self.cards = [Card(rank, suit) for suit in Deck.SUITS for rank in Deck.RANKS]
		random.shuffle(self.cards)

	def drawOne(self):
		""" remove first card and return it """
		try:
			card = self.cards.pop()
		except IndexError:
			self.cards = Deck().cards
			card = self.cards.pop()
		return card

	def dealBJ(self, player, dealer):
		""" deal two cards to two hands, player then dealer"""
		player.cards = []
		dealer.cards = []
		for i in xrange(2):
			player.cards.append(self.drawOne())
			dealer.cards.append(self.drawOne())

class Hand:
	""" class to hold cards and scores """

	def __init__(self):
		self.cards = []
		self.cash = 50

	def twist(self, deck):
		""" function to add card to hand """
		self.cards.append(deck.drawOne())

	def getScore(self):
		""" function to calculate score from a hand object
		 if card has numerical value, add it to the total
		 if the card is an ace, add eleven to total and increase acecount
		 if card is a face, add ten to total, return total """
		total = 0
		acecount = 0

		for card in self.cards:
			if card.rank.isdigit():
				total += int(card.rank)
			elif card.rank == 'A':
				total += 11
				acecount += 1
			else:
				total = total + 10

		# if ace makes you bust, count as one
		if total > 21 and acecount >0:
			total -= acecount * 10

		return total

	def __str__(self):
		return " ".join(str(card) for card in self.cards)


class BlackJack(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master, bg="green", width=300)
		self.deck = Deck()
		self.player = Hand()
		self.dealer = Hand()
		self.grid()
		self.createWidgets()

	def twist(self):
		self.player.twist(self.deck)
		if self.player.getScore() > 21:
			self.bust()
		else:
			self.playerLabel.config(text="Your Hand:\n %s \nscore %d" % (str(self.player), self.player.getScore()))

	def bust(self):
		self.playerLabel.config(text="Your Hand:\n %s \nscore %d" % (str(self.player), self.player.getScore()))
		self.twistButton.config(state="disabled")
		self.stickButton.config(state="disabled")
		self.winnerLabel.config(text="You are BUST")
		self.player.cash-=10
		self.cashLabel.config(text="You have %d bar on you gadge "%self.player.cash)
		self.dealButton.config(state="normal")

	def deal(self):
		if self.player.cash > 0:
			self.deck.dealBJ(self.player, self.dealer)
 			self.twistButton.config(state="normal")
			self.stickButton.config(state="normal")
			self.dealButton.config(state="disabled")
			self.dealerLabel.config(text="Dealer's Hand:\n %s [    ]\n "%str(self.dealer.cards[0]))
			self.playerLabel.config(text="Your Hand:\n %s \nscore %d" % (str(self.player), self.player.getScore()))
			self.winnerLabel.config(text="")
		else:
			self.winnerLabel.config(text="You are broke, get out of here")
			self.dealButton.config(state="disabled")

	def stick(self):
		self.dealerLabel.config(text="Dealer's Hand:\n %s \nscore %d" % (str(self.dealer), self.dealer.getScore()))
		self.playerLabel.config(text="Your Hand:\n %s \nscore %d" % (str(self.player), self.player.getScore()))
		self.twistButton.config(state="disabled")
		self.stickButton.config(state="disabled")
		self.dealButton.config(state="normal")
		while self.dealer.getScore() < 17:
			self.dealer.twist(self.deck)

		self.dealerLabel.config(text="Dealer's Hand:\n %s \nscore %d" % (str(self.dealer), self.dealer.getScore()))

		score = self.player.getScore()
		against = self.dealer.getScore()
		if against == 21:
			self.winnerLabel.config(text="Dealer has BlackJack!!")
			self.player.cash -= 10
		elif score == 21:
			self.player.cash += 20
			self.winnerLabel.config(text="BlackJack!! You Win!!")
		elif len(self.player.cards) == 5:
			self.winnerLabel.config(text="Five Card Trick!! You Win!!")
			self.player.cash += 20
		elif against > 21:
			self.player.cash += 10
			self.winnerLabel.config(text="Dealer is bust. You Win!!")
		elif score <= against:
			self.player.cash -= 10
			self.winnerLabel.config(text="You Lose")
		else:
			self.player.cash += 10
			self.winnerLabel.config(text="You Win!!!")
		self.cashLabel.config(text="You have %d bar on you gadge "%self.player.cash)

	def createWidgets(self):
		myfont=("Helvetica", "16")
		self.quitButton = Button ( self, text="Quit", command=self.quit, font=myfont, fg="red", width=4, bd=4)
		self.twistButton = Button(self, text="twist", command=self.twist, state="disabled", font=myfont, width=4, bd=4)
		self.dealButton = Button(self, text="deal", command=self.deal, font=myfont, width=4, bd=4)
		self.stickButton = Button(self, text="stick", command=self.stick, state="disabled", font=myfont, width=4, bd=4)
		self.dealerLabel = Label(self, text="pedros casino\n\n", bg="green", font=myfont)
		self.playerLabel = Label(self, text="blackjack\n\n", bg="green", font=myfont)
		self.cashLabel = Label(self, text="You have %d bar on you gadge "%self.player.cash, bg="green", font=myfont)
		self.winnerLabel = Label(self, text="", bg="green", font=myfont)
		self.dealerLabel.grid(sticky=E+W)
		self.playerLabel.grid(sticky=E+W)
		self.cashLabel.grid(sticky=E+W, padx=8, pady=8)
		self.twistButton.grid(row=3, sticky=E, padx=8, pady=8, ipadx=8, ipady=8)
		self.stickButton.grid(row=3, sticky=W, padx=8, pady=8, ipadx=8, ipady=8)
		self.dealButton.grid(row=4, sticky=W, padx=8, pady=8, ipadx=8, ipady=8)
		self.quitButton.grid(row=4, sticky=E, padx=8, pady=8, ipadx=8, ipady=8)
		self.winnerLabel.grid(row=5, sticky=E+W)

if __name__=="__main__":

	bj = BlackJack()
	bj.master.title("Black Jack")

	bj.mainloop()
