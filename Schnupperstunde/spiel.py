import random

def zahlenratespiel():
    zufallszahl = random.randint(1, 100)
    versuche = 0
    geraten = False
    
    print("Willkommen zum Zahlenratespiel!")
    print("Ich habe mir eine Zahl zwischen 1 und 100 ausgedacht.")
    
    while not geraten:
        try:
            tipp = int(input("Gib deinen Tipp ein: "))
            versuche += 1
            
            if tipp < zufallszahl:
                print("Zu niedrig! Versuch es nochmal.")
                
            elif tipp > zufallszahl:
                print("Zu hoch! Versuch es nochmal.")
            
            else:
                print(f"Glückwunsch! Die Zahl {zufallszahl} in {versuche} Versuchen erraten!")
        
        except ValueError:
            print("Bitte gib eine gültige Zahl ein.")
    
if __name__ == "__main__":
    zahlenratespiel() 