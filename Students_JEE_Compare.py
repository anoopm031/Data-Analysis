#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


# # Reading benchmark tests and making it into bm mains and bm advanced
BM=pd.read_excel(r'D:\python programs\Data Analysis\Student seggregation\JEE 12 .xlsx',sheet_name='Benchmark overall Result(Eng+Hi',header=2)


# # Drop Right wrong and left columns of dataset

# In[5]:
def drop_rwl(df):
    col_names=df.columns
    for col in col_names:
        if 'Right' in col or 'Wrong' in col or 'Left' in col or 'Unnamed' in col:
            df.drop([col],axis=1,inplace=True)

    return df


# In[6]:
BM_Mains= BM.loc[:,:'Max Marks.3'].copy()


print(BM_Mains.head())

BM_Mains.rename(columns={'% Age':'% Age.0','Marks Scored':'Marks Scored.0','Max Marks':'Max Marks.0'},inplace=True)

print(BM.columns)


BM_Adv=BM[['Test Date', 'Group Name', 'Email', 'Name', 'Contact No','% Age.4',
       'Marks Scored.4', 'Max Marks.4', '% Age.5',
       'Marks Scored.5', 'Max Marks.5', '% Age.6', 'Marks Scored.6',
       'Max Marks.6', '% Age.7', 'Marks Scored.7', 'Max Marks.7']].copy()



# ## Function to clean data columns to p,m,c,t

def clean_pcm(df):
    col=df.columns
    for col in col:
        try:
            param,num=col.split('.')
            if num=='0' or num=='4':
                num='m'
                ncol='_'.join([param,num])
                df.rename(columns={col:ncol},inplace=True)
            elif num=='1' or num=='5':
                num='p'
                ncol='_'.join([param,num])
                df.rename(columns={col:ncol},inplace=True)
            elif num=='2' or num=='6':
                num='c'
                ncol='_'.join([param,num])
                df.rename(columns={col:ncol},inplace=True)
            elif num=='3' or num=='7':
                num='t'
                ncol='_'.join([param,num])
                df.rename(columns={col:ncol},inplace=True)
        except:
            continue

    return df


# ## systematic reading and cleaning of all test data

Mains_tests=["Main Test  1","Main Test  2","Main Test  3"]
Adv_tests=["Adv Test 1","Adv Test 2","Adv Test 3"]


## function to find the average of paper 1 and 2 in adv papers and to rename columns
def adv_test_t1t2_adder(AT):
    for sub,i,j in zip(['m','p','c','t'],['0','1','2','3'],['4','5','6','7']):
        AT["% Age_{}".format(sub)]=(AT["% Age.{}".format(i)]+AT["% Age.{}".format(j)])/2
        AT["Marks Scored_{}".format(sub)]=(AT["Marks Scored.{}".format(i)]+AT["Marks Scored.{}".format(j)])/2
        AT["Max Marks_{}".format(sub)]=(AT["Max Marks.{}".format(i)]+AT["Max Marks.{}".format(j)])/2
        AT.drop(["% Age.{}".format(i),"% Age.{}".format(j),"Marks Scored.{}".format(i),"Marks Scored.{}".format(j),"Max Marks.{}".format(i),
                 "Max Marks.{}".format(j)],axis=1,inplace=True)
    return AT


# In[18]:
def test_dict_gen(test_name_list):
    print("reading mains and adv data initialized")
    test_dict={}
    for test in test_name_list:
        name_split=test.split()
        dict_key=name_split[0][0]+name_split[1][0]+'_'+name_split[2]
        if name_split[0][0]=="M":
            MT=pd.read_excel(r'D:\python programs\Data Analysis\Student seggregation\JEE 12 .xlsx',sheet_name=test,header=1)
            MT.rename(columns={'% Age':'% Age.0','Marks Scored':'Marks Scored.0','Max Marks':'Max Marks.0'},inplace=True)
            test_dict[dict_key]=MT
        elif name_split[0][0]=="A":
            AT=pd.read_excel(r'D:\python programs\Data Analysis\Student seggregation\JEE 12 .xlsx',sheet_name=test,header=2)
            AT.rename(columns={'% Age':'% Age.0','Marks Scored':'Marks Scored.0','Max Marks':'Max Marks.0'},inplace=True)
            AT1=adv_test_t1t2_adder(AT)
            test_dict[dict_key]=AT1

    print("reading mains and adv data done")
    return test_dict


# In[19]:
## Calling generator functions to read datasets and create test dicts

main_dict=test_dict_gen(Mains_tests)  #creates a dict with "MT_1: Mains Test  1 df format for all mains tests"
adv_dict=test_dict_gen(Adv_tests)         #creates a dict with "AT_1: Adv Test 1 df format for all mains tests"
main_dict['BMM_0']= BM_Mains
adv_dict['BMA_0']= BM_Adv



# Advanced tests will be compared on phase 2 of the project (part two included here)

# ## clean  all dfs
# In[29]:
for test in main_dict.keys():
    main_dict[test]=drop_rwl(main_dict[test])
    main_dict[test]=clean_pcm(main_dict[test])

for test in adv_dict.keys():
    adv_dict[test]=drop_rwl(adv_dict[test])
    #clean_pcm(adv_dict[test])   no need to do as it is already cleaned for pcm during reding function

adv_dict["BMA_0"]=clean_pcm(adv_dict["BMA_0"])


# In[34]:

#making a list of tuples multiple times
hj=('s','f')
hh=((hj,)*5)
print(hh)



# In[36]:
# # Function to compare dfs

# In[37]:

'''
def compare_fun2(T1,T2,test_dict):
    print(1)
    testsmerge=test_dict[T1].merge(test_dict[T2],how="inner",on=["Email","Group Name"])
    #print(testsmerge.head())
    n_cols=testsmerge.shape[0]
    t1t2_df=comp_details(T1,T2,n_cols)
    testsmerge["Tests"]=t1t2_df["test2"]+'-'+t1t2_df["test1"]
    for s in ["m","p","c","t"]:
        testsmerge["{}_%_diff".format(s)]=(testsmerge["% Age_{}_y".format(s)]-testsmerge["% Age_{}_x".format(s)])*100

        testsmerge["{}_marks_diff".format(s)]=testsmerge["Marks Scored_{}_y".format(s)]-testsmerge["Marks Scored_{}_x".format(s)]
        testsmerge["{}_maxmarks_diff".format(s)]=testsmerge["Max Marks_{}_y".format(s)]-testsmerge["Max Marks_{}_x".format(s)]
    new=testsmerge[[ 'Group Name', 'Email', 'Name_x',
       'Contact No_x',"Tests","m_%_diff","m_marks_diff","m_maxmarks_diff","p_%_diff","p_marks_diff","p_maxmarks_diff","c_%_diff","c_marks_diff","c_maxmarks_diff","t_%_diff","t_marks_diff","t_maxmarks_diff"]].copy()
    print("comp done")
    return new

'''


# ## Function to compare dfs improved

# In[38]:

def compare_fun_all_col(T1,T2,test_dict):
    print("compare_fun_all_col initialized")
    testsmerge=test_dict[T1].merge(test_dict[T2],how="inner",on=["Email","Group Name","Name","Contact No"])
    #print(testsmerge.head())
    n_cols=testsmerge.shape[0]
    t1t2_df=comp_details(T1,T2,n_cols)
    testsmerge["Tests"]=t1t2_df["test2"]+'-'+t1t2_df["test1"]
    new_col_names={}
    for col in testsmerge.columns:
        if "x" in col:
            param=col.split('_')
            #print(param)
            param.pop(-1)
            col_new_1='_'.join(param)
            col_new =col_new_1+'_'+T1
            new_col_names[col]=col_new


        if "y" in col:
            param=col.split('_')
            param.pop(-1)
            col_new_1='_'.join(param)
            col_new=col_new_1+'_'+T2

            new_col_names[col]=col_new
            #print(new_col_names)


    print(new_col_names)
    testsmerge.rename(columns=new_col_names,inplace=True)

    for s in ["m","p","c","t"]:
        testsmerge["{}_%_diff_{}_{}".format(s,T2,T1)]=(testsmerge["% Age_{}_{}".format(s,T2)]-testsmerge["% Age_{}_{}".format(s,T1)])*100

        testsmerge["{}_marks_diff_{}_{}".format(s,T2,T1)]=testsmerge["Marks Scored_{}_{}".format(s,T2)]-testsmerge["Marks Scored_{}_{}".format(s,T1)]
        testsmerge["{}_maxmarks_diff_{}_{}".format(s,T2,T1)]=testsmerge["Max Marks_{}_{}".format(s,T2)]-testsmerge["Max Marks_{}_{}".format(s,T1)]
    new=testsmerge[[ 'Group Name', 'Email', 'Name',
       'Contact No',"Tests","m_%_diff_{}_{}".format(T2,T1),"m_marks_diff_{}_{}".format(T2,T1),"m_maxmarks_diff_{}_{}".format(T2,T1),"p_%_diff_{}_{}".format(T2,T1),"p_marks_diff_{}_{}".format(T2,T1),"p_maxmarks_diff_{}_{}".format(T2,T1),"c_%_diff_{}_{}".format(T2,T1),"c_marks_diff_{}_{}".format(T2,T1),"c_maxmarks_diff_{}_{}".format(T2,T1),"t_%_diff_{}_{}".format(T2,T1),"t_marks_diff_{}_{}".format(T2,T1),"t_maxmarks_diff_{}_{}".format(T2,T1)]]
    print("full col retain comp done")
    return new


# ### Function that'll create a df with column containing compared test details(eg: MT_2-MT-1). This function is called inside compare_fun2 function
# In[39]:
def comp_details(T1,T2,n):
    t1t2=(T2,T1)
    t1t2_t=((t1t2,)*n)
    t1t2_l=list(t1t2_t)
    t1t2_df=pd.DataFrame(t1t2_l,columns=["test2","test1"])
    return t1t2_df


# # Final function calling and storing results in a dictionary

# ## function to compare all the tests cross

# In[42]:
def result_test_dict_gen_cross(test_dict):
    result_test_dict={}
    for T1 in test_dict.keys():
        for T2 in test_dict.keys():
            t_type1,num1=T1.split('_')
            #print(num1)
            t_type2,num2=T2.split('_')
            #print(num2)
            if int(num2)>int(num1):
                print(num1,'>',num2)
                result_test_dict['{}-{}'.format(T2,T1)]=compare_fun_all_col(T1,T2,test_dict) #calling comp_fun2 to create sheets and append it to result main dict
    #comp_type="cross"
    print("result_test_dict_gen_cross done")
    return result_test_dict




# ## function to compare nearer tests
# In[43]:
def result_test_dict_gen_near(test_dict):
    result_test_dict={}
    for T1 in test_dict.keys():
        for T2 in test_dict.keys():
            t_type1,num1=T1.split('_')
            #print(num1)
            t_type2,num2=T2.split('_')
            #print(num2)
            if int(num2)-int(num1)==1:
                print(num1,'-',num2)
                result_test_dict['{}-{}'.format(T2,T1)]=compare_fun_all_col(T1,T2,test_dict)  #calling comp_fun2 to create sheets and append it to result main dict
    #comp_type="near"
    print("result_test_dict_gen_near done")
    return result_test_dict


# In[44]:

## Function to compare and retain all the columns
# In[45]:

'''
def result_main_dict_gen_full(main_dict):
    result_main_dict={}
    for T1 in main_dict.keys():
        for T2 in main_dict.keys():
            t_type1,num1=T1.split('_')
            #print(num1)
            t_type2,num2=T2.split('_')
            #print(num2)
            if int(num2)-int(num1)==1:
                print(num1,'-',num2)
                result_main_dict['{}-{}'.format(T2,T1)]=compare_fun_all_coll(T1,T2,main_dict)  #calling comp_fun2 to create sheets and append it to result main dict
    #comp_type="near"
    print("result_main_dict_gen_full done")
    return result_main_dict


'''


# ## Function to final stitch of all the data sets to one (called inside result_comp functions

# In[46]:


def dfs_merge(result_test_dict):
    test_comp_lists=list(result_test_dict.keys())
    test_comp_lists.reverse()
    result_sheet=result_test_dict[test_comp_lists[0]]
    #result_sheet.head()
    for df_key in test_comp_lists:
        if df_key!=test_comp_lists[0]:
            result_sheet=result_sheet.merge(result_test_dict[df_key],how="outer",on=["Email","Group Name","Name","Contact No"])

    print("dfs_merge done")
    return result_sheet



# ## Function to save the result sheet

def save_final(save_location,result_sheet):
    print("final sheet size =",result_sheet.shape)
    print("save_final done")
    result_sheet.to_excel(save_location,index=False)
    return 1




# ## call function to cross compare or compare nearer tests (mains)
print("Enter 0 for cross compare and 1 for near compare and 3 for near with full columns")
decide=input("Choosse 0 or 1 or 3- ")



#calling result_main dict generator function
if int(decide)==0:
    final_dict={}  #dict used to call dfs_merge to merge mains and adv result sheet
    result_main_dict=result_test_dict_gen_cross(main_dict)
    print("result main",result_main_dict)
    result_sheet_mains=dfs_merge(result_main_dict)
    final_dict["mains"]=result_sheet_mains
    result_adv_dict=result_test_dict_gen_cross(adv_dict)
    result_sheet_adv=dfs_merge(result_adv_dict)
    final_dict["adv"]=result_sheet_adv
    result_sheet_final=dfs_merge(final_dict)
    comp_type="cross"
    save_location="D:\python programs\Data Analysis\Student seggregation\Results\compare_JEE__{}_final.xlsx".format(comp_type)
    print(save_location)
    save_status=save_final(save_location,result_sheet_final)
    if save_status==1:
        print("Successfully saved")
elif int(decide)==1:
    final_dict={}  #dict used to call dfs_merge to merge mains and adv result sheet
    result_main_dict=result_test_dict_gen_near(main_dict) #fun called here is different
    print("result main",result_main_dict)
    result_sheet_mains=dfs_merge(result_main_dict)
    final_dict["mains"]=result_sheet_mains
    result_adv_dict=result_test_dict_gen_near(adv_dict)
    result_sheet_adv=dfs_merge(result_adv_dict)
    final_dict["adv"]=result_sheet_adv
    result_sheet_final=dfs_merge(final_dict)
    comp_type="cross"
    save_location="D:\python programs\Data Analysis\Student seggregation\Results\compare_JEE__{}_final.xlsx".format(comp_type)
    print(save_location)
    save_status=save_final(save_location,result_sheet_final)
    if save_status==1:
        print("Successfully saved")




if int(decide)==3:
    final_dict={}  #dict used to call dfs_merge to merge mains and adv result sheet
    result_main_dict=result_test_dict_gen_near(main_dict) #fun called here is different
    print("result main",result_main_dict)
    result_sheet_mains=dfs_merge(result_main_dict)
    final_dict["mains"]=result_sheet_mains
    result_adv_dict=result_test_dict_gen_near(adv_dict)
    result_sheet_adv=dfs_merge(result_adv_dict)
    final_dict["adv"]=result_sheet_adv
    result_sheet_final=dfs_merge(final_dict)
    comp_type="cross"
    save_location="D:\python programs\Data Analysis\Student seggregation\Results\compare_JEE__{}_final.xlsx".format(comp_type)
    print(save_location)
    save_status=save_final(save_location,result_sheet_final)
    if save_status==1:
        print("Successfully saved")

    for test in main_dict.keys():
        new_col_dict={}
        for cols in main_dict[test].columns:
            if cols not in ["Group Name","Email","Name","Contact No"]:
                new_col_dict[cols]=cols+'_'+test
            print(list(new_col_dict.values()))
            main_dict[test].rename(columns=new_col_dict,inplace=True)

    for test in adv_dict.keys():
        new_col_dict={}
        for cols in adv_dict[test].columns:
            if cols not in ["Group Name","Email","Name","Contact No"]:
                new_col_dict[cols]=cols+'_'+test
            print(list(new_col_dict.values()))
            adv_dict[test].rename(columns=new_col_dict,inplace=True)


    # create a new df with all the test marks alone using merge function
    all_dict={}  # to pass to dfs_merge to get a final df with all test marks
    all_marks_mains=dfs_merge(main_dict)
    all_dict["mains"]=all_marks_mains
    all_marks_adv=dfs_merge(adv_dict)
    all_dict["adv"]=all_marks_adv
    all_marks_final=dfs_merge(all_dict)

    save_location_2= "D:\python programs\Data Analysis\Student seggregation\Results\compare_JEE__all_marks.xlsx"
    save_status_2=save_final(save_location_2,all_marks_final)
    if save_status_2==1:
        print("Successfully saved all amrks df")
