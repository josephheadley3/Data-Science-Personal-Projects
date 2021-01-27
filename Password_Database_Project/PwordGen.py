import random

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*+=:;?"
clength = len(characters)-1 

def makepword():
    choice = input("Please state the number of characters you want your random password to have: ")
    
    test = True if int(choice) > 8 and int(choice) < 32 else False
    while(test != True):
        try:
            test = True if int(choice) > 8 and int(choice) < 32 else False
            choice = input("\nValue given is either less than 8, greater than 32, or not a number. Please try again.\nPlease state the number of characters you want your random password to have: ")
        except:
            choice = input("\nValue given is either less than 8, greater than 32, or not a number. Please try again.\nPlease state the number of characters you want your random password to have: ")
    
    plength = int(choice)
    pslength = plength//4
    pword = ""
    if plength >= 8 and plength <= 32:
        for num in range(pslength):
            charac = characters[random.randint(0,clength)]
            spcharac1 = characters[random.randint(0,51)]
            spcharac2 = characters[random.randint(52,61)]
            spcharac3 = characters[random.randint(62,clength)]
            z = random.randint(1,24)
            if z == 1:
                pword += charac+spcharac1+spcharac2+spcharac3
            if z == 2:
                pword += charac+spcharac1+spcharac3+spcharac2 
            if z == 3:
                pword += charac+spcharac2+spcharac1+spcharac3
            if z == 4:
                pword += charac+spcharac2+spcharac3+spcharac1
            if z == 5:
                pword += charac+spcharac3+spcharac1+spcharac2
            if z == 6:
                pword += charac+spcharac3+spcharac2+spcharac1
            if z == 7:
                pword += spcharac1+charac+spcharac2+spcharac3
            if z == 8:
                pword += spcharac1+charac+spcharac3+spcharac2
            if z == 9:
                pword += spcharac1+spcharac2+charac+spcharac3
            if z == 10:
                pword += spcharac1+spcharac2+spcharac3+charac
            if z == 11:
                pword += spcharac1+spcharac3+charac+spcharac2
            if z == 12:
                pword += spcharac1+spcharac3+spcharac2+charac
            if z == 13:
                pword += spcharac2+charac+spcharac1+spcharac3
            if z == 14:
                pword += spcharac2+charac+spcharac3+spcharac1
            if z == 15:
                pword += spcharac2+spcharac1+charac+spcharac3
            if z == 16:
                pword += spcharac2+spcharac1+spcharac3+charac
            if z == 17:
                pword += spcharac2+spcharac3+charac+spcharac1
            if z == 18:
                pword += spcharac2+spcharac3+spcharac1+charac
            if z == 19:
                pword += spcharac3+charac+spcharac1+spcharac2
            if z == 20:
                pword += spcharac3+charac+spcharac2+spcharac1
            if z == 21:
                pword += spcharac3+spcharac1+charac+spcharac2
            if z == 22:
                pword += spcharac3+spcharac1+spcharac2+charac
            if z == 23:
                pword += spcharac3+spcharac2+charac+spcharac1
            if z == 24:
                pword += spcharac3+spcharac2+spcharac1+charac 
        if plength%4 != 0:
            count = plength%4
            for thing in range(count):
                excharac = characters[random.randint(0,clength)]
                pword += excharac
        return pword
    else:
        print("The length must be between 8 and 32 characters. Keep that in mind and try again.")
        plength = int(input("Please state the number of characters you want your random password to have:"))
        return makepword()

if __name__ == '__main__':
    print(makepword())