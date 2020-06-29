#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random

all_marks=pd.read_excel(r'D:\python programs\Data Analysis\Student seggregation\Results\compare_JEE__all_marks.xlsx',headers=0)
print(all_marks.head())


for col in all_marks.columns:
    if col not in ['Group Name','Email','Name','Contact No'] and '% Age' not in col:
        all_marks.drop(col,axis=1,inplace=True)
    if '% Age' in col:
        all_marks[col]=all_marks[col]*100


print('shape',all_marks.shape)

all_marks.fillna(value=0,inplace=True) #na can be filled with 0 as it is Marks

'''
def plot_graph(all_marks_list,exam_names_list,exam):
    print('plot_graph initiated')
    fig=plt.figure(figsize=(20,10))
    color_set=['indianred','firebrick','salmon','orangered','burlywood','goldenrod','teal','cornflowerblue','plum','orchid']
    print('for loop')
    for sub_marks_list,i in zip(all_marks_list,range(len(all_marks_list))):
        if exam=="Mains":
            j=i+1
        elif exam=="Adv":
            j=i+5
        print('exam checked')
        if i==0:
            title="Total Marks"
        elif i==1:
            title= "Maths Marks"
        elif i==2:
            title= "Physics Marks"
        elif i==3:
            title="Chemistry Marks"
        print('exam ',exam)
        print('title decided ',title)
        print(type(exam),type(title))
        ax=plt.subplot(2,4,j)
        print('subplot created')
        print(exam_names_list,sub_marks_list)
        barg=ax.bar(exam_names_list,sub_marks_list,color=random.choice(color_set))

        print(exam+title)
        plt.ylim(0,105)
        ax.set_title(title+' '+'('+exam+')')
        for rect in barg:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.02*height,'%d' % int(height),ha='center', va='bottom')



    plt.show()

    if exam=="mains":
        return 1
    elif exam=="adv":
        return 2



'''

def proceed_stdn(all_marks_stdn):

    print("proceed_stdn initiated")
    print("all_marks_stdn",all_marks_stdn)
    grp_name= all_marks_stdn["Group Name"]
    mains_list=['BMM_0','MT_1','MT_2','MT_3']

    Total_mains=[all_marks_stdn['% Age_t_{}'.format('BMM_0')],all_marks_stdn['% Age_t_{}'.format('MT_1')],all_marks_stdn['% Age_t_{}'.format('MT_2')],all_marks_stdn['% Age_t_{}'.format('MT_3')]]
    Maths_mains=[all_marks_stdn['% Age_m_{}'.format('BMM_0')],all_marks_stdn['% Age_m_{}'.format('MT_1')],all_marks_stdn['% Age_m_{}'.format('MT_2')],all_marks_stdn['% Age_m_{}'.format('MT_3')]]
    Physics_mains=[all_marks_stdn['% Age_p_{}'.format('BMM_0')],all_marks_stdn['% Age_p_{}'.format('MT_1')],all_marks_stdn['% Age_p_{}'.format('MT_2')],all_marks_stdn['% Age_p_{}'.format('MT_3')]]
    Chemistry_mains=[all_marks_stdn['% Age_c_{}'.format('BMM_0')],all_marks_stdn['% Age_c_{}'.format('MT_1')],all_marks_stdn['% Age_c_{}'.format('MT_2')],all_marks_stdn['% Age_c_{}'.format('MT_3')]]
    print("Total")
    print(Total_mains)

    adv_list=['BMA_0','AT_1','AT_2','AT_3']

    Total_adv=[all_marks_stdn['% Age_t_{}'.format('BMA_0')],all_marks_stdn['% Age_t_{}'.format('AT_1')],all_marks_stdn['% Age_t_{}'.format('AT_2')],all_marks_stdn['% Age_t_{}'.format('AT_3')]]
    Maths_adv=[all_marks_stdn['% Age_m_{}'.format('BMA_0')],all_marks_stdn['% Age_m_{}'.format('AT_1')],all_marks_stdn['% Age_m_{}'.format('AT_2')],all_marks_stdn['% Age_m_{}'.format('AT_3')]]
    Physics_adv=[all_marks_stdn['% Age_p_{}'.format('BMA_0')],all_marks_stdn['% Age_p_{}'.format('AT_1')],all_marks_stdn['% Age_p_{}'.format('AT_2')],all_marks_stdn['% Age_p_{}'.format('AT_3')]]
    Chemistry_adv=[all_marks_stdn['% Age_c_{}'.format('BMA_0')],all_marks_stdn['% Age_c_{}'.format('AT_1')],all_marks_stdn['% Age_c_{}'.format('AT_2')],all_marks_stdn['% Age_c_{}'.format('AT_3')]]

    mains_all_marks_std_list= [Total_mains,Maths_mains,Physics_mains,Chemistry_mains]
    adv_all_marks_std_list= [Total_adv,Maths_adv,Physics_adv,Chemistry_adv]

    fig=plt.figure(figsize=(16,12))
    for exam_all_marks_std_list,exam_names_list,exam in zip([mains_all_marks_std_list,adv_all_marks_std_list],[mains_list,adv_list],["Mains","Adv"]):
        print('exam',exam)
        print('exam_names_list',exam_names_list)
        print('plot_graph initiated')

        color_set=['indianred','firebrick','salmon','orangered','burlywood','goldenrod','teal','cornflowerblue','plum','orchid']
        print('for loop')
        for sub_marks_list,i in zip(exam_all_marks_std_list,range(len(exam_all_marks_std_list))):
            if exam=="Mains":
                j=i+1
            elif exam=="Adv":
                j=i+5
            print('exam checked')
            if i==0:
                title="Total Marks"
            elif i==1:
                title= "Maths Marks"
            elif i==2:
                title= "Physics Marks"
            elif i==3:
                title="Chemistry Marks"
            print('exam ',exam)
            print('title decided ',title)
            print(type(exam),type(title))
            ax=plt.subplot(2,4,j)
            print('subplot created')
            print(exam_names_list,sub_marks_list)
            barg=ax.bar(exam_names_list,sub_marks_list,color=random.choice(color_set))

            print(exam + ' '+title)
            plt.ylim(0,105)
            #ax.set_ylabel("Marks in %")
            ax.set_title(title+' '+'('+exam+')')
            #ax.set_title(exam+title)
            for rect in barg:
                height = rect.get_height()
                if height !=0:
                    ax.text(rect.get_x() + rect.get_width()/2., 1.02*height,'{}{}'.format(int(height),'%'),ha='center', va='bottom')

            #k=1
            for spine1 in ax.spines.values():
                #if k%2 ==0:
                spine1.set_visible(False)
                    #spine2.set_visible(False)
                #k=k+1
            #plt.tight_layout()
            #ax.axes.xaxis.set_ticks([])
            ax.axes.yaxis.set_ticks([])
            #ax.axes.xaxis.set_ticklabels([])
            ax.axes.yaxis.set_ticklabels([])



    plt.subplots_adjust(top=0.90,hspace=0.5)
    fig.suptitle(grp_name)
    plt.show()



check_set=all_marks["Email"].unique()
check="next"
while check != "exit":

    student_email=input("Enter student's email id- ")
    if student_email=="exit":
        break

    elif student_email in check_set:
        all_marks_stdn=all_marks[(all_marks["Email"]==student_email)]
        all_marks_stdn.apply(proceed_stdn,axis=1)

    else:
        print("Student not found")
        continue
