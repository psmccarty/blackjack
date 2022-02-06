import random
import copy
import time

faces = {'ace': (1, 11), 'two': 2, 'three': 3, 'four': 4, 'five': 5, 
         'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 
         'jack': 10, 'queen': 10, 'king': 10}
suits = ['hearts', 'clubs', 'spades', 'diamonds']
wallet = 40

def new_card(n=1):
    face = random.choices(list(faces.keys()), k=n)
    suit = random.choices(suits, k=n)
    hand = []
    for i in range(n):
        card = [face[i], suit[i]]
        hand.append(card)
    return hand


def count(li):
    counts = [0]
    for card in li:
        counts = list(set(counts))
        if card[0] != 'ace':
            for c, v in enumerate(counts):
                counts[c] += faces[card[0]]
        else:
            clone = copy.copy(counts)
            for c, v in enumerate(counts):
                counts[c] += faces[card[0]][0]
                clone[c] += faces[card[0]][1]
            for num in clone:
                counts.append(num)
    return counts


def player_move(cards):
    decission = input('Your move(h, s): ')
    while decission != 'h' and decission != 's':
        print('Invalid move, try again.')
        decission = input('Your move(h, s): ')
    if decission == 'h':
        cards.append(new_card()[0])
        player_count = count(cards)
        available_counts = []
        for item in player_count:
            if item <= 21:
                available_counts.append(item)
        potential_bust = min(player_count)
        player_count = available_counts[:]
        if player_count == []:
            for c, v in enumerate(cards):
                if c == 0:
                    f = f'Your hand is {v[0]} of {v[1]}'
                elif c == len(cards) - 1:
                    f += f' and {v[0]} of {v[1]}.'
                else:
                    f += f', {v[0]} of {v[1]}'
            print(f)
            time.sleep(1)
            print(f'You bust with a count of {potential_bust}')
            return -1
        else:
            for c, v in enumerate(cards):
                if c == 0:
                    f = f'Your hand is {v[0]} of {v[1]}'
                elif c == len(cards) - 1:
                    f += (f' and {v[0]} of {v[1]}. '
                    + f'Your count is {player_count}')
                else:
                    f += f', {v[0]} of {v[1]}'
            print(f)
            time.sleep(1)
            return player_move(cards)
    elif decission == 's':
        player_count = count(cards)
        available_counts = []
        for c in player_count:
            if c <= 21:
                available_counts.append(c)
        player_count = max(available_counts)
        print(f'You stand with {player_count}')
        return player_count

    
def dealer_move(cards):
    dealer_count = count(cards)
    for c, v in enumerate(cards):
        if c == 0:
            f = f'Dealer\'s hand is {v[0]} of {v[1]}'
        elif c == len(cards) - 1:
            f += f' and {v[0]} of {v[1]}. The count is {dealer_count}'
        else:
            f += f', {v[0]} of {v[1]}'
    print(f)
    bust_li = []
    stand_li =[]
    hit_li = []
    for i in dealer_count:
        if i > 21:
            bust_li.append(i)
        elif i >= 17 and i <= 21:
            stand_li.append(i)
        elif i < 17:
            hit_li.append(i)
    if stand_li != []:
        time.sleep(1)
        print(f'Dealer stands with {max(stand_li)}')
        return max(stand_li)
    elif hit_li != []:
        time.sleep(1)
        new = new_card()
        print('Dealer hits')
        time.sleep(1)
        print(f'New card is {new[0][0]} of {new[0][1]}')
        time.sleep(1)
        return dealer_move(cards + new)
    else:
        time.sleep(1)
        print(f'Dealer busts with {min(bust_li)}')
        return 0
    
    
def check_win(player_out, dealer_out, w):
    time.sleep(1)
    if player_out > dealer_out:
        print("Congratulations! You won the hand!")
        w += 10
        print(f'You have {w} to play with')
        return w
    elif player_out < dealer_out:
        print("Dealer wins the hand.")
        w -= 10
        print(f'You have {w} to play with')
        return w
    else:
        print("It's a tie.")
        return w
        
        
wallet = 40
print("You have 40 chips to play with. Each hand is a 10 chip bet."  
    + "\nIf you get to 80 chips you win! If you lose all your chips you loose. \nGood luck!")

while True:
    time.sleep(1)
    player_hand = new_card(2)
    dealer_hand = new_card(2)
    print(f'Your hand is {player_hand[0][0]} of {player_hand[0][1]} and '
          + f'{player_hand[1][0]} of {player_hand[1][1]}. Your count is {count(player_hand)}')
    time.sleep(1)
    print(f'Dealer is showing {dealer_hand[0][0]} of {dealer_hand[0][1]}')
    p = player_move(player_hand)
    d = dealer_move(dealer_hand)
    wallet = check_win(p, d, wallet)
    
    if wallet == 80:
        print("Well done! You have beaten project blackjack 2! \nThanks for playing!")
        break
    elif wallet == 0:
        print("Unfortunate... You have run out of money. Better luck next time.")
        break
    else:
        var = input("Do you wish to keep playing?(y/n): ")
        while var != "n" and var != "y":
            print("Invalid input")
            var = input("Do you wish to keep playing?(y/n): ")
        if var == "n":
            print("Ok. See you next time.")
            break
        