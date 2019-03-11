"""
Kyle Bigart
Final Python Project

Goal:
Create files and folders in the local directory gathered from two (.csv) files of employees and departments.
Send each single file to the server.
The program won't run a second time if the created folder "Employee-Department-Dat", with same name is available.

"""
import ftplib
import csv
import os
import glob
import random

#The roster is treated like a list even though it's define as a dictionary like departmentDict and employeeDict
roster = {}
departmentDict = {}
employeeDict = {}


#Defining the Department class from the departments.csv
class Department:
    def __init__(self, departmentId, departmentType):
        self.departmentId = departmentId
        self.departmentType = departmentType

    def displayDepartment(self):
        return "Department ID: " + str(self.departmentId) + "Department Type" + self.departmentType

#Defining the Employee class from the emps.csv
class Employee:

    def __init__(self, mainID, fisrtName, lastName, departmentId):
        self.mainID = mainID
        self.fisrtName = fisrtName
        self.lastName = lastName
        self.departmentId = departmentId

    def displayEmployeeID(self):
        return str(self.mainID)

    def displayEmployee(self):
        return self.fisrtName + "_" + self.lastName

#Reads the file named "departments.csv"
with open('departments.csv') as outputfile:
    readCSV = csv.reader(outputfile, delimiter=',')
    for row in readCSV:
        addDepartmentId = int(row[0])
        addDepartmentType = row[1]
        departmentDict[addDepartmentId] = Department(addDepartmentId, addDepartmentType)
        roster[addDepartmentId] = []

#Reads the file named "emps.csv"
with open('emps.csv') as outputfile:
    readCSV = csv.reader(outputfile, delimiter=',')
    header = next(outputfile)
    for row in readCSV:
        addMainID = int(row[0])
        addFirstName = row[1]
        addLastName = row[2]
        addEmployeeId = int(row[3])
        employeeDict[addMainID] = Employee(addMainID, addFirstName, addLastName, addEmployeeId)
        roster[addEmployeeId].append(employeeDict[addMainID])

#Random Password creator
def genPassword(lenght):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-="
    mypw = ""
    for i in range(lenght):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]
    return mypw


DataName = "Employee-Department-Data"


def createFiles():

    os.mkdir(DataName)
    os.chdir(DataName)

    for depId in roster:
        os.mkdir(departmentDict[depId].departmentType)
        os.chdir(departmentDict[depId].departmentType)

        for emp in roster[depId]:

            with open(emp.displayEmployeeID() + ".html", "w") as outputFile:
                message = """<html>
                <head><b><p>Data1</b></p></head>
                <body = style="background-color:#e7f756;"><p>Password: <font color="red">Data2</p></font>
                <p>Department: Data3</p>
                </body>
                </html>"""

                # print(singleData)
                message = message.replace("Data1", emp.displayEmployee())
                message = message.replace("Data2", genPassword(15))
                message = message.replace("Data3", departmentDict[depId].departmentType)

                outputFile.write(message)
                outputFile.close()


                """
                Okay, I got this working by installing XAMP, run FileZilla, click Admin button, you can set a admin password that is what 'password' is set to.
				If there is no password just replace 'password' to nothing in the quotes like this: ''.
                Click on Edit on the top and click on Users and create a user have it set the same name of where 'student' is.
                Last step set the settings with checked on giving all permissions for folder access.
                Set the home of where the folder is stored on the computer, for access to ftp.
                
                Also don't change '127.0.0.1' due to it being local host address, unless if there is something else running might need to change it or stop it.
                """
                session = ftplib.FTP('127.0.0.1', 'student', 'password')
                file = open(emp.displayEmployeeID() + ".html", 'rb')  # file to send
                session.storbinary('STOR '+emp.displayEmployeeID() + ".html", file)  # send the file
                file.close()  # close file and FTP
                session.quit()
        os.chdir("..")


createFiles()

