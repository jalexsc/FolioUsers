import datetime
import warnings
from datetime import datetime
import json
import uuid
import os
import os.path
import requests
import io
import math
import csv
import time
import random
import logging
import pandas as pd
import validator
import ast
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class window:
    def __init__(self, master,titlewin,geometrywin):
        master.title(titlewin)
        master.geometry(geometrywin)
        self.head=""
        self.frame1 = tk.LabelFrame(master, bd=5,text="Data")
        self.frame1.place(height=250, width=1000)
        # Frame for open file dialog
        self.file_frame = tk.LabelFrame(master, text="Open File")
        self.file_frame.place(height=100, width=600, rely=0.50, relx=0)
        # Frame for mapping
        self.map_frame = tk.LabelFrame(master, text="Mapping")
        self.map_frame.place(height=100, width=400, rely=0.50, relx=0.6)
        
        # Buttons Browse files
        self.button1 = tk.Button(self.file_frame, text="Browse a file", command=lambda: self.File_dialog())
        self.button1.place(rely=0.65, relx=0.30)
        #Load file
        self.button2 = tk.Button(self.file_frame, text="Load File", command=lambda: self.Load_excel_data())
        self.button2.place(rely=0.65, relx=0.65)
        
        self.button3 = tk.Button(self.file_frame, text="Transform File", command=lambda: self.readOrganizations())
        self.button3.place(rely=0.65, relx=0.85)

        self.button4 = tk.Button(self.file_frame, text="Mapping", command=lambda: self.readOrganizations())
        self.button4.place(rely=0.65, relx=0.95)
        
        # The file/file path text
        self.label_file = tk.Label(self.file_frame, text="No File Selected")
        self.label_file.place(rely=0, relx=0)

        ## Treeview Widget
        self.tv1 = ttk.Treeview(self.frame1)

        self.tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        self.treescrolly = tk.Scrollbar(self.frame1, orient="vertical", command=self.tv1.yview) # command means update the yaxis view of the widget
        self.treescrollx = tk.Scrollbar(self.frame1, orient="horizontal", command=self.tv1.xview) # command means update the xaxis view of the widget
        self.tv1.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set) # assign the scrollbars to the Treeview Widget
        self.treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        self.treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


    def File_dialog(self):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
        self.label_file["text"] = filename
        return None


    def Load_excel_data(self):
        """If the file selected is valid this will load the file into the Treeview"""
        file_path =self.label_file["text"]
        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".csv":
                df = pd.read_csv(excel_filename)
            else:
                df = pd.read_excel(excel_filename)
            
        except ValueError:
            self.messagebox.showerror("Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            self.messagebox.showerror("Information", f"No such file as {file_path}")
            return None

        self.clear_data()
                #combobox
        #self.vlist=["option 1", "option 2", "option 3"]

        #self.head=list(df.columns.values)
        #self.vlist=self.head
        #ll=len(self.head)
        #for index in ll:
        #    combo=ttk.Combobox(self.map_frame, values=self.vlist)
        #    combo.set("Pick an Option")
        #    combo.pack(padx=5, pady=5)
        
        
        self.tv1["column"] = list(df.columns)
        self.tv1["show"] = "headings"
        
        for column in self.tv1["columns"]:
            self.tv1.heading(column, text=column) # let the column heading = column name

        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            self.tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        return None


    def clear_data(self):
        self.tv1.delete(*self.tv1.get_children())
        return None
######################
#PURCHASE ORDERS
######################

class purchaseOrder():
    def __init__(self,poNumber,vendor,orderType,orderAcqbill,Order_status):
        self.poNumber=poNumber
        self.vendor=vendor
        self.orderType=orderType
        self.workflowStatus=Order_status
        self.orderAcqbill=orderAcqbill
        
    #polines Online
    def polinesOnline(self,polineAcqmethod,polinecost,polinedetailsInfo,
                      polineEresource,poLineDescription,polinePaymentstatus,polineReceiptstatus,
                      polineDescription,polineIspackage,polineTitle,polineVendordetail,publisher):
        poline={}
        poline={
            #"id": polineId,
            "checkinItems": False,
            "acquisitionMethod": polineAcqmethod,
            #"alerts": [],
            #"claims": [],
            "collection": False,
            #"contributors": contributors,
            "cost": polinecost, #{"listUnitPriceElectronic": price,"currency": currency,"discountType": "percentage","quantityElectronic": 1,"poLineEstimatedPrice": price},
            "details": polinedetailsInfo,
            "eresource":polineEresource,# {"activated": False,"createInventory": "None","trial": False, "accessProvider": vendor},
            #"fundDistribution": [],
            "isPackage": polineIspackage,
            #"locations": [],
            "orderFormat": "Electronic Resource",
            "poLineDescription": poLineDescription,
            "paymentStatus": polinePaymentstatus,
            #"physical": {"createInventory": "None","materialSupplier": vendor,"volumes": []},
            #"poLineNumber": poLineNumber,
            "receiptStatus": polineReceiptstatus,
            #"reportingCodes": [],
            "rush": False,
            "source": "User",
            #"tags": {"tagList": taglist2},
            "description": polineDescription,
            "publisher":publisher,
            "selector": "",
            "isPackage": polineIspackage, #True/False
            #"packagePoLineId": packagePoLineId,
            "titleOrPackage": polineTitle,
            "vendorDetail": polineVendordetail,
        }
        print(poline)
        return poline
    
    #polines OTHERS
    def polinesOnlineOthers(self,polineId,polineAcqmethod,polinecost,polinedetailsInfo,polineEresource,
                            poLineDescription,polinePaymentstatus,polinephysical,polineReceiptstatus,polineDescription,
                            polineIspackage,polineTitle,polineVendordetail,publisher):
        poline={}
        poline={"id": polineId,
                "checkinItems": False,
                "acquisitionMethod": polineAcqmethod,
                #"alerts": [],
                #"claims": [],
                "collection": False,
                #"contributors": contributors,
                "cost" : polinecost,# {"listUnitPrice" : price,"listUnitPriceElectronic" : price,"currency" : currency,"discountType" : "percentage","quantityPhysical" : 1,"quantityElectronic" : 1,"poLineEstimatedPrice" : price},
                #"cost": {"listUnitPriceElectronic": price,"currency": currency,"discountType": "percentage","quantityElectronic": 1,"poLineEstimatedPrice": price},
                "details": polinedetailsInfo,
                "eresource": polineEresource,#{"activated": False,"createInventory": "None","trial": trial, "accessProvider": vendor},
                #"fundDistribution": [],
                "isPackage": polineIspackage,
                "locations": [],
                "orderFormat": "P/E Mix",
                "poLineDescription": poLineDescription,
                "paymentStatus": polinePaymentstatus,
                "physical": polinephysical,#{"createInventory": "None","materialSupplier": vendor,"volumes": []},
                #"poLineNumber": poLineNumber,
                "receiptStatus": polineReceiptstatus,
                #"reportingCodes": [],
                "rush": False,
                "source": "User",
                #"tags": {"tagList": taglist2},
                "description": polineDescription,
                "publisher": publisher,
                "selector": "",
                "isPackage": polineIspackage,
                #"packagePoLineId": packagePoLineId,
                "titleOrPackage": polineTitle,
                "vendorDetail": polineVendordetail,
                }
        return poline
    
    #polines Online + Print
    def polinesOnlinePrint(self,polineId,polineAcqmethod,polinecost,
                           polinedetailsInfo,polineEresource,poLineDescription,polinePaymentstatus,polinephysical,
                           polineReceiptstatus,polineDescription,polineIspackage,polineTitle,polineVendordetail,publisher):
        poline={}
        poline={ "id": polineId,
            "checkinItems": False,
            "acquisitionMethod": polineAcqmethod,
            #"alerts": [],
            #"claims": [],
            "collection": False,
            #"contributors": contributors,
            "cost":polinecost,# {"listUnitPrice": 0.0,"listUnitPriceElectronic": price,"currency": currency,"discountType": "percentage","quantityPhysical": 1,"quantityElectronic": 1,"poLineEstimatedPrice": price},
            "details": polinedetailsInfo,
            "eresource": polineEresource,#{"activated": False,"createInventory": "None","trial": trial, "accessProvider": vendor},
            ##"fundDistribution": [],
            "isPackage": polineIspackage,
            "locations": [],
            "orderFormat": "P/E Mix",
            "paymentStatus": polinePaymentstatus,
            "poLineDescription": poLineDescription,
            "physical": polinephysical,# {"createInventory": "None","materialSupplier": vendor,"volumes": []},
            #"poLineNumber": poLineNumber,
            "receiptStatus": polineReceiptstatus,
            #"packagePoLineId": packagePoLineId,
            #"reportingCodes": [],
            "publisher": publisher,
            "rush": False,
            "source": "User",
            #"tags": {"tagList": taglist2},
            "titleOrPackage": polineTitle,
            "vendorDetail": polineVendordetail,
            }
        return poline
    
    #polines Print
    def polinesPrint(self,polineId, polineAcqmethod, polinecost,
                           polinedetailsInfo, polineEresource, poLineDescription, polinePaymentstatus, polinephysical,
                           polineReceiptstatus, polineDescription, polineIspackage, polineTitle, polineVendordetail):
        poline={}
        poline={"id": polineId,
            "checkinItems": False,
            "acquisitionMethod": polineAcqmethod,
            #"alerts": [],
            #"claims": [],
            "collection": False,
            #"contributors": contributors,
            "cost" : polinecost,# {"listUnitPrice" : price,"currency" : currency,"discountType" : "percentage","quantityPhysical" : 1,"poLineEstimatedPrice" : price},
            "details": polinedetailsInfo,
            "eresource": polineEresource,#{"activated": False,"createInventory": "None","trial": trial, "accessProvider": vendor},
            #"fundDistribution": [],
            "isPackage": polineIspackage,
            "locations": [],
            "orderFormat": "Physical Resource",
            "poLineDescription": poLineDescription,
            "paymentStatus": polinePaymentstatus,
            "physical": polinephysical,#{"createInventory": "None","materialSupplier": vendor,"volumes": []},
            #"poLineNumber": poLineNumber,
            "receiptStatus": polineReceiptstatus,
            #"reportingCodes": [],
            "rush": False,
            "source": "User",
            #"tags": {"tagList": taglist2},
            "description": polineDescription,
            "selector": "",
            #"packagePoLineId": packagePoLineId,
            "titleOrPackage": polineTitle,
            "vendorDetail": polineVendordetail,
            }
        return poline

    def polinesOther(self,polineId, polinedetailsInfo, polineEresource, poLineDescription, polinePaymentstatus, polinephysical,
                           polineReceiptstatus, polineinternalnote, polineIspackage, polineTitle, polineVendordetail):
        poline={}
        poline={
            "id": polineId,
            "checkinItems": False,
            "acquisitionMethod": polineId,
            #"alerts": [],
            #"claims": [],
            "collection": False,
            #"contributors": contributors,
            "cost" : polineId,#{"listUnitPrice" : price,"currency" : currency,"discountType" : "percentage","quantityPhysical" : 1,"poLineEstimatedPrice" : price},
            "details": polinedetailsInfo,
            "eresource": polineEresource,#{"activated": False,"createInventory": "None","trial": trial, "accessProvider": vendor},
            #"fundDistribution": [],
            "locations": [],
            "orderFormat": "Other",
            "poLineDescription": poLineDescription,
            "paymentStatus": polinePaymentstatus,
            "physical": polinephysical,#{"createInventory": "None","materialSupplier": vendor,"volumes": []},
            #"poLineNumber": poLineNumber,
            "receiptStatus": polineReceiptstatus,
            #"reportingCodes": [],
            "rush": False,
            "source": "User",
            #"tags": {"tagList": taglist2},
            "description": polineinternalnote,
            "selector": "",
            "isPackage": polineIspackage,
            #"packagePoLineId": packagePoLineId,
            "titleOrPackage": polineTitle,
            "vendorDetail": polineVendordetail,
            }
        return poline    
     
    #MASTER ORDER 
    def masterpurchaseOrders(self,orderPrefix,orderSuffix,ordermanualPo,ordernotes,orderOngoing,
                             orderApproved,orderClosereason,Ordertags,compositePoLines,acqunits,fileName):
        try:
            orderFile=open(fileName+"_orders.json", 'a')
            order= {
                    #"id":polId,
                    "poNumberPrefix": orderPrefix,
                    "poNumber": self.poNumber,
                    "poNumberSuffix": orderSuffix,
                    "vendor": self.vendor,
                    "orderType": self.orderType,
                    "billTo": self.orderAcqbill,
                    "shipTo": self.orderAcqbill,
                    "manualPo": ordermanualPo,
                    "notes": ordernotes,
                    "reEncumber": False,
                    "ongoing": orderOngoing, #{"interval": interval, "manualRenewal": manualPo, "isSubscription": True,"renewalDate": renewalDate, "reviewPeriod": 90, "notes": notesOngoing},
                    #"totalEstimatedPrice": amount,
                    #"totalItems": totalUnits,
                    "approved": orderApproved,
                    "workflowStatus": self.workflowStatus,
                    "closeReason": orderClosereason, # {"reason": closereason,"note": reasonNote},
                    "tags":Ordertags,
                    "compositePoLines": compositePoLines,
                    "acqUnitIds":acqunits,
                    }
            return None
    
        except ValueError:
            print("Module folioAcqfunctions Master Orders: "+str(ValueError))
            
def printOrders(oredertoprint,path):
    orderFile=open(path+".json", 'a')       
    #json_ord = json.dumps(valuetoprint,indent=2)
    json_order = json.dumps(oredertoprint)
    #print('Datos en formato JSON', json_order)
    orderFile.write(json_order+"\n")
    return None

def json_validator(data):
    try:
        json_data = ast.literal_eval(json.dumps(str(data)))
        #print(data)
        #json.loads(str(data))
        return True
    except ValueError as error:
        print("invalid json: %s" % error)
        return False
    
#Print Object with Jscon validator.
def printObject(objectToPrint,path,x,file_name,prettyJson):
    try:
        outfilename=""
        #toPrint=json_validator(objectToPrint)
        if prettyJson:
            path_file=path+f"\\results\\{file_name}"+".json"
            #outfilename = json.load(objectToPrint)
            with open(path_file,"w+") as outfile:
                json.dump(objectToPrint,outfile,indent=2)
        else:
            path_file=path+f"\\logs\\{file_name}"+".json"
            outfilename = json.dumps(objectToPrint)
            with open(path_file,"a+") as outfile:
                outfile.write(outfilename+"\n")
        return None
    except ValueError:
        print("Module folioAcqfunctions Master Orders: "+str(ValueError))
        

        
################################################
### NOTES
################################################

class notes():
    def __init__(self):
        self.idNotes= str(uuid.uuid4())
    #(uuidOrg,typeId,customerName,15,16,17)

def print_notes(linkId,typelinkId,path,**kwargs):
    try:
        notes={}
        notes["typeId"]= kwargs['typeId']
        notes["type"]= kwargs['type']
        notes["domain"]= kwargs['domain']
        notes["title"]= kwargs['title']
        notes["content"]= kwargs['cont']
        notes["links"]= [{"id": linkId,"type": typelinkId}]
        x=0
        printObject(notes,path,x,"all_notes",False)
        #print(notes)
        return notes
        
    except ValueError as error:
            print("Error: %s" % error)
            
       
######END NOTES
    

################################################
### CONTACTS
################################################
class contactsClass():
    
    def __init__(self,contactID,contactfirstName, contactlastName, contactcategories,contactlanguage):
        self.contactid=contactID
        self.contactfirstName= contactfirstName
        self.contactlastName= contactlastName
        self.language= contactlanguage
        self.contactinactive= False
        self.categories=contactcategories

    def printcontactsClass(self,contactprefix,cont_phone,cont_email, cont_address,cont_urls,cont_categories,contactnotes,fileName):
        contactFile=open(fileName+"_contacts.json", 'a')
        contacto={
                "prefix": contactprefix,
                "id": self.contactid,
                "firstName": self.contactfirstName,
                "lastName": self.contactlastName,
                "language": self.language,
                "notes": contactnotes,
                "phoneNumbers": cont_phone,
                "emails": cont_email,
                "addresses": cont_address,
                "urls": cont_urls,
                "categories": cont_categories,
                "inactive": self.contactinactive,
           }
        json_contact = json.dumps(contacto)
        #print('Datos en formato JSON', json_contact)
        contactFile.write(json_contact+"\n")
        
 
    
#end
################################################
### INTERFACES
################################################
class interfaces():

    def __init__(self,interUuid, intername, interuri, type):
        self.interid=interUuid
        self.intername = intername
        self.interuri = interuri
        self.deliveryMethod= "Online"
        self.interavailable=True
        self.intertype=type
        
    def printinterfaces(self, fileName,notes,statisticsNotes):
        intFile=open(fileName+"_interfaces.json", 'a')
        dato={
            "id": self.interid,
            "name": self.intername,
            "uri": self.interuri,
            "notes":notes,
            "available":self.interavailable,
            "deliveryMethod": self.deliveryMethod,
            "statisticsFormat": "HTML",
            "locallyStored": "",
            "onlineLocation": "",
            "statisticsNotes": statisticsNotes,
            "type": self.intertype
           }
        json_interfaces = json.dumps(dato)
        #print('Datos en formato JSON', json_str)
        intFile.write(json_interfaces+"\n")

### CREDENTIALS
    def printcredentials(self, idInter, login, passW, fileName):
        creFile=open(fileName+"_credentials.json", 'a')
        cred ={
            #"id": str(uuid.uuid4()),
            "username": login, 
            "password": passW,
            "interfaceId": idInter
             }
        json_cred = json.dumps(cred)
        #print('Credentials: ', json_cred)
        creFile.write(json_cred+"\n")
        
    def urltype(self,value):
        urlname=[]
        if value=="1":
            urlname.append("Admin")
            urlname.append("Admin")
        elif value=="2":
            urlname.append("FTP")
            urlname.append("Admin")
        elif value=="3":
            urlname.append("Other")
            urlname.append("Other")
        elif value=="4":
            urlname.append("Statistics")
            urlname.append("End user")
        elif value=="Support":
            urlname.append("Support")
            urlname.append("End user")
        else:
            urlname.append("Other")
            urlname.append("Other")
        return urlname


################################################
### ORGANIZATIONS
################################################
class Organizations():
    def __init__(self,idorg,name,orgcode,vendorisactive,orglanguage,account):
        self.id=idorg
        self.name=name
        self.code=orgcode
        self.language=orglanguage
        self.exportToAccounting= True
        self.status="Active"
        self.isVendor= True
        self.accounts=account
            
    def printorganizations(self,org_desc,org_aliases,org_addresses,org_phoneNum,org_emails,org_urls,org_vendorCurrencies,org_contacts, org_interfaces,org_erpCode,file_name):
        #orgFile=open(fileName+"_organizations.json", 'a')
        organization1 = {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "erpCode": org_erpCode,
            "description": org_desc,
            "exportToAccounting" : self.exportToAccounting,
            "status": self.status,
            "language": self.language,
            "aliases": org_aliases,
            "addresses": org_addresses,
            "phoneNumbers": org_phoneNum,
            "emails": org_emails,
            "urls": org_urls,
            "contacts": org_contacts,
            #"agreements": org_agreements,
            "vendorCurrencies": org_vendorCurrencies,
            "claimingInterval": 30,
            "discountPercent": 0,
            "expectedInvoiceInterval": 0,
            "renewalActivationInterval": 0,
            "interfaces": org_interfaces,
            "accounts": self.accounts,
            "isVendor": self.isVendor,
            "paymentMethod": "EFT",
            "accessProvider": True,
            "governmental": False,
            "licensor": False,
            "liableForVat": False,
            "materialSupplier": True,
            "expectedActivationInterval": 0,
            "subscriptionInterval": 0,
            "changelogs": []
            }
        x=0
        printObject(organization1,file_name,x,"organization",False)
        #json_organization = json.dumps(organization)
        #print('Datos en formato JSON', json_organization)
        #orgFile.write(json_organization+"\n")    

#end
###############################################
####PURCHASE ORDERS FUNCTIONS
#########################################

def orderDetails(**kwargs):
    try:
        details={}
        for key, value in kwargs.items():
            details[key]=value#receivingNote
        return details
    except ValueError:
        print("Error")

def SearchMappingDetails(**kwargs):
    #field,schema,file_name
        # Opening JSON file
        dic =dic= {}
        f = open(kwargs['file_name'],)
        data = json.load(f)
        for i in data['organizationMapping']:
            a_line=str(i)
            if i[field] == kwargs['file_name']:
                 dic=i
                 break
        f.close()
        return dic['legacyName']
    
def SearchClient(code_search):
        # Opening JSON file
        dic =dic= {}
        f = open("okapi_customers.json",)
        data = json.load(f)
        for i in data['okapi']:
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                 dic=i
                 del dic['name']
                 del dic['user']
                 del dic['password']
                 del dic['x_okapi_version']
                 del dic['x_okapi_status']
                 del dic['x_okapi_release']
                 break
        f.close()
        return dic
    
def okapiPath(code_search):
    valor=[]
    try:
        #valor="0"
        f = open("setting_data.json",)
        data = json.load(f)
        for i in data['settings']:
            a_line=str(i)
            if i['name'] == code_search:
            #if (a_line.find(code_search) !=-1):
                valor.append(i['pathPattern'])
                valor.append(i['name'])
                break
        f.close()
        return valor
    except ValueError:
        print("schema does not found")
        return 0
    
def check_poNumber(value, path):
    try:
        valuefix=""
        Newmpol=""
        keepit=False
        #sp_chars = [';', ':', '!', "*","<","/","_","-","(",")","|"," ","@","¿","?","=","#","!"] 
        #valuefix = filter(lambda i: i not in sp_chars, value)
        if value.find(" ")!=-1: value=value.replace(" ","")
        if value.find("#")!=-1: value=value.replace("#","")
        if value.find(">")!=-1: value=value.replace(">","")
        if value.find("<")!=-1: value=value.replace("<","")
        if value.find("/")!=-1: value=value.replace("/","")
        if value.find(":")!=-1: value=value.replace(":","")
        if value.find("-")!=-1: value=value.replace("-","")
        if value.find("_")!=-1: value=value.replace("_","")
        if value.find("(")!=-1: value=value.replace("(","")
        if value.find(")")!=-1: value=value.replace(")","")
        if value.find("&")!=-1: value=value.replace("&","")
        if value.find(".")!=-1: value=value.replace(".","")
        if value.find("'")!=-1: value=value.replace("'","")
        if value.find(",")!=-1: value=value.replace(",","")
        if value.find("|")!=-1: value=value.replace("|","")
        if value.find("!")!=-1: value=value.replace("!","")
        if value.find("=")!=-1: value=value.replace("=","")
        if value.find("@")!=-1: value=value.replace("@","")
        if value.find("?")!=-1: value=value.replace("?","")
        if value.find("¿")!=-1: value=value.replace("¿","")
        if value.find("*")!=-1: value=value.replace("*","")
        if len(value)>18: 
            value=""
            keepit=True
            for i in range(2):
                Newmpol=str(random.randint(100, 1000))
                with open(path+"\oldNew_ordersID.txt", "a") as clean:
                    clean.write(str(value)+"/"+str(Newmpol)+"\n")
                value=Newmpol            
        return value
        
    except ValueError:
        print("Concat Error")
        
def searchKeysByVal(dict, byVal):
    try:
        keysList = ""
        keyslist=dict.get(byVal)
        return keyslist
    except ValueError:
        print("Concat Error")

def tsv_To_dic(path):
    try:
        with open(path, mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {rows[0]:rows[1] for rows in reader}
        return mydict            
    except ValueError:
        print("Concat Error")


        
def getId(namesearchValue,path,elementtosearch,okapi_url,okapi_token,okapi_tenant):
        try:
            if namesearchValue is None: searchValue="undefined"
            if namesearchValue=="NULL": searchValue="undefined"
            if namesearchValue=="": searchValue="undefined"
            dic={}
            path1=""        
            pathPattern=path
            #pathPattern1="/organizations/organizations" #?limit=9999&query=code="
            okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
            length="1"
            start="1"
            element=elementtosearch
            query=f"query=name=="
            #/organizations-storage/organizations?query=code==UMPROQ
            paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
            #paging_q = f"?{query}"+search_string
            path1 = pathPattern1+paging_q
            #data=json.dumps(payload)
            url1 = okapi_url + path1
            req = requests.get(url1, headers=okapi_headers)
            idorg=""
            #Search by name
            if req.status_code != 201:
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']
                        return idorg
        except requests.exceptions.HTTPError as err:
            print("error Organization GET")    

  
def get_OrgId(searchValue,customerName):
    try:
        searchValue=searchValue.replace("&","")
        searchValue=searchValue.replace("+","")
        client=SearchClient(customerName)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        pathPattern1="/organizations/organizations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="organizations"
        query=f"query=code=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern1+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']

                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=name=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern1+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']

                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
        
def get_OrgId_license(searchValue,customerName):
    try:
        client=SearchClient(customerName)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        pathPattern1="/organizations/organizations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="organizations"
        query=f"query=name=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern1+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=[]
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg.append(l['id'])
                    idorg.append(l['name'])
                  
                return idorg
            #Search by code
            elif (total_recs==0):
                searchValue=searchValue.replace(" ","")
                searchValue=searchValue.replace(",","")
                searchValue=searchValue.replace(".","")
                searchValue=searchValue.replace("&","")
                searchValue=searchValue.replace("'","")
                query=f"query=code=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern1+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg.append(l['id'])
                        idorg.append(l['name'])
                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
               
def to_string(value):
    try:
        valueR=""
        if int(value):
            #print("numero")
            valueR=str(round(value))
        elif float(value):
            #print("decimal")
            valueR=str(round(value))
        else:
            valueR=value
        return valueR
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
    
def get_funId(searchValue,orderFormat,client):
    try:
        if searchValue=="7444" and orderFormat=="Physical Resource":
            searchValue=searchValue+"-Print"
        elif searchValue=="7444" and orderFormat=="Mixed P/E":
            searchValue=searchValue+"-Electronic"
        elif searchValue=="7444" and orderFormat=="Electronic Resource":
            searchValue=searchValue+"-Electronic"
        elif searchValue=="7443" and orderFormat=="S":
            searchValue=searchValue+"-Sub"
        elif searchValue=="7443" and orderFormat=="A":
            searchValue=searchValue+"-Fees"
        elif searchValue=="7441":
            searchValue=searchValue+"-Sub"
        elif searchValue=="7447":
            searchValue=searchValue+"-Sub"
            
        #7442
        #7023
        #7046
        #7047
        #7049
        client=SearchClient(client)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        pathPattern1="/finance/funds" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="funds"
        query=f"query=code=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern1+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=[]
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg.append(l['id'])
                    idorg.append(l['code'])
                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=name=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern1+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg.append(l['id'])
                        idorg.append(l['code'])
                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
    
def get_matId(searchValue,client):
    try:
        client=SearchClient(client)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        pathPattern1="/material-types" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="mtypes"
        query=f"query=name=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern1+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']
                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=code=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern1+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']
                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")

def get_funId_no_name(searchValue,client):
    try:
        client=SearchClient(client)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        pathPattern1="/finance/funds" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="funds"
        query=f"query=code=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern1+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']
                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=name=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern1+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']
                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
    
def get_locId(searchValue,client):
    try:
        client=SearchClient(client)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        pathPattern1="/locations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="locations"
        query=f"query=code=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern1+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']
                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=code=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern1+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']
                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
        
def get_title(client,**kwargs):
        pathPattern1=okapiPath(kwargs['element'])
        element=kwargs['element']
        pathPattern=pathPattern1[0]
        searchValue=kwargs['searchValue']
        client=SearchClient(client)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        #pathPattern="/instance-storage/instances" #?limit=9999&query=code="
        #https://okapi-ua.folio.ebsco.com/instance-storage/instances?query=hrid=="264227"
        pathPattern="/instance-storage/instances" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        #element="instances"
        #https://okapi-trinitycollegelibrarycambridge.folio.ebsco.com/instance-storage/instances?query=(identifiers any ".b10290242")
        query=f"?query=(identifiers="
        #query=f"query=hrid=="
        #/finance/funds?query=name==UMPROQ
        search='"'+searchValue+'")'
        #.b10290242
        #paging_q = f"?{query}"+search
        paging_q = f"{query} "+search
        path = pathPattern+paging_q
        #data=json.dumps(payload)
        url = okapi_url + path
        req = requests.get(url, headers=okapi_headers)
        idhrid=[]
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idhrid.append(l['id'])
                    idhrid.append(l['title'])            
        return idhrid
    
def order_cost(additionalCost,currency,discount,discountType,exchangeRate,listUnitPrice,
               listUnitPriceElectronic,quantityPhysical,quantityElectronic,poLineEstimatedPrice):
    #{"listUnitPriceElectronic": price,"currency": currency,"discountType": "percentage","quantityElectronic": 1,"poLineEstimatedPrice": price},
    try:
        coste={}        
        coste["additionalCost"]= additionalCost
        coste["currency"]= currency
        coste["discount"]= ""
        coste["discountType"]= discountType #"percentage"
        coste["exchangeRate"]= exchangeRate
        coste["listUnitPrice"]= listUnitPrice
        coste["listUnitPriceElectronic"]= listUnitPriceElectronic
        coste["quantityPhysical"]= quantityPhysical
        coste["quantityElectronic"]: quantityElectronic
        coste["poLineEstimatedPrice"]= poLineEstimatedPrice
        return coste
    except ValueError:
        print("coste Error")
        
def order_closeReason(reasonvalue, reasonnote):
    try:
        reason={}    
        reason["reason"]=""
        reason["note"]= ""
        return reason
    except ValueError:
        print("Concat Error")
        
def order_costbyElectronic(orderprice,ordercurrency,orderdiscountype,orderquantity, orderpoestimateprice):
    try:#{"listUnitPriceElectronic": price,"currency": currency,"discountType": "percentage","quantityElectronic": 1,"poLineEstimatedPrice": price},
        cost={}
        cost["listUnitPriceElectronic"]=orderprice
        cost["currency"]=ordercurrency
        cost["discountType"]=orderdiscountype
        cost["quantityElectronic"]=orderquantity
        cost["poLineEstimatedPrice"]=orderpoestimateprice
        return cost
    except ValueError:
        print("Concat Error")  
        
         
def order_eresource(eresourceActivated, ecreateInventory,etrial, eaccessprovider):
    try:
    # {"activated": False,"createInventory": "None","trial": False, "accessProvider": vendor},
        eresource={} 
        eresource["activated"]=eresourceActivated
        eresource["createInventory"]=ecreateInventory
        eresource["trial"]=etrial
        eresource["accessProvider"]=eaccessprovider #Vendor ID
        return eresource
    except ValueError:
        print("Concat Error") 
def order_notes(value):
    try:
        orderNote=[]
        orderNote.append(value)
        return orderNote
    except ValueError:
        print("Concat Error")


        
def order_tags(value):
    try:
        tags={}
        tagsvalue=[]
        tagsvalue.append(value)
        tagList["tagList"]=tagsvalue
        return tags
    except ValueError:
        print("Concat Error")    
def order_acqUnitId(value):
    adqUni=[]
    adqUni.append(value)
    return value
    
#############################
#GENERAL FUNCTIONS
#############################
def floatHourToTime(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (
        int(h),
        int(m),
        int(r*60),
    )

def timeStamp(dateTimeObj):
    try:
        #dateTimeObj = dateTimeObj.strptime(dateTimeObj, "%Y-%m-%d").strftime("%d-%m-%Y")
        #fecha_dt = datetime.strptime(dateTimeObj, '%Y-%m-%d')
        #dateTimeObj = fecha_dt.strftime(format)
        timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
        return timestampStr
    except ValueError:
        print("Module folioAcqfunctions organizations time Error: "+str(ValueError))
        
def timeStampString(dateTimeObj):
    try:
        #dateTimeObj = dateTimeObj.strptime(dateTimeObj, "%Y-%m-%d").strftime("%d-%m-%Y")
        fecha_dt = datetime.strptime(dateTimeObj, '%Y-%m-%d')
        #dateTimeObj = fecha_dt.strftime(format)
        timestampStr = fecha_dt.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
        return timestampStr
    except ValueError:
        print("Module folioAcqfunctions organizations time Error: "+str(ValueError)) 

def timeStampStringSimple(dateTimeObj):
    try:
        fecha_dt = dateTimeObj.strptime(dateTimeObj, "%Y-%m-%d").strftime("%d-%m-%Y")
        #fecha_dt = datetime.strptime(dateTimeObj, '%Y-%m-%d')
        #dateTimeObj = fecha_dt.strftime(format)
        timestampStr = fecha_dt.strftime("%Y-%m-%d")
        return timestampStr
    except ValueError:
        print("Module folioAcqfunctions organizations time Error: "+str(ValueError)) 
    
    
################################################
### ORGANIZATIONS FUNCTIONS
################################################
def org_aliases(dfRow,*argv):
    try:
        alia={}
        aliaR=[]
        for arg in argv:
        #print("argumentos de *argv:", row[arg])
            if len(dfRow[arg])>0:
                alia['value']=dfRow[arg]
                alia['description']=""
                aliaR.append(alia)
                alia={}
    except ValueError:
        print("Module folioAcqfunctions organizations aliases Error: "+str(ValueError))
    return aliaR

def org_languages(value):
    try:
        value=value.upper()
        if value=="ENGLISH":
            valueR="eng"
        elif value=="SPANISH":
            valueR="spa"
        elif value=="NULL":
            valueR="eng"
        elif value is None:
            valueR="eng"
        elif value=="":
            valueR=""
        else:
            valueR="eng"
        return valueR
    
    except ValueError:
        print("org_addresses Error: "+str(ValueError))
        
def concatfields(dfRow,*argv):
    try:
        concatfield=""
        for arg in argv:
            if dfRow[arg]:
                concatfield=concatfield+"$"+dfRow[arg]
        if len(concatfield)>0:
            return concatfield
        else:
            return None
    except ValueError:
        print("Concat Error")
################################################################
def org_addresses_utm(dfRow, *argv):
    try:
        addr={}
        addrR=[]
        count=1
        for arg in argv:
            addr['addressLine1']=dfRow[arg]
            if dfRow[arg+1]: addr['addressLine2']=dfRow[arg+1]
            if dfRow[arg+2]: addr['city']=dfRow[arg+2]
            if dfRow[arg+3]: addr['stateRegion']=dfRow[arg+3]
            if dfRow[arg+4]: addr['zipCode']=dfRow[arg+4]
            if dfRow[arg+5]: addr['country']=dfRow[arg+5]
            if dfRow[arg+6]: addr['categories']=org_categorie(dfRow[arg+6])
            if dfRow[arg+7]: addr['language']="eng"
            if (count==1): addr["isPrimary"]=True
            count=count+1
            addrR.append(addr)
            addr={}
            return addrR
    except ValueError:
        print("org_addresses Error: "+str(ValueError))
        
def org_addresses_mls(dfRow, *argv, **kwargs):
    try:
        addr={}
        addrR=[]
        count=1
        cat=[]        
        for i in argv:
            if dfRow[i]=="":
                addr['addressLine1']=dfRow[i]
                if dfRow[i+1]: addr['addressLine2']=dfRow[i+1]
                if dfRow[i+2]: addr['city']=dfRow[i+2]
                if dfRow[i+3]: addr['stateRegion']=dfRow[i+3]
                if dfRow[i+4]: addr['zipCode']=dfRow[i+4]
                if dfRow[i+5]: addr['country']=dfRow[i+5]
                if dfRow[i+6] and dfRow[i+6]=="No":
                    addr["isPrimary"]=False
                if dfRow[i+6] and dfRow[i+6]=="Yes":
                    addr["isPrimary"]=True

                if dfRow[i+7]:
                    cadena=str(dfRow[i+7]).strip()
                    c=cadena.find(";")
                    if c > 0:
                        chunked=cadena.split(";")
                        cat.append(get_Id(kwargs['customer'],searchValue=chunked[0].strip(),element="categories"))
                        cat.append(get_Id(kwargs['customer'],searchValue=chunked[1][1:].strip(),element="categories"))
                    else:
                        cat.append(get_Id(kwargs['customer'],search=cadena))
                    addr['categories']=cat 
                addr['language']="eng"
                addrR.append(addr)
                cat=[]
                addr={}
        return addrR
    except ValueError:
        print("org_addresses Error: "+str(ValueError))
        
################################################################        
def org_addresses(dfRow,concat, *argv):
    try:
        if concat:
            addr={}
            addrR=[]
            dir2=""
            dir=""
            cadena=""
            for arg in argv:
                cadena=dfRow[arg]
                if cadena!="$ $ $ $":
                    print(cadena)
                    if len(cadena)>0:
                        x=cadena.count("$")                
                        if (x>0):
                            chunked=cadena.split("$")
                            if (x==1):
                                addr['addressLine1']=chunked[0]
                                addr['addressLine2']=""
                                cadena=chunked[1]
                                if (cadena.find(",")!=-1):
                                    y=cadena.find(",")
                                    addr['city']=cadena[:y]
                                    addr['country']=""
                                    cadena=cadena[y+2:]
                                    if (cadena.find(" ")!=-1):
                                        y=cadena.find(" ")
                                        addr['stateRegion']=cadena[:y]
                                        addr['zipCode']=cadena[y+1:]
                                        addr['categories']=org_categorie("nn")
                                        addr['language']=""
                                        addr["isPrimary"]=True    
                            elif (x==2):
                                addr['addressLine1']=chunked[0]
                                addr['addressLine2']=chunked[1]
                                cadena=chunked[2]
                                if (cadena.find(",")!=-1):
                                    y=cadena.find(",")
                                    addr['city']=cadena[:y]
                                    addr['country']=""
                                    cadena=cadena[y+2:]
                                    if (cadena.find(" ")!=-1):
                                        y=cadena.find(" ")
                                        addr['stateRegion']=cadena[:y]
                                        addr['zipCode']=cadena[y+1:]                     
                                        addr['categories']=org_categorie("nn")
                                        addr['language']=""
                                        addr["isPrimary"]=True    
                            elif (x==3):
                                pass
                            elif (x==4):
                                addr['addressLine1']=chunked[0]
                                addr['addressLine2']=chunked[1]
                                addr['city']=chunked[2]
                                addr['country']=chunked[3]
                                addr['zipCode']=chunked[4]
                                addr['categories']=org_categorie("nn")
                                addr['language']="eng-uk"
                                addr["isPrimary"]=True    
                                
                                #addr['addressLine1']=dfRow[10]
                                #addr['addressLine2']=dfRow[11]
                                #addr['city']=dfRow[12]
                                #addr['stateRegion']=dfRow[13]
                                #addr['zipCode']=dfRow[14]
                                #addr['country']=""
                                #addr['categories']=org_categorie("nn")
                                #addr['language']=""
                                #addr["isPrimary"]=True
                                #addrR.append(addr)

                            elif (x==5):
                                pass
                    else:
                        addr['addressLine1']=dfRow[arg]
                        addr['addressLine2']=""
                        addr['city']=""
                        addr['stateRegion']=""
                        addr['zipCode']=""
                        addr['country']=""
                        addr['categories']=org_categorie("nn")
                        addr['language']="eng"
                        addr["isPrimary"]=True
                    addrR.append(addr)
                    cadena=""
                    addr={}
                return addrR
        
            return addrR
    except ValueError:
            print("org_addresses Error: "+str(ValueError))
        
def org_addresses_trinity(dfRow,concat, *argv):
    try:
        addr={}
        addrR=[]
        dir2=""
        dir=""
        cadena=""
        for arg in argv:
            cadena=dfRow[arg]
            if cadena!="$ $ $ $":
                print(cadena)
                if len(cadena)>0:
                    x=cadena.count("$")                
                    if (x>0):
                        chunked=cadena.split("$")
                        if x==1:
                            addr['addressLine1']=chunked[0]
                            addr['addressLine2']=""
                            cadena=chunked[1]
                            if (cadena.find(",")!=-1):
                                y=cadena.find(",")
                                addr['city']=cadena[:y]
                                addr['country']=""
                                cadena=cadena[y+2:]
                                if (cadena.find(" ")!=-1):
                                    y=cadena.find(" ")
                                    addr['stateRegion']=cadena[:y]
                                    addr['zipCode']=cadena[y+1:]
                                    addr['categories']=org_categorie("nn")
                                    addr['language']=""
                                    addr["isPrimary"]=True    
                        elif x==2:
                            addr['addressLine1']=chunked[0]
                            addr['addressLine2']=chunked[1]
                            cadena=chunked[2]
                            if (cadena.find(",")!=-1):
                                y=cadena.find(",")
                                addr['city']=cadena[:y]
                                addr['country']=""
                                addr['stateRegion']=""
                                addr['zipCode']=cadena[y+1:]                     
                                addr['categories']=org_categorie("nn")
                                addr['language']=""
                                addr["isPrimary"]=True    
                        elif x==3:
                            addr['addressLine1']=chunked[0]
                            addr['addressLine2']=chunked[1]
                            addr['city']=chunked[2]
                            addr['country']=""
                            addr['stateRegion']=""
                            addr['zipCode']=chunked[3]           
                            addr['categories']=[]
                            addr['language']=""
                            addr["isPrimary"]=True  
                        elif x==4:
                            addr['addressLine1']=chunked[0]
                            addr['addressLine2']=chunked[1]
                            addr['city']=chunked[2]
                            addr['country']=chunked[3]
                            addr['zipCode']=chunked[4]
                            addr['categories']=org_categorie("nn")
                            addr['language']="eng-uk"
                            addr["isPrimary"]=True    
                        elif x==5:
                            addr['addressLine1']=chunked[0]
                            addr['addressLine2']=chunked[1]
                            addr['city']=chunked[2]
                            addr['country']=chunked[3]
                            addr['zipCode']=chunked[4]
                            addr['categories']=org_categorie("nn")
                            addr['language']="eng-uk"
                            addr["isPrimary"]=True 
                else:
                    addr['addressLine1']=dfRow[arg]
                    addr['addressLine2']=""
                    addr['city']=""
                    addr['stateRegion']=""
                    addr['zipCode']=""
                    addr['country']=""
                    addr['categories']=org_categorie("nn")
                    addr['language']="eng"
                    addr["isPrimary"]=True
                addrR.append(addr)
                cadena=""
                addr={}
        return addrR                            
    except ValueError:
            print("org_addresses Error: "+str(ValueError))
            
def org_phoneNumbers(dfRow,*argv):
    pho={}
    phoR=[]
    count=1
    for arg in argv:
        #print("argumentos de *argv:", row[arg])
        if len(dfRow[arg])>0:
            if dfRow[arg]: pho["phoneNumber"]=dfRow[arg]
            if dfRow[arg+1]: pho["type"]="Office"
            if dfRow[arg+2]: pho["language"]="eng" 
            if dfRow[arg+3]: pho["categories"]=[]
            if (count==1): pho["isPrimary"]= True
            count=count+1
            phoR.append(pho)
            pho={}
    return phoR


def org_emails(dfRow,*argv):
    emai={}
    emaiR=[]
    count=1
    for arg in argv:
        #print("argumentos de *argv:", row[arg])
        if len(dfRow[arg])>0:
            if dfRow[arg]:   emai['value']=dfRow[arg] 
            if dfRow[arg+1]: emai['description']=dfRow[arg+1]
            if dfRow[arg+2]: emai['language']="eng"
            if dfRow[arg+3]: emai['categories']=org_categorie(dfRow[arg+3])
            if (count==1): emai['isPrimary']=True
            count=count+1
            emaiR.append(emai)
            emai={}
    return emaiR

def dic(**kwargs):
    try:
        details={}
        for key, value in kwargs.items():
            details[key]=value
        return details
    except ValueError:
        print("Error")

def org_urls(dfRow,*argv):
    urls={}
    urlsR=[]
    for arg in argv:
        #print("argumentos de *argv:", row[arg])
        if len(dfRow[arg])>0:
            if (dfRow[arg].find("http://")!=-1 or dfRow[arg].find("https://")!=-1): 
                urls['value']=dfRow[arg]
            else:
                urls['value']="http://"+dfRow[arg]
                urls['notes']=""#dfRow[arg]
            if dfRow[arg+1]: urls['description']=dfRow[arg+1]
            if dfRow[arg+2]: urls['language']="eng"
            if dfRow[arg+3]: urls['categories']=org_categorie(dfRow[arg+3])
            if dfRow[arg+4]: urls['notes']=""
            urlsR.append(urls)
            urls={}
    return urlsR

def org_contacts(dfRow, *argv):
    contactsId=[]
    person={}
    for arg in argv:
        #print("argumentos de *argv:", row[arg])
        if len(dfRow[arg])>0:
            if dfRow[arg]:
                contactprefix= dfRow[arg]
                contactName_temp=str(dfRow[arg])+" "+str(dfRow[arg])
                ContactName=SplitString(contactName_temp)
                FN=str(ContactName[0])
                LN=str(ContactName[1])
            else:
                FN="NaN"
                LN="NaN"
                #Title go to notes and categorical
                #contactTitle="NULL"
                #if namesheet.cell_value(c,4)!="NULL":
                #    contactTitle=str(namesheet.cell_value(c,4))
                #address
            contactLang="en-us"
            contactnotes=""
            addcontnote=True
            if addcontnote:
                if dfRow[arg]:
                    contactnotes=contact_notes(dfRow[arg])

            addcono=True
            if addcono:
                if dfRow[arg]:
                    contactnotes= dfRow[arg]
            #Contacts phone
            contactphoneN=[]
            addpho=True
            if addpho:
                contactphoneN=""
                contactphoneN=org_phoneNumbers(dfRow[arg],23,31,35,39,)
            #Contact emails
            contactemail=[]
            addmails=True
            if addmails:
                contactemail=""
                contactemail=org_emails(dfRow[arg],15,23)

            #Contact Address
            contactaddresses=[]
            addadd=False
            if addadd:
                contactaddresses=""
                contactaddresses=org_addresses(dfRow[arg],47)

            #INACTIVE / ACTIVE
            contactinactive= False
            #Contact URL
            contacturls=[]
            addurl=False
            if addurl:
                contacturls="" 
                contacturls=org_urls(dfRow[arg],43)
                
            contcategories=[]
            if dfRow[6]:
                contcategories=org_categorie(dfRow[arg])
            conID=str(uuid.uuid4())
            contactsId.append(conID)
            #(self,contactID,contactfirstName, contactlastName, contactcategories):
            ctc=contactsClass(conID,FN,LN,contcategories,contactLang)
            #def printcontacts(self,cont_phone,cont_email, cont_address,cont_urls,cont_categories,contactnotes,fileName):
            ctc.printcontactsClass(contactprefix,contactphoneN, contactemail, contactaddresses, contacturls,contcategories,contactnotes,customerName)  
    return contactsId


def org_account(dfRow,*argv):
    accou={}
    accouR=[]
    for arg in argv:
        print("argumentos de *argv:", dfRow[arg])
        accouR.append(accou)
        accou={}
    return accouR

def org_acqunit(dfRow,*argv):
    acqunit={}
    acqunitR=[]
    for arg in argv:
        print("argumentos de *argv:", dfRow[arg])
        acqunit.append(acqunit)
        acquint={}
    return acqunit

def org_agreements(dfRow,*argv):
    agre={}
    for arg in argv:            
        agre["name"]= "History Follower Incentive"
        agre["discount"]= 10
        agre["referenceUrl"]= "http://my_sample_agreement.com"
        agre["notes"]= "note"
    return agre


def contact_notes(dfRow,*argv):
    nt=""
    for arg in argv:
        if (dfRow.find(' - ') !=-1):
            result=dfRow.find(' - ')
            nt=dfRow[result+3:]
        elif (dfRow.find(' -- ') !=-1):
            result=dfRow.find(' -- ')
            nt=dfRow[result+3:]
        elif (dfRow.find('; ') !=-1):
            result=dfRow.find('; ')
            nt=dfRow[result+2:]
        elif (dfRow.find(' | ') !=-1):
            result=dfRow.find(' | ')
            nt=dfRow[result+3:]
        elif (dfRow.find(' / ') !=-1):
            result=dfRow.find(' / ')
            nt=dfRow[result+3:]
        elif (dfRow.find(', ') !=-1):
            result=dfRow.find(', ')
            nt=dfRow[result+2:]
        else:
            nt=dfRow[arg]
    return nt

def org_categorie(valueA):
    catego=[]
    
    if valueA=="company URL":
        catego.append("d963c6fa-7aa8-4b65-8f64-5f119ef17cd1")
    elif valueA=="Office":
        catego.append("6a60106e-6ffb-4e02-a872-f6941f76245e")
    elif valueA=="Fax":
        catego.append("d78d4e2e-11f9-4397-971e-300cb3dd8522")
    elif valueA=="nn":
        catego=[] #GENERAL
    else:
        value=cat(valueA)
        if len(value)>0:
            catego.append(value)
    return catego
#end

def get_licId1(orgname):
        dic={}
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        #https://okapi-macewan.folio.ebsco.com/licenses/licenses?stats=true&term=Teatro Español del Siglo de Oro&match=name
        pathPattern="/licenses/licenses" #?limit=9999&query=code="
        okapi_url="https://okapi-macewan.folio.ebsco.com"
        okapi_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInVzZXJfaWQiOiI4MjEzODdhZS1hNzkxLTQ5NTgtYTg3ZS1jYTFmMDE2NzA2YmUiLCJpYXQiOjE2MTA5MzAwMjEsInRlbmFudCI6ImZzMDAwMDEwMzcifQ.ygLWuFDNUT8No5TF6FD9NNRpNk4Z_iSRVmPmxaH_UsE"
        okapi_tenant="fs00001037"
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="organizations"
        query=f"?stats=true&term="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"{query}"+orgname+"&match=name"
        path = pathPattern+paging_q
        #data=json.dumps(payload)
        url = okapi_url + path
        req = requests.get(url, headers=okapi_headers)
        idorg=[]
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                #print('Datos en formato JSON',json.dumps(json_str))
                rec=json_str["results"]
                #print(json_str)
                l=rec[0]
                if 'id' in l:
                    idorg.append(l['id'])
                    #idorg.append(l['name'])
        if len(idorg)==0:
            return "00000-000000-000000-00000"
        else:
            return idorg
        
def urlValidator(value):
    try:
        valid=False
        #valid=validator.url(str(value))
        if (value.find("http")!= -1):
            #print("Url is valid only for folio ")
            valid=True
        return valid
    except ValueError:
        print("error")
        
def is_empty(data_structure):
    if data_structure:
            #print("No está vacía")
            return False
    else:
            #print("Está vacía")
            return True

def interfacetype(categ):
    catego=[]
    if (categ.find('Admin') != -1): catego.append("Admin")
    if (categ.find('Statistics') != -1): catego.append("Admin")
    if (categ.find('End user') != -1): catego.append("End user")
    if (categ.find('Other') != -1): catego.append("Other")
    if (categ.find('Report') != -1): catego.append("Report")
    return catego


def floatHourToTime(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (
        int(h),
        int(m),
        int(r*60),
    )
    
def cat(categ):
        dic={}
        #https://okapi-liverpool-ac-uk.folio.ebsco.com/organizations-storage/categories?query=value=="Sales"
        pathPattern="/organizations-storage/categories" #?limit=9999&query=code="
        okapi_url="https://okapi-utm.folio.ebsco.com"
        okapi_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsInVzZXJfaWQiOiJiNWM4YzFmOS02YzQxLTRhMzgtYjk1ZS03YTk5ZTgxMTM3MjUiLCJpYXQiOjE2MTg4NTI5NzMsInRlbmFudCI6ImZzMDAwMDEwNTMifQ.kKuVc2PdXuEgQioN2jphmFw4AdVmKkngoYMdZrfSJ54"
        okapi_tenant="fs00001053"
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="categories"
        query=f"query=value=="
        #/finance/funds?query=name==UMPROQ
        search='"'+categ+'"'
        #paging_q = f"?{query}"+search
        paging_q = f"?{query}"+search
        path = pathPattern+paging_q
        #data=json.dumps(payload)
        url = okapi_url + path
        req = requests.get(url, headers=okapi_headers)
        idcat=[]
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idcat.append(l['id'])                   
        return idcat
#END


def exitfile(arch):    
    if os.path.isfile(arch):
        print ("File exist")
        os.remove(arch)
    else:
        print ("File not exist")


def search(fileB,code_search):
    idlicense=""
    foundc=False
    with open(fileB,'r',encoding = 'utf-8') as h:
        for lineh in h:
            if (lineh.find(code_search) != -1):
                #print(lineh)
                foundc=True
                if (foundc):                    
                    idlicense=lineh[8:44]
                    break
    if (foundc):
        return idlicense
    else:
        idlicense="No Vendor"
        return idlicense

def SearchJsonFile_UTM(code_search,schema):
        # Opening JSON file
        dic =""
        f = open("UTM/categories.json",)
        data = json.load(f)
        for i in data[schema]:
            a_line=str(i)
            if i['value'] == code_search:
            #if (a_line.find(code_search) !=-1):
                 dic=i['id']

                 break
        f.close()
        return dic
    
def SearchJsonFile(code_search,code_return,**kwargs ):
        # Opening JSON file
        dic =""
        f = open(kwargs['filetosearch'],)
        data = json.load(f)
        for i in data[kwargs['schema']]:
            if i[kwargs['field']] == code_search:
            #if (a_line.find(code_search) !=-1):
                 dic=i[code_return]

                 break
        f.close()
        return dic
    
def SplitString(string_to_split):
    string_fn=""
    string_ln=""
    if (string_to_split.find('@') !=-1):
            result=string_to_split.find('@')
            largo=len(string_to_split)
            #print("largo:", largo)
            #print("position @:",result)
            string_fn=" "
            string_ln=string_to_split[0:result]
    elif (string_to_split.find(' ') !=-1):
            largo=len(string_to_split)
            result=string_to_split.find(' ')
            #print("Large:", largo)
            #print("position blank:",result)
            string_fn=string_to_split[0:result]
            string_ln=string_to_split[result+1:largo]
            if (string_ln.find(' - ') !=-1):
                result=string_ln.find(' - ')
                #print("Large:", largo)
                #print("position blank:",result)
                string_ln=string_ln[:result]
            elif (string_ln.find(', ') !=-1):
                result=string_ln.find(', ')
                #print("Large:", largo)
                #print("position blank:",result)
                string_ln=string_ln[:result]


    else:
            #print("is not last name, first name")    
            string_fn=" "
            string_ln=string_to_split
    return string_fn, string_ln

###########################
### LICENCES FUNCTIONS
##########################

def get_licId(licToSearch,okapi_url,okapi_token,okapi_tenant):
    try:
        dic={}
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        #https://okapi-macewan.folio.ebsco.com/licenses/licenses?stats=true&term=Teatro Español del Siglo de Oro&match=name
        pathPattern="/licenses/licenses" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        element="organizations"
        query=f"?stats=true&term="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"{query}"+licToSearch+"&match=name"
        path = pathPattern+paging_q
        #data=json.dumps(payload)
        url = okapi_url + path
        req = requests.get(url, headers=okapi_headers)
        idorg=""
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                #print('Datos en formato JSON',json.dumps(json_str))
                rec=json_str["results"]
                #print(json_str)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']
                    #idorg.append(l['name'])
                    return idorg
    except ValueError as error:
            print("Error: %s" % error)

######END

###################
###NOTES
###########################
### FUNDS
#############

def readfunds(path,sheetName,customerName):
        try:
            be={"AnnisWaterResearchCenter":"AWRI",
                             "BrooksCollegeofInterdisciplinaryStudies":"BCOIS",
                             "ClinicalLaboratorySciences":"CLS",
                             "CollegeofCommunityandPublicServices":"CCPS",
                             "CollegeofEducation":"COE",
                             "CollegeofEducationFunding":"COE$",
                             "CollegeofHealthProfessions":"CHS",
                             "CollegeofLiberalArtsandSciences":"CLAS",
                             "GeneralFunds":"GEN",
                             "InterlibraryLoanBookPurchases":"ILL",
                             "JuvenileMaterials":"JUV",
                             "KirkhofCollegeofNursing":"KCON",
                             "PadnosCollegeofEngineeringandComputing-Computer Science":"PCECC",
                             "PadnosCollegeofEngineeringandComputing-Engineering":"PCECE",
                             "SeidmanCollegeofBusiness":"SCB"
                             }
            funds= faf.readFileToDataFrame(path,orderby="",distinct=[])            
            count=1
            for c, row in funds.iterrows():
                cp={}
                if row[0]:
                    searchvalue=row[0]
                    budgetId=faf.get_Id(customerName,searchValue=searchvalue,element="budgets")
                    searchvalue=row[1]
                    searchvalue=faf.searchKeysByVal(be, searchvalue)      
                    expId=faf.get_Id(customerName,searchValue=searchvalue,element="expenseClasses")
                    cp["id"]=str(row[2])
                    cp["budgetId"]=budgetId
                    cp["expenseClassId"]=expId
                    cp["status"]="Active"
                    count+=1
                    
                    faf.printObject(cp,path,count)
        except ValueError as error:
            print("Error: %s" % error)                 

def exportDataFrame(df,file_path,**kwargs):
    pathprint=file_path[:-5]
    df.to_csv(pathprint, index = False)

def createDataFrame(columnsDataframe):
    df = pd.DataFrame(columns = columnsDataframe)
    return df

def importDataFrame(file_path,**kwargs):
    try:
        orderby=kwargs['orderby']
        distinct=kwargs['distinct']
        filename = r"{}".format(file_path)
        if filename[-4:] == ".csv":
            df = pd.read_csv(filename)
        elif filename[-4:] == ".tsv":
            sep=kwargs['delimiter']
            if sep: df = pd.read_csv(filename, sep='\t')
            else: df = pd.read_csv(filename)
        else:
            if kwargs['sheetName']=="": df = pd.read_excel(filename, engine='openpyxl')
            else: df = pd.read_excel(filename, engine='openpyxl', sheet_name=kwargs['sheetName'])
                
        #license = license.sort_values(by="RECORD #(LICENSE)", ascending=False)
        print("Total rows: {0}".format(len(df)))
        #print(df.shape)
        print(df.columns)
        df = df.apply(lambda x: x.fillna(""))
        #de= df.sort_values(orderby, inplace = True)
        #print(df)
        #print(type(df))
        #df = df.infer_objects()
        #df[distinct]=df[distinct].astype('str')
        if len(distinct)>0:
            df_unique =df.drop_duplicates(subset =distinct, keep="first", inplace=False,ignore_index=True)
            print("Total rows without duplicated records: {0}".format(len(df_unique)))
            df=df_unique
            #df_unique =df.drop_duplicates(subset =distinct, keep="first", inplace=True,ignore_index=True) 
            #df_unique =df.drop_duplicates(subset =orderby, keep="first", inplace=True,ignore_index=True) 
            #df_unique = df.drop_duplicates(subset=orderby, keep="first", inplace=True)
            #print("Total rows: {0}".format(len(df)))
            #print(df)
            #duplicates = df[df.duplicated(['PO number', 'Subscription from', 'Subscription to'])]
            #print(duplicates)
            #duplicate = df[df['PO number'].duplicated(keep=False)]['PO number'].tolist()
            #set_duplicate = set(duplicate)
            #for r in set_duplicate:
            #    dup = df[df['PO number'] == r]
            #    print(dup)
                
            #    df.loc[dup.iloc[1,:].name, 'PO number'] = str(df.loc[dup.iloc[1,:].name]['PO number'])+"z"
            #print(df.duplicated().sum())
            #print(df)
            #dfdropped=df.drop_duplicates(subset=distinct, keep='first')
            #df_nodup = df.groupby(by=distinct).first()
            #print("Total rows: {0}".format(len(df_nodup)))
            
            #df = df.merge(df_nodup, left_on=[distinct], right_index=True, suffixes=('', '_dupindex'))
            #print("Total rows: {0}".format(len(dfdropped)))
            #print(dfdropped)
            #df=dfdropped
            #dfdropped=df.drop_duplicates(distinct)
            #dfdropped = dfdropped.apply(lambda x: x.fillna(""))
            #print(dfdropped)
            #print("Total rows: {0}".format(len(df_nodup)))
            
        #print('\n'*5)
        #Cleaning licenses section for vendorsframe
        #Replacing NaN content by blank
        
        #df = df.replace("-","", regex=True)
        #print(df.to_string(index=False,max_rows=5))
        #duplicate = df[df.duplicated(['PO number', 'Subscription from', 'Subscription to'])]
        #duplicate = df[df.duplicated([orderby])]
        #duplicated=df[df.duplicated()]
        #print("Duplicate records"+str(duplicate))
        #print("Total duplicated records= ",df.duplicated(subset = orderby).sum())
        #group=duplicate.groupby(orderby).first()
        #print("agrupados: "+str(group))
        #df.concat(g for _, g in df.groupby(orderby) if len(g) > 1)
        #is there duplicated content in the orgCode?
        #print("Duplicate vendors= ",df.duplicated(subset = 'RECORD #(LICENSE)').sum())
        return df
    except ImportError:
        from io import StringIO



def readFileToDataFrame(file_path,**kwargs):
    try:

        orderby=kwargs['orderby']
        distinct=kwargs['distinct']
        sep=kwargs['sep']
        filename = r"{}".format(file_path)
        if filename[-4:] == ".csv":
                if sep:
                    df = pd.read_csv(filename, sep='\t')
                else:
                    df = pd.read_csv(filename)
        else:
                df = pd.read_excel(filename, engine='openpyxl')
        #license = license.sort_values(by="RECORD #(LICENSE)", ascending=False)
        print("Total rows: {0}".format(len(df)))
        print(df.columns)
        if len(distinct)>0:
            dfdropped=df.drop_duplicates(distinct)
            print(dfdropped)
            print("Total rows: {0}".format(len(dfdropped)))
            print("Total duplicated records= ",dfdropped.duplicated(subset = orderby).sum())
        #print('\n'*5)
        #Cleaning licenses section for vendorsframe
        #Replacing NaN content by blank
        df = df.apply(lambda x: x.fillna(""))
        #df = df.replace("-","", regex=True)
        print(df.to_string(index=False,max_rows=10))
        #duplicate = df[df.duplicated(['PO number', 'Subscription from', 'Subscription to'])]
        #duplicate = df[df.duplicated([orderby])]
        #duplicated=df[df.duplicated()]
        #print("Duplicate records"+str(duplicate))
        #print("Total duplicated records= ",df.duplicated(subset = orderby).sum())
        #group=duplicate.groupby(orderby).first()
        #print("agrupados: "+str(group))
        #df.concat(g for _, g in df.groupby(orderby) if len(g) > 1)
        #is there duplicated content in the orgCode?
        #print("Duplicate vendors= ",df.duplicated(subset = 'RECORD #(LICENSE)').sum())
        return df
    except ValueError as error:
            print("Error: %s" % error)   

#def acquisitionMethod(value):
#    try:
#        acquisition_Method={"A":"Approval Plan", 
#                            "DDA":"Demand Driven Acquisitions (DDA)",
#                            "D":"Depository", "EBA":"Evidence Based Acquisitions (EBA)",
#                            "E":"Exchange", "Gift":"Gift",
#                            "Purchase At Vendor System":"Purchase At Vendor System", "Technical":"Technical"
#                            }
#    except ValueError as error:
#            print("Error: %s" % error)

def get_Id(customerName, **kwargs):
    try:
        #print(kwargs)
        pathPattern1=okapiPath(kwargs['element'])
        element=kwargs['element']
        pathPattern=pathPattern1[0]
        searchValue=kwargs['searchValue']
        client=SearchClient(customerName)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        #pathPattern1="/organizations/organizations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        #element="organizations"
        query=f"query=code=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']

                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=name=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']

                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
        
def get_Id_with_values(customerName, **kwargs):
    try:
        #print(kwargs)
        pathPattern1=okapiPath(kwargs['element'])
        element=kwargs['element']
        searchValue=kwargs['searchValue']
        pathPattern=pathPattern1[0]
        client=SearchClient(customerName)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        #pathPattern1="/organizations/organizations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        #element="organizations"
        query="query="+kwargs['query']+"="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']

                    return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")
        
                        
def get_Id_value(customerName, **kwargs):
    try:
        #print(kwargs)
        pathPattern1=okapiPath(kwargs['element'])
        element=kwargs['element']
        pathPattern=pathPattern1[0]
        searchValue=kwargs['searchValue']
        client=SearchClient(customerName)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        #pathPattern1="/organizations/organizations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        #element="organizations"
        query=f"query=value=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if 'id' in l:
                    idorg=l['id']

                    return idorg
            #Search by code
            elif (total_recs==0):
                query=f"query=name=="
                paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
                #paging_q = f"?{query}"+orgname
                path1 = pathPattern+paging_q
                #data=json.dumps(payload)
                url1 = okapi_url + path1
                req = requests.get(url1, headers=okapi_headers)
                json_str = json.loads(req.text)
                total_recs = int(json_str["totalRecords"])
                if (total_recs!=0):
                    rec=json_str[element]
                    #print(rec)
                    l=rec[0]
                    if 'id' in l:
                        idorg=l['id']

                        return idorg
    except requests.exceptions.HTTPError as err:
        print("error Organization GET")



     
def get_Id1(customerName, **kwargs):
    try:
        #print(kwargs)
        pathPattern1=okapiPath(kwargs['element'])
        element=kwargs['element']
        pathPattern=pathPattern1[0]
        searchValue=kwargs['searchValue']
        client=SearchClient(customerName)
        okapi_url=str(client.get('x_okapi_url'))
        okapi_tenant=str(client.get('x_okapi_tenant'))
        okapi_token=str(client.get('x_okapi_token'))
        dic={}
        path1=""        
        #pathPattern="/organizations-storage/organizations" #?limit=9999&query=code="
        #pathPattern1="/organizations/organizations" #?limit=9999&query=code="
        okapi_headers = {"x-okapi-token": okapi_token,"x-okapi-tenant": okapi_tenant,"content-type": "application/json"}
        length="1"
        start="1"
        #element="organizations"
        query=f"query=username=="
        #/organizations-storage/organizations?query=code==UMPROQ
        paging_q = f"?{query}"+'"'+f"{searchValue}"+'"'
        #paging_q = f"?{query}"+search_string
        path1 = pathPattern+paging_q
        #data=json.dumps(payload)
        url1 = okapi_url + path1
        req = requests.get(url1, headers=okapi_headers)
        idorg=""
        #Search by name
        if req.status_code != 201:
            json_str = json.loads(req.text)
            total_recs = int(json_str["totalRecords"])
            if (total_recs!=0):
                rec=json_str[element]
                #print(rec)
                l=rec[0]
                if kwargs['id'] in l:
                    idorg=l['barcode']
            #Search by code
        return idorg   
    except Exception as err:
        print("error ", str(err))
        idorg="nobarcode"
        return idorg
    
def readJsonfile_1(path,json_file,schema):
    try:
        f = open(json_file)
        data = json.load(f)
        count=0
        con={}
        lic={}
        for i in data[schema]:
            count+=1
            print("record: "+str(count))
            j_content=i
            id=j_content['id']
            if j_content['customProperties']['InterlibraryLoan'] is not None:
                interlibraryLoanId=""
                interlibraryLoaninternal=""
                interlibraryLoanvalue=""
                interlibraryLoanId=j_content['customProperties']['InterlibraryLoan'][0]['id']
                interlibraryLoaninternal=j_content['customProperties']['InterlibraryLoan'][0]['internal']
                interlibraryLoanvalue=j_content['customProperties']['InterlibraryLoan'][0]['value']
                lic['id']=str(id)
                lic['customProperties']={"InterlibraryLoan":[{"id": interlibraryLoanId ,"internal":False}]}
                printObject(lic,path,str(count),"Inter_lic_to_change",False)
            if j_content['customProperties']['ConcurrentUsers'] is not None:
                interlibraryLoanId=""
                interlibraryLoaninternal=""
                interlibraryLoanvalue=""
                interlibraryLoanId=j_content['customProperties']['ConcurrentUsers'][0]['id']
                interlibraryLoaninternal=j_content['customProperties']['ConcurrentUsers'][0]['internal']
                interlibraryLoanvalue=j_content['customProperties']['ConcurrentUsers'][0]['value']
                con['id']=str(id)
                con['customProperties']={"ConcurrentUsers":[{"id": interlibraryLoanId ,"internal":False}]}
                printObject(con,path,str(count),"concurrent_lic_to_change",False)
    except Exception as err:
        print("error ", str(err))

def readJsonfile_Cornell(path,json_file,schema):
    try:
        f = open(json_file)
        data = json.load(f)
        count=0
        con={}
        lic={}
        for i in data[schema]:
            count+=1
            print("record: "+str(count))
            j_content=i
            #print(j_content)
            #print(j_content['compositePoLines'][0]['acquisitionMethod'])
            c=0
            if j_content['compositePoLines'][0]['acquisitionMethod']=="Approval":
               printObject(j_content,path,str(count),"cornell_purchaseOrders_approvalPlan",False)               
    except Exception as err:
        print("error ", str(err))

def readJsonfile_mls(path,json_file,schema):
    try:
        f = open(path+"\\"+json_file)
        data = json.load(f)
        count=0
        con={}
        lic={}
        for i in data[schema]:
            count+=1
            print("record: "+str(count))
            j_content=i
            id=j_content['code']
            name=j_content['name']
            printObject(id+","+name,path,str(count),"michigan_location_codes",False)
    except Exception as err:
        print("error ", str(err))
        
def readJsonfile(path,json_file,schema,toSearch,fielTosearch):
    try:
        f = open(path+"\\"+json_file)
        data = json.load(f)
        count=0
        con={}
        lic={}
        for i in data[schema]:
            count+=1
            j_content=i
            if j_content[fielTosearch]==toSearch:
                id=j_content['id']
                return id
    except Exception as err:
        return None
        print("error ", str(err))
        
def readJsonfile_identifier(path,json_file,schema,toSearch,tovalue):
    try:
        f = open(path+"\\"+json_file)
        data = json.load(f)
        count=0
        con={}
        lic={}
        sw=False
        for i in data[schema]:
            count+=1
            j_content=i
            if j_content['title']==toSearch:
                if len(j_content['identifiers'])>0:
                    for x in j_content['identifiers']:
                        if x['value']==tovalue:
                            sw= True
        if sw:
           return sw
        else:
            return None
    except Exception as err:
        return None
        print("error ", str(err))

def readJsonfile_fund(path,json_file,schema,toSearch,fielTosearch):
    try:
        f = open(path+"\\"+json_file)
        data = json.load(f)
        count=0
        con={}
        lic={}
        id=[]
        for i in data[schema]:
            count+=1
            j_content=i
            if j_content[fielTosearch]==toSearch:
                id.append(j_content['id'])
                id.append(j_content['code'])
                return id
    except Exception as err:
        return None
        print("error ", str(err))
