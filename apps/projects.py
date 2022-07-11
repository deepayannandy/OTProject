import streamlit as st
from PIL import Image
import os
import qrcode

from streamlit_option_menu import option_menu

isworkorder=False
base_path=os.getcwd()
conp = {}
equip={}
avlprojects=[]
def createDataFrame(rawdata):
    address=[]
    clientName=[]
    jobDescriptions=[]
    po=[]
    workorders=[]
    for i in rawdata:
        po.append(i["po"])
        jobDescriptions.append(i["jobDescriptions"])
        clientName.append(i["clientName"])
        address.append(i["address"])
        work = ""
        for workorder in i["workorders"]:
            work = work + workorder + ","
        workorders.append(work)
        # emplist=""
        # for emp in i["assignedEmployee"]:
        #     emplist+=emp.split('(')[0]+"\n"
        # employeeid.append(emplist)
        # eqplist=""
        # j=0
        # for eqp in i["equipments"]:
        #     eqplist+=eqp+"("+str(i["equipQ"][j])+")\n"
        #     j+=1
        # equipments.append(eqplist)
        #
        #
        # conlist = ""
        # j = 0
        # for con in i["consumables"]:
        #     conlist += con + "(" + str(i["consQ"][j]) + ")\n"
        #     j += 1
        # consumables.append(conlist)
    #print(employeeid)
    global avlprojects
    avlprojects= po
    df={"PO":po,"ClientName":clientName,"JobDescriptions":jobDescriptions,"WorkOrders":workorders}
    return df
def streamlit_menu():
    options = ["Projects List","WorkOrders","Create Project"]  # requiredß
    icons = ["card-list","hammer","plus-square"]  # optional

    selected = option_menu(
            menu_title=None,  # required
            options=options, # required
            icons=icons,  # optional
            menu_icon="cast",  # optional nww
            default_index=0,  # optional
            orientation="horizontal",
        )
    return selected
def getworkorder(swo):
    wo = []
    employeeid = []
    equipments = []
    po = []
    consumables = []
    for i in swo:
        po.append(i["po"])
        wo.append(i["wo"])
        emplist=""
        for emp in i["assignedEmployee"]:
            emplist+=emp.split('(')[0]+" ,"
        employeeid.append(emplist)
        eqplist=""
        j=0
        for eqp in i["equipments"]:
            eqplist+=eqp+"("+str(i["equipQ"][j])+")\n"
            j+=1
        equipments.append(eqplist)


        conlist = ""
        j = 0
        for con in i["consumables"]:
            conlist += con + "(" + str(i["consQ"][j]) + ")\n"
            j += 1
        consumables.append(conlist)
    # print(employeeid)
    df = {"PO": po, "Work Order":wo,"Employee":employeeid,"Equipments":equipments,"Consumables":consumables}
    return df
def showprojects(projects,otdb):
    global isworkorder
    df = createDataFrame(projects)
    st.table(df)
    if isworkorder==False :
        addWO=st.button("Create WorkOrder")
        if addWO:
            isworkorder=True
    if isworkorder:
        showWOCreate(otdb)
def showwotable(wo):
    df = getworkorder(wo)
    st.table(df)
def openImage(path):
    im=Image.open(path)
    return im
def inDB(otdb,type,id):
    if type=="wo":
        res = otdb.db.collection("Workorders").where("wo", "==", id).get()
        if len(res)==1:
            return True
        else:
            return False
    if type=="po":
        res = otdb.db.collection("userProjects").where("po", "==", id).get()
        if len(res)==1:
            return True
        else:
            return False

def showWOCreate(otdb):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    condata = conitemname(otdb)
    eqpdata = equipname(otdb)
    global isworkorder
    global avlprojects
    st.title("Add new workorder")
    col1, col2 = st.columns((1, 3))
    po = col1.selectbox("Select Consumable Product", avlprojects)
    with col2:
        wo= st.text_input("WorkOrder Number")
        st.write("WO ID Naming Convention: XXX123")
    databaselink, name=createuserList(otdb)
    empid = st.multiselect("Select Employees", name)
    st.write("Consumable Product")
    col3, col4 = st.columns((2, 3))
    conlist = col3.selectbox("Select Consumable Product", list(condata.keys()))
    conlistq = col4.number_input("Consumable Qnt", 1, condata[conlist])
    addcon = st.button("Add Consumable")
    if (addcon):
        conp[conlist] = conlistq
    if len(conp) > 0:
        st.write("Consumables items")
        st.table({"Consumables Name": conp.keys(), "Quantity": conp.values()})
    st.write("Equipment List")
    col5, col6 = st.columns((2, 3))
    equiplist = col5.selectbox("Select Equipment ", list(eqpdata.keys()))
    equiplistq = col6.number_input("Equipment Qnt", 1, eqpdata[equiplist])
    addequ = st.button("Add Equipment")
    if (addequ):
        equip[equiplist] = equiplistq
    if len(equip) > 0:
        st.write("Used Equipments")
        st.table({"Equipment Name": equip.keys(), "Quantity": equip.values()})
    submit = st.button("Create Work Order")
    if (submit):
        if inDB(otdb,"wo",wo):
            st.warning("Work order id is already taken!")
        else:
            fianlemp=[]
            for emp in empid:
                fianlemp.append(databaselink[name.index(emp)])
            data = {"wo":wo,"po": po, "assignedEmployee": fianlemp, "consumables": list(conp.keys()), "consQ": list(conp.values()),
                    "equipQ": list(equip.values()), "equipments": list(equip.keys())}
            st.success("Work Order Created Successfully")
            otdb.createWorkOrder(data)
            Udata = otdb.getUserList()
            for emp in empid:
                for userid in Udata:
                    if userid["uniqueid"] == emp.split("(")[0]:
                        otdb.db.collection("users").document(userid["uid"]).update({"assignedprojects": po+"~"+wo})
            conproducts = otdb.getCONList()
            st.success("Assigned to Users Successfully")
            res = otdb.db.collection("userProjects").where("po", "==", po).get()
            oldwo = res[0].to_dict()["workorders"]
            wod = list(oldwo)
            wod.append(wo)
            print(type(wod),wod)
            otdb.db.collection("userProjects").document(po).update({"workorders":wod})
            st.success("Assigned to Work Order Successfully")
            for con in conp.keys():
                for conproduct in conproducts:
                    if conproduct["ConName"] == con:
                        otdb.db.collection("consumableItems").document(conproduct["conId"]).update(
                            {"DispatchQuantityforProject": conproduct["DispatchQuantityforProject"] + conp[con],
                             "StockQuantity": (conproduct["StockQuantity"] - conp[con])})
            equips = otdb.getEQPList()
            st.success("ConsumableItems database updated Successfully")
            for equ in equip.keys():
                for eq in equips:
                    if eq["EqName"] == equ:
                        otdb.db.collection("equipments").document(eq["eqId"]).update(
                            {"DispatchQuantityforProjects": eq["DispatchQuantityforProjects"] + equip[equ],
                             "AvailableQuantity": (eq["AvailableQuantity"] - equip[equ])})
            st.success("Equipments database updated Successfully")
            conp.clear()
            equip.clear()
            st.success("Job Created successfully! ")
            col0, col00 = st.columns((3, 1))
            col00.write("Scan to See the Work Order")
            with col00:
                qr.add_data("http://3.95.56.247:8080/wo/" + wo)
                qr.make(fit=True)
                img = qr.make_image()
                imgpath = os.path.join("qr_images", wo + ".png")
                img.save(imgpath)
                st.image(openImage(imgpath))
            isworkorder=False
        if isworkorder==False:
            st.button("Close")
def createprojects(otdb):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    st.write("Create a new Projects")
    po = st.text_input("PO ID")
    st.text("PO ID Naming Convention: XXX123")
    clintName = st.text_input("Client Name")
    address = st.text_area("Address")
    jobDescriptions = st.text_area("jobDescriptions")
    submit = st.button("Create Project")
    if (submit):
        if inDB(otdb,"po",po):
            st.warning("Po Id already taken!")
        else:
            data = {"address": address, "po": po,"clientName":clintName, "jobDescriptions": jobDescriptions,"workorders":[]}
            otdb.createProjct(data)
            col0, col00 = st.columns((3, 1))
            col00.write("Scan to See the Project")
            with col00:
                qr.add_data("http://3.95.56.247:8080/wo/" + po)
                qr.make(fit=True)
                img = qr.make_image()
                imgpath = os.path.join("qr_images", po + ".png")
                img.save(imgpath)
                st.image(openImage(imgpath))
            st.success("Project Created Successfully")

def createuserList(otdb):
    data=otdb.getUserList()
    userlsit=[]
    name=[]
    for user in data:
        userlsit.append(user["uniqueid"]+"("+user["fullname"]+")")
        name.append(user["fullname"])
    return userlsit,name
def conitemname(otdb):
    data=otdb.getCONList()
    condata={}
    for con in data:
        condata[con["ConName"]]=con["StockQuantity"]
    return condata
def equipname(otdb):
    data=otdb.getEQPList()
    condata={}
    for con in data:
        condata[con["EqName"]]=con["InStock"]
    return condata
def app(otdb):
    #st.image(Image.open(base_path+"/comp_logo/logo0.png"))
    st.title("Company Project")
    selected = streamlit_menu()
    if selected=="Projects List":
        showprojects(otdb.getProjectList(),otdb)
    if selected=="Create Project":
        createprojects(otdb)
    if selected=="WorkOrders":
        showwotable(otdb.getwo())


