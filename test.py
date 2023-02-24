import queue
from Database import *
from datetime import timedelta, date
BloodTypes = ["O-", "O+", "B-", "B+", "A-", "A+", "AB-", "AB+"]
db = Database()


# def GetDiscount(value, percentage):
#         return int(value - (value * (percentage/100)))

# print(GetDiscount(75,50))

# binaryImage = db.convertToBinaryData("Data\Prescriptions\Ali Abd El Rahman.pdf")

# # qu = queue.Queue()

# # qu.put("Ali: Hello Doctor")
# # qu.put("Amira: Hello Ali, How are you")
# # qu.put("Ali: Feeling ill")

# # print(qu.queue)
# # c = list(qu.queue)


# # textChat =""
# # for i in range(len(c)):
# #     if i == 0:
# #         textChat += c[i]
# #     else:
# #         textChat += "&,&"+c[i]

res = db.Insert("INSERT INTO reports (Issuer_ID, Reporter_ID, Reason, ReportDate) VALUES (%s, %s, %s, %s)", [
                6, 2, "Test Report",date.today()])


# # SELECT requests.Patient_ID, requests.Request_Date, users.Name, users.Gender, users.Age, vipmembers.Vip_Level FROM vipmembers INNER JOIN users ON vipmembers.memberID = users.ID INNER JOIN requests ON  users.ID  = requests.Patient_ID ORDER BY vipmembers.Vip_Level DESC,  DATE (requests.Request_Date) ASC
# # print(textChat)

# # symp = "Fever, "+ "Cough, "+"difficulty breathing, "+"Fatigue, "+"Headache, "+"loss of taste and smell, " + "Sore throat"
# # # print(symp)

# EndDate = date.today() - timedelta(days=10000)
# print(EndDate)
# res = db.Update("UPDATE users SET DateOfBirth= %s",[EndDate])
# # res1 = db.Update("UPDATE chatdata SET Chat_Status= %s WHERE Patient_ID= %s",["ongoing", 5])
# # res2 = db.Update("UPDATE requests SET Request_Status= %s WHERE Patient_ID= %s",["ongoing", 5])
db.Commit()


# # db.write_file(binaryImage,"test12.pdf")


# # print(binaryImage)
