import pandas as pd

#Pt intro call handling (yes or no)
''' Pt Intro call handling'''
def pt_intro(row):
    try:
        if row["PT INTRO CALL"]=="YES":
            return row["Date"]
        elif row["PT INTRO CALL"]=="RNR":  #change in aiswarya's
            return "RNR"
        else:
            return "no_call"
    except:
        if row["Call Status "]=="YES":
            return row["Date"]
        elif row["Call Status "]=="RNR":  #change in aiswarya's
            return "RNR"
        else:
            return "no_call"


'''no.of days identifier'''
def no_of_days(row):        #no.of days identifier
    if row["Date"]== "no_call":
        days= 1000
        return days
    elif row["Date"]=="RNR":
        days=2000   #change in aiswarya's        days= 2000
        return days
    else:
        days=pd.datetime.now().date()-row['Date'].date()
        return days.days

'''marking never called and RNR'''
def never_called(column):
    if column==1000:
        column="Never_called"
        return column
    elif column==2000:
        column="RNR"
        return column  #change in aiswarya's
    else:
        return column


for sheetname in ["Anoop M","Aiswarya Anand K","Raja"]:
    #sheetname="Anoop M"
    try:
        call_list= pd.read_excel(r"D:\python programs\Data Analysis\Vedantuptintro\Call_list.xlsx",sheet_name=sheetname, header=0,parse_dates=["Date"])
    except:
        print("Error in reading file {}".format(sheetname))
        continue
    for col in ["Support","Benchmark test","% Age","Unnamed: 17","Unnamed: 18","Unnamed: 19","Unnamed: 20","Unnamed: 21","Unnamed: 22","Unnamed: 23","Unnamed: 24","Unnamed: 25","Unnamed: 26","Unnamed: 27","Unnamed: 28","Unnamed: 29","Unnamed: 30"]:
        try:
            call_list.drop([col],axis=1,inplace=True)
        except:
            continue
    try:
        call_list= call_list[call_list["ACCOUNT STATUS (Col29)"]=="Active"] #active inactive list handling
    except:
        call_list= call_list[call_list["Status2nd April"]=="Active"]

    call_list["Date"]= call_list.apply(pt_intro,axis=1)

    call_list["Date"]= call_list["Date"].fillna("no_call") #calls not made yet

    call_list["No.of_days"]=call_list.apply(no_of_days,axis=1)
    call_list_today=call_list.sort_values("No.of_days",ascending=False)  #sorting
    call_list_today["No.of_days"]=call_list_today["No.of_days"].apply(never_called)
    '''
    import datetime as dt
    def todate(DT):
        try:
            DatE= dt.datetime.strptime(DT, "%d-%m-%Y")
            DatE= DatE.date().isoformat()
            return DatE
        except:
            return DT
        call_list_today["Date"]=call_list_today["Date"].apply(todate)
    '''
    today=pd.datetime.now().date()
    save_location="D:\python programs\Data Analysis\Vedantuptintro\A_Test\call_list_{}_{}.xlsx".format(sheetname,today)
    print(save_location)
    try:
        call_list_today.to_excel(save_location, sheet_name=sheetname,index=False)
    except:
        print("Error occured while saving the file")
    finally:
        print("End")
