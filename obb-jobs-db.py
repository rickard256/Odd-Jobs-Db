"""
This is the Python Program that allows us to edit
the firestore database that we have.
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


def initialize_firestore():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "odd-jobs-db-firebase-adminsdk-qffl1-613ea60f5c.json"

    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'projectId': 'odd-jobs-db',})

    db = firestore.client()
    return db

def find_user(db, name):
    result = db.collection("users").document(name).get()
    if result.exists:
        location = result.to_dict()
        return location
    else:
        return None

def find_job(db, name):
    result = db.collection("jobs").document(name).get()
    if result.exists:
        location = result.to_dict()
        return location

def main():
    db = initialize_firestore()

    username = input("Enter username: ")
    exist = find_user(db, username)
    checkUsername = None

    while exist is None:
        createUser = input("Could not find username, create new user? (y/n) ")
        if createUser == 'n':
            username = input("Enter a different username: ")
            exist = find_user(db, username)
        if createUser == 'y':
            realName = input("Please enter your first and last name: ")
            while username != checkUsername:
                username = input("Please enter the username you wish to use: ")
                checkUsername = input("Enter your username again: ")
                if username != checkUsername:
                    print("Usernames do not match, try again.")
            print("Welcome to the database " + realName)
            print('To access the database next time, please use the username "' + username + '"')
            userEmail = input("Please enter your email address: ")
            userPhone = input("Please enter your phone number (Optional): ")
            print("Creating user profile...")
            profile = {"name" : realName, "email" : userEmail, "phone_number" : userPhone}
            db.collection("users").document(username).set(profile)
            print("Profile created.")
            exist = find_user(db, username)

    quitProgram = False
    print("Welcome to the database " + username)
    while not quitProgram:
        print("What would you like to do?")
        print("1: Create a job posting")
        print("2: Erase a job posting")
        print("3: Edit a job posting")
        print("4: Leave the database")
        command = input("> ")
        if command == '1':
            jobName = input("What is your job: ")
            jobTime = input("How long will your job take: ")
            jobPay = input("How much will your job pay in total (Enter a number): ")
            jobDesc = input("Type a job description: ")
            job = {'job_length' : jobTime, 'job_pay' : jobPay, 'job_desc' : jobDesc, 'job_poster' : username}
            db.collection("jobs").document(jobName).set(job)
            print("Job created")
        elif command == '2':
            jobNameEdit = input('Type the name of the job you would like to erase, or type "!back" to cancel: ')
            jobExists = find_job(db, jobNameEdit)
            if jobNameEdit != '!back':
                while jobExists is None:
                    jobNameEdit = input('That job does not exist, please type another name or "!back"')
                    if jobNameEdit == '!back':
                        break
                    jobExists = find_job(db, jobNameEdit)
                if jobNameEdit != '!back':
                    deleteInput = input("Are you sure you want to delete this job? (y/n) ")
                    if deleteInput == 'y':
                        db.collection("jobs").document(jobNameEdit).delete()


        elif command == '3':
            jobNameEdit = input('Type the name of the job you would like to edit, or type "!back" to cancel: ')
            jobExists = find_job(db, jobNameEdit)
            if jobNameEdit != '!back':
                while jobExists is None:
                    jobNameEdit = input('That job does not exist, please type another name or "!back"')
                    if jobNameEdit == '!back':
                        break
                    jobExists = find_job(db, jobNameEdit)
                if jobNameEdit != '!back':
                    """currentJobInfo = db.collection("jobs").document(jobNameEdit).get()"""
                    print("Which part of the job would you like to edit?")
                    print("1. Job Description")
                    print("2. Job Pay")
                    print("3. Job Time")
                    print("4. Cancel")
                    editInput = input("> ")
                    while editInput != '4':
                        if editInput == '1':
                            job_ref = db.collection("jobs").document(jobNameEdit)
                            job = job_ref.get().to_dict()
                            currentJobDesc = job["job_desc"]
                            print('The current job description is "' + currentJobDesc + '"')
                            newJobDesc = input("Type new job description: ")
                            job["job_desc"] = newJobDesc
                            db.collection("jobs").document(jobNameEdit).set(job)
                            print("Job description changed")
                            print("")
                            break
                        elif editInput == '2':
                            job_ref = db.collection("jobs").document(jobNameEdit)
                            job = job_ref.get().to_dict()
                            currentJobPay = job["job_pay"]
                            print('The current job pay is "' + currentJobPay + '"')
                            newJobPay = input("Type new job description: ")
                            job["job_pay"] = newJobPay
                            db.collection("jobs").document(jobNameEdit).set(job)
                            print("Job pay changed")
                            print("")
                            break
                        elif editInput == '3':
                            job_ref = db.collection("jobs").document(jobNameEdit)
                            job = job_ref.get().to_dict()
                            currentJobTime = job["job_length"]
                            print('The current job length is "' + currentJobTime + '"')
                            newJobTime = input("Type new job description: ")
                            job["job_length"] = newJobTime
                            db.collection("jobs").document(jobNameEdit).set(job)
                            print("Job pay changed")
                            print("")
                            break
                        elif editInput == '4':
                            print("Returning to the main menu...")
                            print("")
                        else:
                            editInput = input("Invalid option, please try again: ")
        elif command == '4':
            print("Thank you for using the database, logging off")
            quitProgram = True
        else:
            print("Invalid command, please try again")
            print("")
if __name__ == "__main__":
    main()