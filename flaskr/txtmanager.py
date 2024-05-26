#Αντιθέτως με το tutorial δεν χρησιμοποιώ SQL βάση δεδομένων οπότε φτιάχνω μερικές δικες
#μου εντολές για να διαχειρίζομαι τις πληροφορίες των χρηστών
import os
import random
import hashlib
path = os.path.join('users', 'data.txt')
userlist = [] #Λίστα που περιέχει όλους τους χρήστες
id_counter= 0 #Mετράει των αριθμό των id

class user:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        self.id = id(username)
        self.data = data

def init():
    with open(path, 'r') as file:
        for line in file:
            words = line.strip().split() #Σπαει την σειρά σε λέξεις
            userlist.append(user(words[0], words[1], words[3:]))


def search(user): 
#Επιστρέφει κωδικό αν υπάρχει ο χρήστης, False αν δεν υπάρχει
    for current in userlist:
        if current.username == user:
            return current.password
    
    return False #δεν βρέθηκε

def search_id(id): 
#Επιστρέφει username αν υπάρχει ο χρήστης, αλλιώς False
    for current in userlist:
        if current.id == id:
            return current.username
    return False #δεν βρέθηκε

def new(username, password):
    
    for user in userlist: #Έλεγχος
        if username == user.username:
            raise ValueError #Υπάρχει ήδη ERROR

    password= passwordhash(password)
    with open(path, 'a') as file:
        file.write(f"\n{username} {password}")

    init() #Ξαναδιαβάζει το txt


def id(username): #H συγκεκριμένη συνάρτηση δημιουργήθηκε με chatgpt 3.5 (prompt:I need a python function that converts usernames into numbers)
    # Generate a hash value from the username
    hash_value = hash(username)
    # Convert the hash value to a positive number
    positive_number = hash_value % (10 ** 8)  # Limit to 100 million to ensure a reasonable range
    return positive_number

def passwordhash(password): #Παρόμοια με την id() αυτή η συνάρτηση δημιουργήθηκε με chatgpt 4o με prompt: "I need a fucntion to hash passwords using hashlib"
# Generate a salt and hash the password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password



def info(id):
#Επιστρέφει το αντικείμενο του χρήστη αν υπάρχει, αλλιώς False
    for current in userlist:
        if current.id == id:
            
            return current #Eπιστρέφει ολόκληρο το αντικείμενο
    return False #δεν βρέθηκε

init()