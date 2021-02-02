import sqlite3
from tabulate import tabulate
import pickle

jar = []
conn = sqlite3.connect('frdict.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS dictionary (ID INTEGER NOT NULL, Fre_Word TEXT NOT NULL, Eng_Trans TEXT NOT NULL, Type TEXT NOT NULL, Subtype TEXT NOT NULL, Theme TEXT NOT NULL);")

def guide():
    guide = []
    guide_headers = ["Available Commands", "Descriptions"]
    guide.append("nw (new word): Adds a new French word, English Translation, word type, subtype and theme to the dictionary.".split(":"))
    guide.append("dw (delete word): Remove word from the dictionary.".split(":"))
    guide.append("iw (insert word): Inserts word into a specified id in the dictionary.".split(":"))
    guide.append("rw (restore word): Restores deleted word to its original state prior to deletion.".split(":"))
    guide.append("sw (show words): Prints out display of account entries.".split(":"))
    guide.append("ci (change id): Changes the id of a given word.".split(":"))
    guide.append("cf (change French): Changes the French word of a given word entry.".split(":"))
    guide.append("ce (change English): Changes the English translation of a given word entry.".split(":"))
    guide.append("cty (change type): Changes word type for a given word entry.".split(":"))
    guide.append("cs (change subtype): Changes word subtype for given word entry.".split(":"))
    guide.append("cth (change theme): Changes word theme for given word entry.".split(":"))
    guide.append("hp (help): Prints this command guide to the terminal screen.".split(":"))
    guide.append("q (quit): Exits user interface and terminates program.".split(":"))
    print("\n")
    print(tabulate(guide, guide_headers, tablefmt = "fancy_grid"))
    print("\n")


def toString(query):
    table = []
    headers = ["ID", "French Word", "English Translation", "Word Type", "Word Subtype", "Theme"]
    for val in query:
        table.append(val)
    print(tabulate(table, headers, tablefmt = "fancy_grid"))

def display():
    choice = input("\nAre you looking for specific dictionary entries?\n> ")

    while(choice.lower() not in ["y", "yes", "n", "no"]):
        choice = input("\nYour response is not clear. Please respond with yes or no.\nAre you looking for specific dictionary entries?\n> ")

    if(choice.lower() in ["y", "yes"]):
        condition = input("\nHow would you like to search for entries?\n> ")

        while(condition.lower() not in ["word", "french", "fre", "translation", "trans", "english", "eng", "type", "subtype", "theme"]):
            condition = input("\nYour response is not clear. Please respond with word, translation, type, subtype or theme.\nHow would you like to search for entries?\n> ")

        if(condition.lower() in ["word", "french", "fre"]):
            word = input("\nWhat is the French word you are searching for?\n> ")
            toString(cursor.execute("SELECT * FROM dictionary WHERE Fre_Word = ? ORDER BY ID", (word.lower(),)))

        if(condition.lower() in ["translation", "trans", "english", "eng"]):
            trans = input("\nWhat is the English translation you are searching for?\n> ")
            toString(cursor.execute("SELECT * FROM dictionary WHERE Eng_Trans = ? ORDER BY ID", (trans.lower(),)))

        if(condition.lower() == "type"):
            wtype = input("\nWhat is the word type you are searching for?\n> ")
            toString(cursor.execute("SELECT * FROM dictionary WHERE Type = ? ORDER BY ID", (wtype.capitalize(),)))

        if(condition.lower() == "subtype"):
            subtype = input("\nWhat is the word subtype you are searching for?\n> ")
            toString(cursor.execute("SELECT * FROM dictionary WHERE Subtype = ? ORDER BY ID", (subtype.capitalize(),)))

        if(condition.lower() == "theme"):
            theme = input("\nWhat is the word type you are searching for?\n> ")
            toString(cursor.execute("SELECT * FROM dictionary WHERE Theme = ? ORDER BY ID", (theme.capitalize(),)))

    else:
        condition = input("\nHow many entries would you like to view?\n> ")

        while(condition.lower() not in ["few", "many", "several", "all", "rfew", "rmany", "rseveral", "rall"]):
            condition = input("\nYour response is not clear. Please respond with (r)few(5), (r)many(10), (r)several(15), or (r)all.\nHow would you like to search for entries?\n> ")

        if(condition.lower() == "few"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY ID LIMIT 5"))

        if(condition.lower() == "many"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY ID LIMIT 10"))

        if(condition.lower() == "several"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY ID LIMIT 15"))

        if(condition.lower() == "all"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY ID"))

        if(condition.lower() == "rfew"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY -ID LIMIT 5"))

        if(condition.lower() == "rmany"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY -ID LIMIT 10"))

        if(condition.lower() == "rseveral"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY -ID LIMIT 15"))

        if(condition.lower() == "rall"):
            toString(cursor.execute("SELECT * FROM dictionary ORDER BY -ID"))


def wordcheck(word):
    wordlist = []
    wordtuple = cursor.execute("SELECT Fre_Word FROM dictionary").fetchall()
    for val in wordtuple:
        wordlist.append(val[0])
    if(len(wordlist) != 0):
        while(word.lower() not in wordlist):
            word = input("\nThe word that you entered does not exist in this dictionary. Please try again.\nWhat is the word that you want to remove from the dictionary?\n> ")

    else:
        print("\nThe dictionary is currently empty. Please try again when there are entries in the dictionary.\nTerminating command...")
        return False

    return word


def interface():
    while(True):
        command = input("> ")

        if(command == "nw"):
            idx = cursor.execute("SELECT COUNT(ID) FROM dictionary").fetchone()[0]
            word = input("\nWhat is the French word that you are adding to the dictionary?\n> ")
            trans = input("\nWhat is the English translation of this word?\n> ")
            wtype = input("\nWhat type of word is this French word?\n> ")
            stype = input("\nWhat subtype of word is this French word? (ie. -er [verbs])\n> ")
            theme = input("\nWhat theme does this French word follow?\n> ")

            cursor.execute("INSERT INTO dictionary VALUES (?,?,?,?,?,?)", (idx+1, word.lower(), trans.lower(), wtype.capitalize(), stype.capitalize(), theme.capitalize()))
            conn.commit()

            print("\nThe new word has now been added to your dictionary.\n")

        if(command == "dw"):
            word = input("\nWhat is the word that you want to remove from the dictionary?\n> ")
            word = wordcheck(word)
            
            delete_confirmation = input("\nYou are about to delete an entry. Are you sure that's what you want to do?\n> ")
            while(delete_confirmation.lower() not in ["y", "yes", "n", "no"]):
                logout_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to delete an entry from the dictionary?\n> ")
            
            if(delete_confirmation.lower() in ["y", "yes"]):
                idx = cursor.execute("SELECT ID FROM dictionary WHERE Fre_Word = ?", (word.lower(),)).fetchone()[0]
                
                recentdel = cursor.execute("SELECT * FROM dictionary WHERE Fre_Word = ?", (word.lower(),)).fetchone()[:]
                jar.append(recentdel)

                with open('jar.pkl', 'wb') as f:
                    pickle.dump(jar,f)

                count = cursor.execute("SELECT COUNT(ID) FROM dictionary").fetchone()[0]
                idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (idx+1, count)).fetchall()[:]

                cursor.execute("DELETE FROM dictionary WHERE Fre_Word = ?", (word.lower(),))

                idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (idx+1, count)).fetchall()[:]
                idxs.sort()
                
                for val in idxs:
                    cursor.execute("UPDATE dictionary SET ID = ? WHERE ID = ?",(val[0]-1, val[0]))

                conn.commit()

                print("\nThe entry has now been deleted from your dictionary.\n")

            else:
                print("\nVery well. The entry will not be deleted from your dictionary.\n")

        if(command == "iw"):
            count = cursor.execute("SELECT COUNT(ID) FROM dictionary").fetchone()[0]
            word = input("\nWhat is the French word that you are adding to the dictionary?\n> ")
            trans = input("\nWhat is the English translation of this word?\n> ")
            wtype = input("\nWhat type of word is this French word?\n> ")
            stype = input("\nWhat subtype of word is this French word? (ie. -er [verbs])\n> ")
            theme = input("\nWhat theme does this French word follow?\n> ")

            idx = int(input("\nWhat id would you like to insert the given word on?\n> "))

            idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (idx, count)).fetchall()[:]
            idxs.sort()

            for val in reversed(idxs):
                cursor.execute("UPDATE dictionary SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

            cursor.execute("INSERT INTO dictionary VALUES (?,?,?,?,?)", (idx, word.lower(), trans.lower(), wtype.capitalize(), stype.capitalize(), theme.capitalize()))
            conn.commit()

            print("\nThe new entry has now been inserted into your dictionary.\n")

        if(command == "rw"):
            restore_confirmation = input("\nWould you like to restore the most recently deleted entry?\n> ")
            while(restore_confirmation.lower() not in ["y", "yes", "n", "no"]):
                restore_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to restore an entry from the dictionary?\n> ")

            with open("jar.pkl", "rb") as f:
                jars = pickle.load(f)

            if(restore_confirmation.lower() in ["y", "yes"]):
                try:
                    recentdel = jars.pop()
                except IndexError:
                    print("\nThere are no recently deleted entries.\nTerminating command...")
                    continue

                with open("jar.pkl", "wb") as f:
                    pickle.dump(jars,f)

                count = cursor.execute("SELECT COUNT(ID) FROM dictionary").fetchone()[0]
                idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (recentdel[0], count)).fetchall()[:]
                idxs.sort()

                for val in reversed(idxs):
                    cursor.execute("UPDATE dictionary SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

                cursor.execute("INSERT INTO dictionary VALUES (?,?,?,?,?,?)", (recentdel[0], recentdel[1], recentdel[2], recentdel[3], recentdel[4], recentdel[5]))
                conn.commit()

                print("\nThe deleted entry has now been restored to its original state in your dictionary.\n")

            elif(restore_confirmation.lower() in ["n", "no"]):
                found = False
                word = input("\nWhat is the French word that you previously deleted?\n> ")

                try:
                    for i,val in enumerate(jars):
                        if(word.lower() in val):
                            priordel = jars.pop(i)
                            with open("jar.pkl", "wb") as f:
                                pickle.dump(jars,f)

                            count = cursor.execute("SELECT COUNT(ID) FROM dictionary").fetchone()[0]
                            idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (priordel[0], count)).fetchall()[:]
                            idxs.sort()

                            for val in reversed(idxs):
                                cursor.execute("UPDATE dictionary SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

                            cursor.execute("INSERT INTO dictionary VALUES (?,?,?,?,?,?)", (priordel[0], priordel[1], priordel[2], priordel[3], priordel[4], priordel[5]))
                            conn.commit()

                            print("\nThe deleted entry has now been restored to its original state in your dictionary.\n")
                            found = True
                            continue
                except IndexError:
                    print("\nThere are no recently deleted entries.\nTerminating command...")
                    continue
                    
                if(found == False):    
                    print("\nThe word you want to recover is not a prior deletion.\nTerminating command...\n")
                
        if(command == "ci"):
            word = input("\nWhat word are you changing the id of?\n> ")
            word = wordcheck(word)

            curidx = cursor.execute("SELECT ID FROM dictionary WHERE Fre_Word = ?", (word.lower(),)).fetchone()[0]
            newidx = int(input("\nWhat new id for the word would you like to change to?\n> "))

            if(curidx < newidx):
                idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (curidx+1, newidx)).fetchall()[:]
                idxs.sort()
                
                for val in idxs:
                    cursor.execute("UPDATE dictionary SET ID = ? WHERE ID = ?",(val[0]-1, val[0]))

            elif(curidx > newidx):
                idxs = cursor.execute("SELECT ID FROM dictionary WHERE ID BETWEEN ? AND ?", (newidx, curidx-1)).fetchall()[:]
                idxs.sort()

                for val in reversed(idxs):
                    cursor.execute("UPDATE dictionary SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

            elif(curidx == newidx):
                print("This is the current index for the given word.\nNo further action required. Terminating command...\n")
                continue

            cursor.execute("UPDATE dictionary SET ID = ? WHERE Fre_Word = ?",(newidx, word.lower()))
            conn.commit()

            print("\nThe word id has now been changed to the new word id.\n")

        if(command == "cf"):
            word = input("\nWhat initial French word are you trying to change?\n> ")
            word = wordcheck(word)

            newword = input("\nWhat new French word would you like to change to?\n> ")

            cursor.execute("UPDATE dictionary SET Fre_Word = ? WHERE Fre_Word = ?",(newword.lower(), word.lower()))
            conn.commit()

            print("\nThe initial French word has now been changed to the new French word.\n")

        if(command == "ce"):
            word = input("\nWhat word are you changing the English translation for?\n> ")
            word = wordcheck(word)

            trans= input("\nWhat new translation for the word would you like to change to?\n> ")

            cursor.execute("UPDATE dictionary SET Eng_Trans = ? WHERE Fre_Word = ?",(trans.lower(), word.lower()))
            conn.commit()

            print("\nThe translation has now been changed to the new translation.\n")

        if(command == "cty"):
            word = input("\nWhat word are you changing the type for?\n> ")
            word = wordcheck(word)

            wtype = input("\nWhat new word type would you like to change to?\n> ")

            cursor.execute("UPDATE dictionary SET Type = ? WHERE Fre_Word = ?",(wtype.capitalize(), word.lower()))
            conn.commit()

            print("\nThe word type has now been changed to the new word type.\n")

        if(command == "cs"):
            word = input("\nWhat word are you changing the subtype for?\n> ")
            word = wordcheck(word)

            stype = input("\nWhat new word subtype would you like to change to?\n> ")

            cursor.execute("UPDATE dictionary SET Subtype = ? WHERE Fre_Word = ?",(stype.capitalize(), word.lower()))
            conn.commit()

            print("\nThe word subtype has now been changed to the new word subtype.\n")

        if(command == "cth"):
            word = input("\nWhat word are you changing the theme for?\n> ")
            word = wordcheck(word)

            theme = input("\nWhat new word theme would you like to change to?\n> ")

            cursor.execute("UPDATE dictionary SET Theme = ? WHERE Fre_Word = ?",(theme.capitalize(), word.lower()))
            conn.commit()

            print("\nThe word theme has now been changed to the new word theme.\n")

        if(command == "sw"):
            display()

        if(command == "hp"):
            guide()

        if(command == "q"):
            logout_confirmation = input("\nYou are about to quit this application. Are you sure that's what you want to do?\n> ")
            while(logout_confirmation.lower() not in ["y", "yes", "n", "no"]):
                logout_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to stop the dictionary?\n> ")
            
            if(logout_confirmation.lower() in ["y", "yes"]):
                print("\nVery well. The dictionary will be closed and this program will be terminated.\nHave a nice day.")
                conn.close()
                exit()
            else:
                print("\nVery well. The dictionary will continue to run.\n")



def main():
    print("\n\nWelcome to your personal French dictionary!\nHere is a helpful guide for all the available commands.")
    guide()
    interface()
    

if __name__ == '__main__':
    main()