import random
import keyboard
from collections import deque

card = ['S1','S2','S3','S4','S5','B1','B2','B3','B4','B5','K1','K2','K3','K4','K5','P1','P2','P3','P4','P5']

i = 5
cardDeck = []
for one in range(i):
    cardDeck.append(card[0])
    cardDeck.append(card[5])
    cardDeck.append(card[10])
    cardDeck.append(card[15])
for two in range(i-2):
    cardDeck.append(card[1])
    cardDeck.append(card[6])
    cardDeck.append(card[11])
    cardDeck.append(card[16])
for three in range(i-2):
    cardDeck.append(card[2])
    cardDeck.append(card[7])
    cardDeck.append(card[12])
    cardDeck.append(card[17])
for four in range(i-3):
    cardDeck.append(card[3])
    cardDeck.append(card[8])
    cardDeck.append(card[13])
    cardDeck.append(card[18])
for five in range(i-4):
    cardDeck.append(card[4])
    cardDeck.append(card[9])
    cardDeck.append(card[14])
    cardDeck.append(card[19])
random.shuffle(cardDeck)

User1=cardDeck[0:13]
User2=cardDeck[14:27]
User3=cardDeck[28:41]
User4=cardDeck[42:55]

Turn = 0
i = j = k = l = 0

que = deque(['0','0','0','0'])


def CardCheck(i):
    check = 0
    for j in range (3 - i):
        if que[i] in card[0:5]:
            if que[i+j+1] == card[0]:
                check += 1
            if que[i+j+1] == card[1]:
                check += 2
            if que[i+j+1] == card[2]:
                check += 3
            if que[i+j+1] == card[3]:
                check += 4
        if que[i] in card[5:10]:
            if que[i+j+1] == card[5]:
                check += 1
            if que[i+j+1] == card[6]:
                check += 2
            if que[i+j+1] == card[7]:
                check += 3
            if que[i+j+1] == card[8]:
                check += 4
        if que[i] in card[10:15]:
            if que[i+j+1] == card[10]:
                check += 1
            if que[i+j+1] == card[11]:
                check += 2
            if que[i+j+1] == card[12]:
                check += 3
            if que[i+j+1] == card[13]:
                check += 4
        if que[i] in card[15:20]:
            if que[i+j+1] == card[15]:
                check += 1
            if que[i+j+1] == card[16]:
                check += 2
            if que[i+j+1] == card[17]:
                check += 3
            if que[i+j+1] == card[18]:
                check += 4
    return check

def CardNumber(i):
    point = False
    for i in range (4):
        # 5개
        if que[i] in card[4::5]:
            print('Five')
            point = True
            break
        # 4개
        if que[i] in card[3::5]:
            if CardCheck(i) == 1:
                print('Four')
                point = True
                break
        #3개
        if que[i] in card[2::5]:
            if CardCheck(i) == 2:
                print('Three')
                point = True
                break
        #2개
        if que[i] in card[1::5]:
            if CardCheck(i) == 3:
                print('Two')
                point = True
                break
        #1개
        if que[i] in card[0::5]:
            if CardCheck(i) == 4:
                 print('One')
                 point = True
                 break

def getCard(point):
    # if User1 win
    if point is True:
        User1.extend(que)
        del User1[len(User1)-4:]
    #if User1 Lose
    elif point is False:
        User2.append(User1[0])
        User3.append(User1[1])
        User4.append(User1[2])
        del User1[0:3]


        
while True:
    
    key = keyboard.read_key()
    if key =="+":
        if(Turn%4 == 0):
            if i >= len(User1):
                print('1 Lose')
                break
            print('User1 :' + User1[i])
            que.appendleft(User1[i])
            i += 1
        elif(Turn%4 == 1):
            if j >= len(User1):
                print('2 Lose')
                break
            print('User2 :' + User2[j])
            que.appendleft(User2[j])
            j += 1
        elif(Turn%4 == 2):
            if k >= len(User1):
                print('3 Lose')
                break
            print('User3 :' + User3[k])
            que.appendleft(User3[k])
            k +=1
        else:
            if l >= len(User1):
                print('4 Lose')
                break
            print('User4 :' + User4[l])
            que.appendleft(User4[l])
            l += 1
    elif key =="q":
        print("Ring")
        getCard(CardNumber(i))
    Turn += 1
