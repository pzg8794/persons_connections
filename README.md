# Steps to run the program:
1) clone repository:   
git clone git@github.com:pzg8794/persons_connections.git  
2) access directory:  
cd persons_connections 
3) run program:  
python3 test_persons -id 0  
Note: you can use any id from 0 to 3  

# Unit Tests:
1) Connected Persons by Company:   
python3 test_persons.py -id 0 -conn company   
2) Connected Persons by Contacts:  
python3 test_persons.py -id 0 -conn contacts  
3) Connected Persons by Company/Contacts:  
python3 test_persons.py -id 0  
Note: you can use any id from 0 to 3  

# The Logic:
The program is composed of three main components, a Person object, a Contact Object, and a Persons object  
Each object has a unique purpose from a data perspective, and each represents a unique entity  
The Persons objects manages the relationship between each entity to assure that requirements are met
