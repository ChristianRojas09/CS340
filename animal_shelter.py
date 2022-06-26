#Python CRUD handler for CS-340 | Christian Rojas

from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId

userCreatedData = {} #input data for create
userSearchData = {} #Search data for read
userUpdateData = {} #input data for update
userUpdatedTarget = {} #updated entry 
userDeleteData = {} #input data for delete

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username: str, password: str) -> None:
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        self.client = MongoClient('mongodb://%s:%s@localhost:37518/?authMechanism=DEFAULT&authSource=AAC' % (username, password))
        self.database = self.client['AAC']

# method to take user input for Create
    def getCreateData(self):
        # Table to match the structure of the dictionary
        stockDict = [
          '1', 'age_upon_outcome', 'animal_id', 'animal_type', 'breed', 'color', 'date_of_birth', 'datetime', 
          'monthyear', 'name', 'outcome_subtype', 'outcome_type', 'sex_upon_outcome', 'location_lat', 
          'location_long', 'age_upon_outcome_in_weeks'
        ]

        #loop to get the input data from users
        for i in range(len(stockDict)):
            key = stockDict[i]
            value = input("Enter " + stockDict[i] + ": ")
            userCreatedData.update({key: value})

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        #try except are for testing
        try:
            if data is not None:
                self.database.animals.insert_one(data)  # data should be dictionary     

                # Store insert result
                insertResult = self.database.animals.insert_one(data)

                #return true if successful
                if insertResult is not None:
                    pprint(insertResult)
                    return True
            else:
                raise Exception("Nothing to save, because data parameter is empty")
        except:
            return False

# Get the data for read
    def getReadData(Self):
        for i in range(1):
            key = input("Search key: ")
            value = input("Search value: ")
        userSearchData.update({key: value})

# Create method to implement the R in CRUD. 
    def read(self, data):
        #try except are for testing
        try:
            if data is not None:
                readResult = list(self.database.animals.find(data,{"_id":False})) #This will fetch data if it is in the dictionary
                
                return readResult
            else:
                raise Exception("Nothing to return, because data parameter is empty")
                #return False
                
        except Exception as e:
            print("There has been an exception: ", e)

# Get data for Update
    def getUpdateData(self):
        for i in range(1):
            key = input("Update key: ")
            value = input("Update value: ")
        userUpdateData.update({key: value})

        #update target entry
        for i in range(1):
            key = input("Update key: ")
            value = input("New update value: ")
            userUpdatedTarget.update({'$set': {key: value}})
            print(userUpdatedTarget)

# Method for U in CRUD
    def update(self, fromData, toData, count):
        if fromData is not None:
            if count == 1:
                updateResult = self.database.animals.update_one(fromData, toData)

                pprint("Matched count: " + str(updateResult.matchedCount) 
                + ", Modified count: " + str(updateResult.modifiedCount))

                if updateResult.modifiedCount == 1:
                    print("Updated: " + updateResult)
                    return True
                else: 
                    print("An unexpected error has occured")
                    return False
            elif count == 2:
                updateResult = self.database.animals.update_many(fromData, toData)
                pprint("Matched count: " + str(updateResult.matchedCount) 
                + ", Modified count: " + str(updateResult.modifiedCount))

                if updateResult.modifiedCount == updateResult.matchedCount:
                    print("Updated: " + updateResult)
                    return True
                else:
                    print("An unexpected error has occured")
                    return False
            else:
                print("The count is not recognized, please try again.")
                return False
        #statement to let the user know there is an empty target parameter
        else:
            raise Exception("Error: There is an empty parameter.")
            return False

# Method to get data for delete
    def getDeleteData(self):
        for i in range(1):
            key = input("Delete key: ")
            value = input("Delete value: ")
            userDeleteData.update({key:value})

# Method for D in CRUD
    def delete(self, data, count):
        if data is not None:
            if count == 1:
                #try except are for testing
                try:
                    deleteResult = self.database.animals.delete_one(data)
                    pprint("Deleted: " + str(deleteResult.deletedCount))

                    if deleteResult.deletedCount == 0:
                        print("No data to delete " + deleteResult)
                        return True
                    else:
                        print("Item deleted: " + deleteResult)
                        return True
                except Exception as e:
                    print("An exception has occored: ", e)
            # elif for more than one delete query
            elif count == 2:
                try:
                    deleteResult = self.database.animals.delete_many(data)
                    pprint("Deleted: " + str(deleteResult.deletedCount))

                    if deleteResult.deletedCount == 0:
                        print("Nothing to be deleted " + deleteResult)
                        return True
                    else:
                        print("Items deleted: " + deleteResult)
                        return True
                except Exception as e:
                    print("An exception has occured: ", e)
                    return False
            else:
                print("Could not recognize, please try again.")
        else:
            raise Exception("An exception has occured")
            return False