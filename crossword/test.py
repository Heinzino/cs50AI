footballers_goals = {'Eusebio': 120, 'Cruyff': 104, 'Pele': 150, 'Ronaldo': 132, 'Messi': 125}


def returnSortedKeys(dictd):
    return sorted(dictd.keys(), key= lambda x:dictd[x]) 

print(returnSortedKeys(footballers_goals))
