import sqlite3
import rpw
from tabulate import tabulate
import pickle

MASTER_PASSWORD = "12345"
jar = []
conn = sqlite3.connect('.pwdb.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (ID INTEGER NOT NULL, Organization TEXT NOT NULL, Category TEXT NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL);")

def initiate():
    pwinput = input("Please input the master password to access the database: ")
    attempts = 1

    while(pwinput != MASTER_PASSWORD):
        pwinput = input("\nSorry that's the wrong password. \nPlease try again with the correct master password: ")
        attempts += 1
        if(attempts == 5 and pwinput != MASTER_PASSWORD):
            print("\nThis is your fifth incorrect attempt as such this program will be terminated. \nHave a nice day!")
            conn.close()
            exit()

        elif(pwinput == "q"):
            logout_confirmation = input("\nYou are about to close this program. Are you sure that's what you want to do?\n> ")
            while(logout_confirmation.lower() not in ["y", "yes", "n", "no"]):
                logout_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to close this program?\n> ")
            
            if(logout_confirmation.lower() in ["y", "yes"]):
                print("\nVery well. This program will be terminated.\nHave a nice day.")
                conn.close()
                exit()
            else:
                print("\nVery well. The database will continue to run.\n")
    
    print("\n\nWelcome to your secret password database!\nHere is a helpful guide for all the available commands.")


def guide():
    guide = []
    guide_headers = ["Available Commands", "Descriptions"]
    guide.append("ne (new entry): Adds a new organization, category, username, and password to the databaase.".split(":"))
    guide.append("de (delete entry): Remove entry data from the database.".split(":"))
    guide.append("ie (insert entry): Inserts entry data into a specified id in the database.".split(":"))
    guide.append("re (restore entry): Restores deleted entry data to its original state prior to deletion.".split(":"))
    guide.append("se (show entries): Prints out display of account entries.".split(":"))
    guide.append("ci (change id): Changes the id of a given organization entry.".split(":"))
    guide.append("co (change organization): Changes the name of a given organization entry.".split(":"))
    guide.append("cc (change category): Changes the category of a given organization entry.".split(":"))
    guide.append("cu (change username): Changes username for given existing organization entry.".split(":"))
    guide.append("cp (change password): Changes password for given existing organization entry.".split(":"))
    guide.append("hp (help): Prints this command guide to the terminal screen.".split(":"))
    guide.append("q (quit): Exits user interface and terminates program.".split(":"))
    print("\n")
    print(tabulate(guide, guide_headers, tablefmt = "fancy_grid"))
    print("\n")


def toString(query):
    table = []
    headers = ["ID","Organization", "Category", "Username", "Password"]
    for val in query:
        table.append(val)
    print(tabulate(table, headers, tablefmt = "fancy_grid"))

def display():
    choice = input("\nAre you looking for specific database entries?\n> ")

    while(choice.lower() not in ["y", "yes", "n", "no"]):
        choice = input("\nYour response is not clear. Please respond with yes or no.\nAre you looking for specific database entries?\n> ")

    if(choice.lower() in ["y", "yes"]):
        condition = input("\nHow would you like to search for entries?\n> ")

        while(condition.lower() not in ["cat", "category", "org", "organization", "user", "username"]):
            condition = input("\nYour response is not clear. Please respond with category, organization, or username.\nHow would you like to search for entries?\n> ")

        if(condition.lower() in ["cat", "category"]):
            cat = input("\nWhat is the category are you searching for?\n> ")
            toString(cursor.execute("SELECT * FROM accounts WHERE Category = ? ORDER BY ID", (cat.capitalize(),)))

        if(condition.lower() in ["org", "organization"]):
            org = input("\nWhat is the organization are you searching for?\n> ")
            toString(cursor.execute("SELECT * FROM accounts WHERE Organization = ? ORDER BY ID", (org.capitalize(),)))

        if(condition.lower() in ["user", "username"]):
            user = input("\nWhat is the username are you searching for?\n> ")
            toString(cursor.execute("SELECT * FROM accounts WHERE Username = ? ORDER BY ID", (user,)))

    else:
        condition = input("\nHow many entries would you like to view?\n> ")

        while(condition.lower() not in ["few", "many", "several", "all", "rfew", "rmany", "rseveral", "rall"]):
            condition = input("\nYour response is not clear. Please respond with (r)few(5), (r)many(10), (r)several(15), or (r)all.\nHow would you like to search for entries?\n> ")

        if(condition.lower() == "few"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY ID LIMIT 5"))

        if(condition.lower() == "many"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY ID LIMIT 10"))

        if(condition.lower() == "several"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY ID LIMIT 15"))

        if(condition.lower() == "all"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY ID"))

        if(condition.lower() == "rfew"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY -ID LIMIT 5"))

        if(condition.lower() == "rmany"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY -ID LIMIT 10"))

        if(condition.lower() == "rseveral"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY -ID LIMIT 15"))

        if(condition.lower() == "rall"):
            toString(cursor.execute("SELECT * FROM accounts ORDER BY -ID"))


def orgcheck(org):
    orglist = []
    orgtuple = cursor.execute("SELECT Organization FROM accounts").fetchall()
    for val in orgtuple:
        orglist.append(val[0])
    if(len(orglist) != 0):
        while(org.capitalize() not in orglist):
            org = input("\nThe organization that you entered does not exist in this database. Please try again.\nWhat is the organization that you want to remove from the database?\n> ")

    else:
        print("\nThe database is currently empty.Please try again when there are entries in the database.\nTerminating command...")
        return False

    return org


def interface():
    while(True):
        command = input("> ")

        if(command == "ne"):
            idx = cursor.execute("SELECT COUNT(ID) FROM accounts").fetchone()[0]
            org = input("\nWhat is the organization that you are making an account with?\n> ")
            cat = input("\nWhat is the category of the organization you are making an account with?\n> ")
            user = input("\nWhat username or email do you plan on using?\n> ")

            pw_question = input("\nWould you like to use the random password generator?\n> ")
            while(pw_question.lower() not in ["y", "yes", "n", "no"]):
                pw_question = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to use the random password generator?\n> ")
            
            if(pw_question.lower() in ["y", "yes"]):
                print("\nNoted. Running the random password generator now.")
                pw = rpw.makepword()
            else:
                pw = input("\nNoted. What password would you like to use?\n> ")

            cursor.execute("INSERT INTO accounts VALUES (?,?,?,?,?)", (idx+1, org.capitalize(), cat.capitalize(), user, pw))
            conn.commit()

            print("\nThe new entry has now been added to the hidden database.\n")

        if(command == "de"):
            org = input("\nWhat is the organization that you want to remove from the database?\n> ")
            org = orgcheck(org)
            
            delete_confirmation = input("\nYou are about to delete an entry. Are you sure that's what you want to do?\n> ")
            while(delete_confirmation.lower() not in ["y", "yes", "n", "no"]):
                logout_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to delete an entry from the database?\n> ")
            
            if(delete_confirmation.lower() in ["y", "yes"]):
                idx = cursor.execute("SELECT ID FROM accounts WHERE Organization = ?", (org.capitalize(),)).fetchone()[0]
                
                recentdel = cursor.execute("SELECT * FROM accounts WHERE Organization = ?", (org.capitalize(),)).fetchone()[:]
                jar.append(recentdel)

                with open('.jar.pkl', 'wb') as f:
                    pickle.dump(jar,f)

                count = cursor.execute("SELECT COUNT(ID) FROM accounts").fetchone()[0]
                idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (idx+1, count)).fetchall()[:]

                cursor.execute("DELETE FROM accounts WHERE Organization = ?", (org.capitalize(),))

                idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (idx+1, count)).fetchall()[:]
                idxs.sort()
                
                for val in idxs:
                    cursor.execute("UPDATE accounts SET ID = ? WHERE ID = ?",(val[0]-1, val[0]))

                conn.commit()

                print("\nThe entry has now been deleted from the hidden database.\n")

            else:
                print("\nVery well. The entry will not be deleted from the database.\n")

        if(command == "ie"):
            count = cursor.execute("SELECT COUNT(ID) FROM accounts").fetchone()[0]
            org = input("\nWhat is the organization that you are making an account with?\n> ")
            cat = input("\nWhat is the category of the organization you are making an account with?\n> ")
            user = input("\nWhat username or email do you plan on using?\n> ")

            pw_question = input("\nWould you like to use the random password generator?\n> ")
            while(pw_question.lower() not in ["y", "yes", "n", "no"]):
                pw_question = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to use the random password generator?\n> ")
            
            if(pw_question.lower() in ["y", "yes"]):
                print("\nNoted. Running the random password generator now.")
                pw = rpw.makepword()
            else:
                pw = input("\nNoted. What password would you like to use?\n> ")

            idx = int(input("\nWhat id would you like to insert the given organization entry on?\n> "))

            idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (idx, count)).fetchall()[:]
            idxs.sort()

            for val in reversed(idxs):
                cursor.execute("UPDATE accounts SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

            cursor.execute("INSERT INTO accounts VALUES (?,?,?,?,?)", (idx, org.capitalize(), cat.capitalize(), user, pw))
            conn.commit()

            print("\nThe new entry has now been inserted into the hidden database.\n")

        if(command == "re"):
            restore_confirmation = input("\nWould you like to restore the most recently deleted entry?\n> ")
            while(restore_confirmation.lower() not in ["y", "yes", "n", "no"]):
                restore_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to delete an entry from the database?\n> ")

            with open(".jar.pkl", "rb") as f:
                jars = pickle.load(f)

            if(restore_confirmation.lower() in ["y", "yes"]):
                try:
                    recentdel = jars.pop()
                except IndexError:
                    print("\nThere are no recently deleted entries.\nTerminating command...")
                    continue

                with open(".jar.pkl", "wb") as f:
                    pickle.dump(jars,f)

                count = cursor.execute("SELECT COUNT(ID) FROM accounts").fetchone()[0]
                idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (recentdel[0], count)).fetchall()[:]
                idxs.sort()

                for val in reversed(idxs):
                    cursor.execute("UPDATE accounts SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

                cursor.execute("INSERT INTO accounts VALUES (?,?,?,?,?)", (recentdel[0], recentdel[1], recentdel[2], recentdel[3], recentdel[4]))
                conn.commit()

                print("\nThe deleted entry has now been restored to its original state in the hidden database.\n")

            elif(restore_confirmation.lower() in ["n", "no"]):
                found = False
                org = input("\nWhat is the name of the organization that you previously deleted?\n> ")

                try:
                    for i,val in enumerate(jars):
                        if(org.capitalize() in val):
                            priordel = jars.pop(i)
                            with open(".jar.pkl", "wb") as f:
                                pickle.dump(jars,f)

                            count = cursor.execute("SELECT COUNT(ID) FROM accounts").fetchone()[0]
                            idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (priordel[0], count)).fetchall()[:]
                            idxs.sort()

                            for val in reversed(idxs):
                                cursor.execute("UPDATE accounts SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

                            cursor.execute("INSERT INTO accounts VALUES (?,?,?,?,?)", (priordel[0], priordel[1], priordel[2], priordel[3], priordel[4]))
                            conn.commit()

                            print("\nThe deleted entry has now been restored to its original state in the hidden database.\n")
                            found = True
                            continue
                except IndexError:
                    print("\nThere are no recently deleted entries.\nTerminating command...")
                    continue
                    
                if(found == False):    
                    print("\nThe organization entry you want to recover is not a prior deletion.\nTerminating command...\n")
                
        if(command == "ci"):
            org = input("\nWhat organization are you changing the id of?\n> ")
            org = orgcheck(org)

            curidx = cursor.execute("SELECT ID FROM accounts WHERE Organization = ?", (org.capitalize(),)).fetchone()[0]
            newidx = int(input("\nWhat new id for the organization would you like to change to?\n> "))

            if(curidx < newidx):
                idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (curidx+1, newidx)).fetchall()[:]
                idxs.sort()
                
                for val in idxs:
                    cursor.execute("UPDATE accounts SET ID = ? WHERE ID = ?",(val[0]-1, val[0]))

            elif(curidx > newidx):
                idxs = cursor.execute("SELECT ID FROM accounts WHERE ID BETWEEN ? AND ?", (newidx, curidx-1)).fetchall()[:]
                idxs.sort()

                for val in reversed(idxs):
                    cursor.execute("UPDATE accounts SET ID = ? WHERE ID = ?",(val[0]+1, val[0]))

            elif(curidx == newidx):
                print("This is the current index for the given organization entry.\nNo further action required. Terminating command...\n")
                continue

            cursor.execute("UPDATE accounts SET ID = ? WHERE Organization = ?",(newidx, org.capitalize()))
            conn.commit()

            print("\nThe organization id has now been changed to the new organization id.\n")

        if(command == "co"):
            org = input("\nWhat organization are you changing the name of?\n> ")
            org = orgcheck(org)

            neworg = input("\nWhat new name for the organization would you like to change to?\n> ")

            cursor.execute("UPDATE accounts SET Organization = ? WHERE Organization = ?",(neworg.capitalize(), org.capitalize()))
            conn.commit()

            print("\nThe organization name has now been changed to the new organization name.\n")

        if(command == "cc"):
            org = input("\nWhat organization are you changing the category for?\n> ")
            org = orgcheck(org)

            cat= input("\nWhat new category for the organization would you like to change to?\n> ")

            cursor.execute("UPDATE accounts SET Category = ? WHERE Organization = ?",(cat.capitalize(), org.capitalize()))
            conn.commit()

            print("\nThe organization category has now been changed to the new organization category.\n")

        if(command == "cu"):
            org = input("\nWhat organization are you changing the username for?\n> ")
            org = orgcheck(org)

            user = input("\nWhat new username or email would you like to change to?\n> ")

            cursor.execute("UPDATE accounts SET Username = ? WHERE Organization = ?",(user, org.capitalize()))
            conn.commit()

            print("\nThe username has now been changed to the new username.\n")

        if(command == "cp"):
            org = input("\nWhat organization are you changing the username for?\n> ")
            org = orgcheck(org)

            pw_question = input("\nWould you like to use the random password generator?\n> ")
            while(pw_question.lower() not in ["y", "yes", "n", "no"]):
                pw_question = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to use the random password generator?\n> ")
            
            if(pw_question.lower() in ["y", "yes"]):
                print("\nNoted. Running the random password generator now.")
                pw = rpw.makepword()
            else:
                pw = input("\nNoted. What new password would you like to change to?\n> ")

            cursor.execute("UPDATE accounts SET Password = ? WHERE Organization = ?",(pw, org.capitalize()))
            conn.commit()

            print("\nThe password has now been changed to the new password.\n")

        if(command == "se"):
            display()

        if(command == "hp"):
            guide()

        if(command == "q"):
            logout_confirmation = input("\nYou are about to logout. Are you sure that's what you want to do?\n> ")
            while(logout_confirmation.lower() not in ["y", "yes", "n", "no"]):
                logout_confirmation = input("\nYour response is not clear. Please respond with yes or no.\nWould you like to logout from the database?\n> ")
            
            if(logout_confirmation.lower() in ["y", "yes"]):
                print("\nVery well. The database will be closed and this program will be terminated.\nHave a nice day.")
                
                jars = []
                with open(".jar.pkl", "wb") as f:
                    pickle.dump(jars,f)
                
                conn.close()
                exit()
            else:
                print("\nVery well. The database will continue to run.\n")



def main():
    initiate()
    guide()
    interface()
    

if __name__ == '__main__':
    main()