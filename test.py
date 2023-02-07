from Database import *
BloodTypes = ["O-","O+","B-","B+","A-","A+","AB-","AB+"]
db = Database()

import queue

# binaryImage = db.convertToBinaryData("COVID-996.png")

# qu = queue.Queue()

# qu.put("Ali: Hello Doctor")
# qu.put("Amira: Hello Ali, How are you")
# qu.put("Ali: Feeling ill")

# print(qu.queue)
# c = list(qu.queue)


# textChat =""
# for i in range(len(c)):
#     if i == 0:
#         textChat += c[i]
#     else:
#         textChat += "&,&"+c[i] 
# res = db.Update("UPDATE requests SET = %s, Prediction= %s WHERE Patient_ID= %s",[binaryImage,"Covid-19",7])


# print(textChat)

# symp = "Fever, "+ "Cough, "+"difficulty breathing, "+"Fatigue, "+"Headache, "+"loss of taste and smell, " + "Sore throat"
# # print(symp)

res2 = db.Update("UPDATE chatdata SET Chat_Status= %s WHERE Patient_ID= %s",["ongoing", 5])
res2 = db.Update("UPDATE requests SET Request_Status= %s WHERE Patient_ID= %s",["ongoing", 5])
db.Commit()


# db.write_file(binaryImage,"test12.pdf")


# print(binaryImage)