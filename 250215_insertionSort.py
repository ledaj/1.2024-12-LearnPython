hand = [5,2,4,6,1,3]
max = len(hand)


print(hand)

for instance in range(1,max):
    card = hand[instance]
    instanceMinus = instance - 1
    while instanceMinus >= 0 and hand[instanceMinus] > card:
        hand[instanceMinus + 1] = hand[instanceMinus]
        #décrémentation pour le loop d'après
        instanceMinus = instanceMinus - 1 
    hand[instanceMinus + 1] = card
    print(hand)

sum = 0

for instance in range(0, max):
    sum = sum + hand[instance]
    print(sum)

for instance in range(1,max):
    card = hand[instance]
    instancePlus = instance + 1
    while instancePlus <= 0