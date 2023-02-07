import connectorx as cx
conn = 'mysql://root:@localhost:3306/systemdb'  

query = "SELECT Patient_ID FROM chatdata WHERE Chat_Status = 'ongoing' and Doc_ID = 4"    
r = cx.read_sql(conn, query)
print(list(r["Patient_ID"]))