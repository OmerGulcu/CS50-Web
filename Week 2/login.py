#Construct an accounts list
def constructAccountsList():
    accountsFile = open("accounts.txt","r")

    lineCount = 0
    for line in accountsFile:
        lineCount += 1

    accountsFile.close()
    accountsFile = open("accounts.txt","r")
    accountsList = []

    for i in range(0, lineCount, 2):
        account = []
        account.append(accountsFile.readline()[0:-1])
        account.append(accountsFile.readline()[0:-1])
        accountsList.append(tuple((account)))
    
    accountsFile.close()

    return accountsList



#Update the accounts list
def updateAccountsList(username_, password_):
    accountsFile = open("accounts.txt", "a")
    accountsFile.write(username_ + "\n")
    accountsFile.write(password_ + "\n")
    accountsFile.close



accountsList = constructAccountsList()

usernames = []
for account in accountsList:
    usernames.append(account[0])

loginSelect = input("Hello. Enter 'L' to  login to an existing account, 'C' to create a new account.\n")
while loginSelect not in ["L", "l", "C", "c"]:
    loginSelect = input("Please enter 'L' (login to an existing account) or 'C' (create a new account).\n")

if loginSelect in ["L", "l"]:
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if (username, password) in accountsList:
            break
        else:
            print("Invalid username or password.")

            retrySelect = input("Enter 'R' to retry or 'Q' to quit.\n")
            while retrySelect not in ["R", "r", "Q", "q"]:
                retrySelect = input("Please enter 'R' (retry) or 'Q' (quit).\n")
            
            if retrySelect in ["Q", "q"]:
                quit()
else:
    username = input("Select a username: ")
    while username in usernames:
        print("This username already exists.")
        username = input("Select a username: ")
    password = input("Select a password: ")
    updateAccountsList(username, password)

print(f"Welcome, {username}.")