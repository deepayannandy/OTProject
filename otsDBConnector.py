import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("ots-pocket-firebase-adminsdk-5q0jt-fceeeffe12.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

def getUserList():
  userdata= db.collection("users").get()
  users=[]
  for data in userdata:
    users.append(data.to_dict())
  #print(users)
  return users

def getProjectList():
  userproj= db.collection("userProjects").get()
  proj=[]
  for data in userproj:
    proj.append(data.to_dict())
  #print(proj)
  return proj

def getEQPList():
  eqp= db.collection("equipments").get()
  eqps=[]
  for data in eqp:
    eqps.append(data.to_dict())
  #print(eqps)
  return eqps
def getCONList():
  con= db.collection("consumableItems").get()
  cons=[]
  for data in con:
    cons.append(data.to_dict())
  #print(cons)
  return cons
def addEquipment():
  eq={"A":3,"B":1,"C":4,"D":6,"E":2,"F":5,"G":1}
  j=0
  for i in eq.keys():
    data={'EqName':"Equipment "+i,"Descriptions":"","DispatchQuantityforProjects":0,"InStock":eq[i],"AvailableQuantity":eq[i],"eqId":"EQ00"+str(j)}
    db.collection("equipments").document("EQ00"+str(j)).set(data)
    j=j+1

def addConsumeables():
  eq={"X Ray Film":5,"Mask":50,"Safety Gloves":50}
  j=0
  for i in eq.keys():
    data={'ConName':i,"StockQuantity":eq[i],"NewpurchaseQuantity":eq[i],"DispatchQuantityforProject":0,"conId":"CON00"+str(j)}
    db.collection("consumableItems").document("CON00"+str(j)).set(data)
    j=j+1

def updateConsumable(data):
  db.collection("consumableItems").document(data["conId"]).set(data)

def createProjct(data):
  db.collection("userProjects").document(data["po"]).set(data)

def createWorkOrder(data):
  db.collection("Workorders").document(data["wo"]).set(data)
def getwo():
  workorder = db.collection("Workorders").get()
  wos = []
  for data in workorder:
    wos.append(data.to_dict())
  return wos