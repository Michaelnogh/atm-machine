import json

<<<<<<< HEAD

eror_list =[]
history1 =[]
history2 =[]
history3 =[]
=======
from datetime import *
import os

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(MAIN_DIR, "data.json")

def all_clients(filename=DATA_FILE):
    
    #read the data.json and store client data in data var 
    with open(filename, "r") as file:
        data = json.load(file)
        return data

def main():
    print(all_clients())

if __name__ == "__main__":
    main()    
>>>>>>> 3b48e5bc2bb5e76f38ab7a7d87857dd929d88a5c
