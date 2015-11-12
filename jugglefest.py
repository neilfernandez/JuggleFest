class Juggler:
    
    def __init__(self, name, h, e, p, pref):
        self.name = name
        self.h = int(h)
        self.e = int(e)
        self.p = int(p)
        self.pref = pref
        self.choice = 0
        self.assigned = ""
        self.dotproduct = {}

    def getName(self):
        return self.name
    
    def getH(self):
        return self.h

    def getE(self):
        return self.e

    def getP(self):
        return self.p

    def getPref(self):
        return self.pref

    def getChoice(self):
        return self.choice

    def getDot(self):
        return self.dotproduct
    
    def assign(self, circuit):
        self.assigned.append(circuit)

    def kicked(self):
        self.choice += 1

    def restart(self):
        self.choice = 0

    def calcdot(self, circuits):
        for i in range(len(self.pref)):
            circPref = self.pref[i]
            circuit = circuits[circPref]
            ch = circuit.getH()
            ce = circuit.getE()
            cp = circuit.getP()
            dot= (self.h * ch) + (self.e * ce) + (self.p * cp)
            self.dotproduct[circPref] = dot

    def __str__(self):        
        return "Juggler {0}: {1}, {2}, {3} Prefs: {4} Choice: {5} Dot: {6}".format(self.name, self.h, self.e, self.p, self.pref, self.choice, self.dotproduct[self.pref[self.choice]])

    def __repr__(self):
        return "Juggler {0}".format(self.name)

class Circuit:

    def __init__(self, name, h, e, p):
        self.name = name
        self.h = int(h)
        self.e = int(e)
        self.p = int(p)

    def getH(self):
        return self.h

    def getE(self):
        return self.e

    def getP(self):
        return self.p
    
    def __repr__(self):        
        return "Circuit {0}: {1}, {2}, {3}".format(self.name, self.h, self.e, self.p)

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
        
def main():
    # Open file for reading.
    infile = open("jugglefest.txt",'r')
    output = open("out.txt", 'w')
    
    # Read in the circuits.
    circuits = readCircuits(infile)
    
## FOR TESTING PURPOSES    
##    for circuit in circuits:
##        print(circuit)
        
    # Read in the jugglers and calculate dot product.
    jugglers = readJugglers(infile)
    for i in range(len(jugglers)):
        jugglers[i].calcdot(circuits)


    # Calcuate max jugglers per circuit and the final circuits.
    maxperCirc = len(jugglers)//len(circuits)
    final = {}
    for i in range(len(circuits)):
        final[i] = []

    #Calc prefernece list length
    lastPref = len(jugglers[0].getPref()) - 1
        
    #Create a queue to place jugglers.
    q = Queue()
    for i in range(len(jugglers)):
        q.enqueue(jugglers[i])

    # Place jugglers in favorite circuit.
    while q.isEmpty() == False:
        juggler = q.dequeue()
        choice = juggler.getPref()[juggler.getChoice()]
        circuit = circuits[choice]


        # If the circuit is not full, add them to their favorite circuit!
        if len(final[choice]) < maxperCirc:
            final[choice].append(juggler)
            # Sort by dotproduct
            final[choice].sort(key=lambda x: x.dotproduct[choice], reverse=True)
        # If their favorite circuit is full, compare them to the juggler with
        # the weakest dot product in that circuit
        else:
            lastplaced = final[choice][-1]
            dotlastplaced = lastplaced.getDot()[choice]
            dotnew = juggler.getDot()[choice]
            
            if dotnew > dotlastplaced:
                # Kick out the weakest juggler in that circuit.
                final[choice].remove(lastplaced)
                # If the weak juggler is already in their least favorite circuit,
                # then try placing them by starting at the beginning of their
                # preference list.
                if lastplaced.getChoice() == lastPref:
                    lastplaced.restart()
                else:
                    lastplaced.kicked()
                q.enqueue(lastplaced)
                final[choice].append(juggler)
                final[choice].sort(key=lambda x: x.dotproduct[choice], reverse=True)

            else:
                if juggler.getChoice() == lastPref:
                    juggler.restart()
                else:
                    juggler.kicked()
                    q.enqueue(juggler)

    printout(final, output)

    



def printout(final, output):
    finalString = ""
    for i in range(len(final)-1,-1,-1):
        finalString += "C" + str(i) + " " 
        for j in range(len(final[i])):
            finalString += "J"
            juggler = final[i][j]
            name = juggler.getName()
            finalString += str(name) + " " 
            prefs = juggler.getPref()
            dot = juggler.getDot()
            for item in prefs:
                finalString +="C" + str(item)  + ":"
                value = dot[item]
                if item != prefs[-1]:
                    finalString+= str(value) + " "
                else:
                    finalString+=str(value)
            if juggler == final[i][-1]:
                pass
            else:
                finalString += ", "
        finalString += "\n"
    print(finalString, file = output)
            
                

def readCircuits(infile):
    circuits = []
    line = infile.readline()
    while line != "\n":
        split = line.split()
        name = split[1]
        h = split[2]
        e = split[3]
        p = split[4]
        circuits.append(Circuit(name[1:], h[2:], e[2:], p[2:]))
        line = infile.readline()
    return circuits

def readJugglers(infile):
    jugglers = []
    for line in infile:
        split = line.split()
        name = split[1]
        h = split[2]
        e = split[3]
        p = split[4]
        prefs = split[5].split(",")
        intPrefs = []
        for i in range(len(prefs)):
            intPrefs.append(int(prefs[i][1:]))
        jugglers.append(Juggler(name[1:], h[2:], e[2:], p[2:], intPrefs))
    return jugglers


if __name__ == "__main__":
    main()
