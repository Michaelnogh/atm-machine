import json

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
