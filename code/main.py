import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from pycricbuzz import Cricbuzz
import math         
import tkinter 
import tkinter.ttk

fixed='https://www.cricbuzz.com'
live='https://www.espncricinfo.com/scores/'
response=requests.get(live)
soup=BeautifulSoup(response.content,'html.parser')
t=len(soup.find_all('span',class_="cscore_name cscore_name--long"))
p=len(soup.find_all('div',class_="cscore_info-overview"))
j=0
ws=[]
for k in range(p):
    v=[]
    if j%2==0:
        place=(soup.find_all('div',class_="cscore_info-overview")[k].get_text())
        pl=place.split(" at ",1)
        if len(pl)>1:
            place=pl[1]
            pl=place.split(",")
            v.append(pl[0])
        k+=1
    for l in range(2):
        v.append((soup.find_all('span',class_="cscore_name cscore_name--long")[j].get_text()))
        j+=1
    

    ws.append(v)
    
c=Cricbuzz()
live_matches=c.matches()
t_name=["India","Pakistan","Australia","Bangladesh","England","Afghanistan","Sri Lanka","New Zealand","South Africa","West Indies"]
w=[]
for i in range(len(ws)):
    for j in range(len(t_name)):
        if ws[i][1]==t_name[j]:
            v=[]
            v.append(ws[i][0])
            v.append(ws[i][1])
            v.append(ws[i][2])
            w.append(v)
            
        

index_r=[]
k=1
index_live=[]
for i in range(len(w)):
    for j in range(len(live_matches)):
        if live_matches[j].get('type')=='ODI':
            ven=live_matches[j].get('venue_location')
            venue=ven.split(",")
            if (w[i][1]==live_matches[j].get('team1').get('name') or w[i][2]==live_matches[j].get('team1').get('name')) and (w[i][0]==venue[0]):
                if live_matches[j].get('mchstate')=='preview' or live_matches[j].get('mchstate')=='inprogress' or live_matches[j].get('mchstate')=='toss': 
                       print(k,".",live_matches[j].get('team1').get('name'),"vs",live_matches[j].get('team2').get('name'),"at",live_matches[j].get('venue_location'),"on",live_matches[j].get('start_time')) 
                       index_r.append(i)
                       index_live.append(j)
                       k+=1
#----------------------------------------------------------------                       
window = tkinter.Tk()
window.title("Cricket Predictor")
window.geometry('700x640')


txt = tkinter.Entry(window,width=10)
txt.grid(column=1, row=2)
txt.focus()
label1=tkinter.Label(window,text="Recent Match Prediction",font=20,bg="cyan",anchor="w")
label1.grid(column=1,row=1)
lbl = tkinter.Label(window, text="Enter no. of Recent Matches* :",font=10,anchor="w")

lbl.grid(column=0, row=2)
lbl_n = tkinter.Label(window, text="* These are the no. of matches \n we are using for test set and rest \n we are using for training set.",anchor="w")

lbl_n.grid(column=0, row=4)
lbl4 = tkinter.Label(window, text="",font=10)
lbl4.grid(column=1, row=5)
lbl5 = tkinter.Label(window, text="",font=10)
lbl5.grid(column=1, row=6)

def recentp():
    
    lbl4.configure(text="")
    lbl5.configure(text="")
    
    dataset = pd.read_csv('match_new.csv')
    xt=dataset.iloc[:,[0,1,3,5,6,7,8]].values
    yt=dataset.iloc[:,[2]].values
        


    from sklearn.preprocessing import LabelEncoder
    labelencoder_y=LabelEncoder()
    yt=labelencoder_y.fit_transform(yt)

    import category_encoders as ce
    ohe = ce.OneHotEncoder(handle_unknown='ignore', use_cat_names=True)
    xt= ohe.fit_transform(xt)

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train , y_test = train_test_split(xt,yt,test_size=0.01, random_state=0)
    
    res=txt.get()
    ik=int(res)
    x_train=xt.iloc[:-ik,:]
    x_test=xt.iloc[-ik:,:]
    y_train=yt[:-ik]
    y_test=yt[-ik:]
    


    from sklearn.preprocessing import StandardScaler
    sc_x=StandardScaler()
    x_train=sc_x.fit_transform(x_train)
    x_test=sc_x.transform(x_test)


    from sklearn.linear_model import LogisticRegression
    classifier=LogisticRegression(multi_class='ovr',solver='liblinear')
    classifier.fit(x_train,y_train)
    y_pred2=classifier.predict(x_test)


    from sklearn.metrics import accuracy_score
    score2 =accuracy_score(y_test,y_pred2)
    score=score2*100
    sco="{:.2f}".format(score)
    if ik<=100:
        lbl4.configure(text=sco,fg="green")
    else:
        lbl4.configure(text=sco,fg="green")
        lbl5.configure(text="Please Enter value Less Than 100",fg="red",font=5)

label=tkinter.Label(window,text="",font=10)  
label.grid(column=0,row=18) 
lbl6=tkinter.Label(window,text="",font=10)
lbl6.grid(column=1,row=19)
lbl7=tkinter.Label(window,text="",font=10)
lbl7.grid(column=1,row=20)
lbl8=tkinter.Label(window,text="",font=8)
lbl8.grid(column=0,row=19)
lbl9=tkinter.Label(window,text="Team Wise Prediction",font=20,bg="cyan")
lbl9.grid(column=1,row=13)

label.configure(text="Actual Winner")
lbl11 = tkinter.Label(window, text="Prediction",font=10)
lbl11.grid(column=1, row=18)

def teamp():
    team_a=combo_a.get()
    team_b=combo_b.get()
    lbl6.configure(text="")
    lbl7.configure(text="")
    lbl8.configure(text="")
    
    
    if team_a!=team_b:
        dataset = pd.read_csv('match_new.csv')
        q1=(dataset.a==team_a) | (dataset.a==team_b) 
        q2=(dataset.b==team_a) | (dataset.b==team_b) 
        query=q1 & q2
        team_vs=dataset[query]
        xt=team_vs.iloc[:,[0,1,3,5,6,7,8]].values
        yt=team_vs.iloc[:,[2]].values
        
        from sklearn.preprocessing import LabelEncoder
        labelencoder_y=LabelEncoder()
        yt=labelencoder_y.fit_transform(yt)

        import category_encoders as ce
        ohe = ce.OneHotEncoder(handle_unknown='ignore', use_cat_names=True)
        xt= ohe.fit_transform(xt)
        
        ik=1
        ik=round(ik)
        
        x_train=xt.iloc[:-ik,:]
        x_test=xt.iloc[-ik:,:]
        y_train=yt[:-ik]
        y_test=yt[-ik:]
        
        from sklearn.preprocessing import StandardScaler
        sc_x=StandardScaler()
        x_train=sc_x.fit_transform(x_train)
        x_test=sc_x.transform(x_test)


        from sklearn.linear_model import LogisticRegression
        classifier=LogisticRegression(multi_class='ovr',solver='liblinear')
        classifier.fit(x_train,y_train)
        y_pred2=classifier.predict(x_test)


        from sklearn.metrics import accuracy_score
        score2 =accuracy_score(y_test,y_pred2)
        
        from sklearn.ensemble import RandomForestClassifier
        classifier=RandomForestClassifier(n_estimators=10,random_state=6)
        classifier.fit(x_train,y_train)
        y_pred3=classifier.predict(x_test)


        score3 =accuracy_score(y_test,y_pred3)
        if score2>=score3:
           
            pred=y_pred2
        else:
           
            pred=y_pred3
        if pred==0:
            if team_a<team_b:
                pre_t=team_a
            else:
                pre_t=team_b
        if pred==1:
            if team_a>team_b:
                pre_t=team_a
            else:
                pre_t=team_b
        
        
       
        lbl8.configure(text=team_vs.iloc[-ik,2])
        if pre_t==team_vs.iloc[-ik,2]:
            lbl6.configure(text=pre_t,fg="green",font=10)
        else:
            lbl6.configure(text=pre_t,fg="red",font=10)
        
    else:
        lbl7.configure(text="Select two Different Teams",fg="red")
btn = tkinter.Button(window, text="Score", command=recentp,font=10,bg="grey",fg="white",width=10)
btn.grid(column=3, row=2)
lbl1 = tkinter.Label(window, text="Prediction Accuracy",font=10)
lbl1.grid(column=1, row=4)
lbl_title=tkinter.Label(window,text="ODI Cricket Predictor",padx=0.1,height=2,width=25,bg='orange',fg='black',font=20)
lbl_title.grid(column=1,row=0)

lbl_a=tkinter.Label(window,text="Team A",anchor="w")
lbl_a.grid(column=0,row=15)
lbl_b=tkinter.Label(window,text="Team B",anchor="w")
lbl_b.grid(column=1,row=15)

combo_a = tkinter.ttk.Combobox(window,state="readonly")
combo_a['values']= ("Afghanistan","Australia","Bangladesh","England","India","New Zealand","Pakistan","South Africa","Sri Lanka","West Indies")
combo_a.current(1) #set the selected item
combo_a.grid(column=0, row=17)

combo_b = tkinter.ttk.Combobox(window,state="readonly")
combo_b['values']= ("Afghanistan","Australia","Bangladesh","England","India","New Zealand","Pakistan","South Africa","Sri Lanka","West Indies")
combo_b.current(5) #set the selected item
combo_b.grid(column=1, row=17)

btn1 = tkinter.Button(window, text="Score", command=teamp,font=10,bg="grey",fg="white",width=10)
btn1.grid(column=3, row=17)

#----------------------------list of ongoing matches--------------------
matches=pd.read_csv('match_new.csv')
def livem():

            
    index_r=[]
    k=1
    index_live=[]
    match_name=[]
   
    print("------------Current ODI matches----------\n")
    for i in range(len(w)):
        for j in range(len(live_matches)):
            if live_matches[j].get('type')=='ODI':
                ven=live_matches[j].get('venue_location')
                venue=ven.split(",")
                if (w[i][1]==live_matches[j].get('team1').get('name') or w[i][2]==live_matches[j].get('team1').get('name')) and (w[i][0]==venue[0]):
                    if live_matches[j].get('mchstate')=='preview' or live_matches[j].get('mchstate')=='inprogress' or live_matches[j].get('mchstate')=='toss': 
                        print(k,".",live_matches[j].get('team1').get('name'),"vs",live_matches[j].get('team2').get('name'),"at",live_matches[j].get('venue_location'),"on",live_matches[j].get('start_time')) 
                        index_r.append(i)
                        index_live.append(j)
                        k+=1
                        str1=live_matches[j].get('team1').get('name')+" vs "+live_matches[j].get('team2').get('name')
                        match_name.append(str1)
    
    if len(index_r)>0:
        btnl.destroy()
        vart=[]
        lbl_i=tkinter.Label(window,text="Select any of the Given Matches\n to get the prediction",fg="purple")
        lbl_i.grid(column=0,row=29)
        for i in range(len(index_r)):
            var="check"+str(i)
            var=tkinter.IntVar()
            vart.append(var)
            cb = tkinter.Checkbutton(window,text=match_name[i],variable=var,anchor ="w",  onvalue = 1, offvalue = 0, height=1, width = 40)
            cb.grid(row=i+30,column=0)
        
        def prints():
            
            cnt=0
            for i in range(len(index_r)):
                xt=vart[i].get()
                if xt==1:
                    cnt+=1
                    index=i
            if cnt==1:
                players(index)

                    
        btn_lv=tkinter.Button(window,text="Next",command=prints,bg="blue")
        btn_lv.grid(column=0,row=30+i+1)
        
    else:
        print("No ongoing matches")
        label_no=tkinter.Label(window,text="No Ongoing or Upcoming Matches",fg="red")
        label_no.grid(column=1,row=32)
#-----------------------------------------------------------------------------
def players(index):
    index=index_r[index]

    squad='https://www.cricbuzz.com/cricket-match/live-scores'
    response=requests.get(squad)
    soup=BeautifulSoup(response.content,'html.parser')
    m=len(soup.find_all('a',class_="text-hvr-underline text-bold"))
    for i in range(m):
        vs=(soup.find_all('a',class_="text-hvr-underline text-bold")[i].get_text())
        tm=vs.split(" vs ")
        if tm[0]==w[index][1] or tm[0]==w[index][2]:
            lv_link=(soup.find_all('a',class_="text-hvr-underline text-bold")[i].get('href'))
            break
    
    lve=lv_link.split("/",2)
    lv_link=lve[2]

    http="https://www.cricbuzz.com/live-cricket-scorecard/"
    lve_link=http+lv_link
    response=requests.get(lve_link)
    soup=BeautifulSoup(response.content,'html.parser')
    check=len(soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm"))
    team_a=[]
    team_b=[]
    if check>1:
        name_a=((soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm")[1].get_text()))
        name_ac=name_a.split(" Playing XI  ")
        name_a=name_ac[1]
        name_ac=name_a.split(", ")
        name_b=((soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm")[3].get_text()))
        name_bc=name_b.split(" Playing XI  ")
        name_b=name_bc[1]
        name_bc=name_b.split(", ")
        name_ac[10]=name_ac[10][0:-2]
        name_bc[10]=name_bc[10][0:-2]
        m=len(soup.find_all('a',class_="margin0 text-black text-hvr-underline"))
        j=0
        k=0
        name_a=[]
        name_b=[]
        for i in range(m):
            
            if name_ac[j]==(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[i].get_text()):
                z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[i].get_text())
                name_a.append(z)
                z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[i].get('href'))
                team_a.append(z)
                j+=1
            if j==11:
                break
            
        for i in range(m):
            if name_bc[k]==(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[i].get_text()):
                z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[i].get_text())
                name_b.append(z)
                z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[i].get('href'))
                team_b.append(z)
                k+=1
            if k==11:
                break
            
        
    else:
        print("\ncouldn't fetch playing xi profile link")

    
    if len(name_ac)<11 or len(name_bc)<11:
        print("\nPlaying XI not available at the moment, using 15 squad for prediction\n")
        response=requests.get(lve_link)
        soup=BeautifulSoup(response.content,'html.parser')
        check=len(soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm"))
        team_as=[]
        team_bs=[]
        if check>1:
            name_as=((soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm")[1].get_text()))
            name_acs=name_as.split(",")
            name_bs=((soup.find_all('div',class_="cb-col cb-col-100 cb-minfo-tm-nm")[2].get_text()))
            name_bcs=name_bs.split(",")
            m=len(soup.find_all('a',class_="margin0 text-black text-hvr-underline"))
            j=0
            k=0
            name_as=[]
            name_bs=[]
            for i in range(m):
                var1=name_acs[j]
                var1=var1.split(" ",1)
                var2=name_bcs[k]
                var2=var2.split(" ",1)
                for kti in range(m):
                    if var1[1]==(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[kti].get_text()):
                        z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[kti].get_text())
                        name_as.append(z)
                        z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[kti].get('href'))
                        team_as.append(z)
                        j+=1
                    if var2[1]==(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[kti].get_text()):
                        z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[kti].get_text())
                        name_bs.append(z)
                        z=(soup.find_all('a',class_="margin0 text-black text-hvr-underline")[kti].get('href'))
                        team_bs.append(z)
                        k+=1
            bat=[]
            bowl=[]
            for p in range(len(team_as)):
                var=fixed+team_as[p]
                response=requests.get(var)
                soup=BeautifulSoup(response.content,'html.parser')
                td=len(soup.find_all('td'))
                ch=0
                for i in range(td):
                    if (soup.find_all('td')[i].get_text())=='ODI':
                        if ch==0:
                            temp=[]
                            for j in range(i+1,i+14):
                                z=(soup.find_all('td')[j].get_text())
                                temp.append(z)
                            temp.insert(0,name_as[p])
                            bat.append(temp)
                        if ch==1:
                            temp=[]
                            for j in range(i+1,i+13):
                                z=(soup.find_all('td')[j].get_text())
                                temp.append(z)
                            temp.insert(0,name_as[p])
                            bowl.append(temp)
                        ch=1
            team_a_bat=pd.DataFrame(bat)
            team_a_bowl=pd.DataFrame(bowl)
            team_a_bat.columns=['Player','M','Inn','NO','Runs','HS','Avg','BF','SR','100','200','50','4s','6s']
            team_a_bowl.columns=['Player','M','Inn','B','Runs','Wkts','BBI','BBM','Econ','Avg','SR','5W','10W']
            time.sleep(1)
            order=0
            if tm[0]==w[index][1]:
                print(w[index][1],"Players")
                order=1
            else:
                print(w[index][2],"Players")
            bat=[]
            bowl=[]
            for p in range(len(team_bs)):
                var=fixed+team_bs[p]
                response=requests.get(var)
                soup=BeautifulSoup(response.content,'html.parser')
                td=len(soup.find_all('td'))
                ch=0
                for i in range(td):
                    if (soup.find_all('td')[i].get_text())=='ODI':
                        if ch==0:
                            temp=[]
                            for j in range(i+1,i+14):
                                z=(soup.find_all('td')[j].get_text())
                                temp.append(z)
                            temp.insert(0,name_bs[p])
                            bat.append(temp)
                        if ch==1:
                            temp=[]
                            for j in range(i+1,i+13):
                                z=(soup.find_all('td')[j].get_text())
                                temp.append(z)
                            temp.insert(0,name_bs[p])
                            bowl.append(temp)
                        ch=1
            team_b_bat=pd.DataFrame(bat)
            team_b_bowl=pd.DataFrame(bowl)
            team_b_bat.columns=['Player','M','Inn','NO','Runs','HS','Avg','BF','SR','100','200','50','4s','6s']
            team_b_bowl.columns=['Player','M','Inn','B','Runs','Wkts','BBI','BBM','Econ','Avg','SR','5W','10W']
            time.sleep(1)
            if order==1:
                print(w[index][2],"Players")
            else:
                print(w[index][1],"Players")
        else:
            print("couldn't fetch 15 squad profile link")
        
#------------------ fetching playing xi squad ------------------------
                
    else:
        print("using playing xi squad data")
        bat=[]
        bowl=[]
        for p in range(len(team_a)):
            var=fixed+team_a[p]
            response=requests.get(var)
            soup=BeautifulSoup(response.content,'html.parser')
            td=len(soup.find_all('td'))
            ch=0
            for i in range(td):
                if (soup.find_all('td')[i].get_text())=='ODI':
                    if ch==0:
                        temp=[]
                        for j in range(i+1,i+14):
                            z=(soup.find_all('td')[j].get_text())
                            temp.append(z)
                        temp.insert(0,name_a[p])
                        bat.append(temp)
                    if ch==1:
                        temp=[]
                        for j in range(i+1,i+13):
                            z=(soup.find_all('td')[j].get_text())
                            temp.append(z)
                        temp.insert(0,name_a[p])
                        bowl.append(temp)
                    ch=1
        team_a_bat=pd.DataFrame(bat)
        team_a_bowl=pd.DataFrame(bowl)
        team_a_bat.columns=['Player','M','Inn','NO','Runs','HS','Avg','BF','SR','100','200','50','4s','6s']
        team_a_bowl.columns=['Player','M','Inn','B','Runs','Wkts','BBI','BBM','Econ','Avg','SR','5W','10W']
        time.sleep(1)
        order=0
        if tm[0]==w[index][1]:
            print(w[index][1],"Players")
            order=1
        else:
            print(w[index][2],"Players")
        
        bat=[]
        bowl=[]
        for p in range(len(team_b)):
            var=fixed+team_b[p]
            response=requests.get(var)
            soup=BeautifulSoup(response.content,'html.parser')
            td=len(soup.find_all('td'))
            ch=0
            for i in range(td):
                if (soup.find_all('td')[i].get_text())=='ODI':
                    if ch==0:
                        temp=[]
                        for j in range(i+1,i+14):
                            z=(soup.find_all('td')[j].get_text())
                            temp.append(z)
                        temp.insert(0,name_b[p])
                        bat.append(temp)
                    if ch==1:
                        temp=[]
                        for j in range(i+1,i+13):
                            z=(soup.find_all('td')[j].get_text())
                            temp.append(z)
                        temp.insert(0,name_b[p])
                        bowl.append(temp)
                    ch=1
        team_b_bat=pd.DataFrame(bat)
        team_b_bowl=pd.DataFrame(bowl)
        team_b_bat.columns=['Player','M','Inn','NO','Runs','HS','Avg','BF','SR','100','200','50','4s','6s']
        team_b_bowl.columns=['Player','M','Inn','B','Runs','Wkts','BBI','BBM','Econ','Avg','SR','5W','10W']
        time.sleep(1)
        if order==1:
            print(w[index][2],"Players")
        else:
            print(w[index][1],"Players")
    
    team_b_bowl=team_b_bowl.replace(to_replace="-",value=0)
    team_a_bowl=team_a_bowl.replace(to_replace="-",value=0)
    team_b_bat=team_b_bat.replace(to_replace="-",value=0)
    team_a_bat=team_a_bat.replace(to_replace="-",value=0)
    
    ts_file=["ind","pak","aus","bdesh","eng","afg","sl","nz","sa","wi"]
    seq_name=["Afghanistan","Australia","Bangladesh","England","India","New Zealand","Pakistan","South Africa","Sri Lanka","West Indies"]
    
    if w[index][1]<w[index][2]:
        at=w[index][1]
    else:
        bt=w[index][2]
    for pla in range(len(t_name)):
        for plas in range(pla+1,len(t_name)):
            if (t_name[pla]==w[index][1] and t_name[plas]==w[index][2]) or (t_name[pla]==w[index][2] and t_name[plas]==w[index][1]):
                at=ts_file[pla]
                bt=ts_file[plas]
    player=at+"_"+bt+"_score.csv"
    pdat=pd.read_csv(player)
    a_bat=0
    for sco in range(len(team_a_bat)):
        hain=0
        if float(team_a_bat.iloc[sco,2])>=10:
            f1=math.sqrt(float(team_a_bat.iloc[sco,2])/float(team_a_bat.iloc[sco,1]))
            f2=float(team_a_bat.iloc[sco,6])
            f3=float(team_a_bat.iloc[sco,4])
            f4=float(team_a_bat.iloc[sco,9])*100+ 200*float(team_a_bat.iloc[sco,10])+50*float(team_a_bat.iloc[sco,11])
            f5=float(team_a_bat.iloc[sco,5])
            if f4==0:
                fac=f5
            else:
                fac=f4
            f6=float(team_a_bat.iloc[sco,8])
            fsc=f1*(0.6*(f2/(f3/fac))+0.4*f6)
            if fsc>25:
                for ipk in range(len(pdat)):
                    if pdat.iloc[ipk,0]==team_a_bat.iloc[sco,0]:
                        const=10
                        if pdat.iloc[ipk,1]!=0:
                            a_bat+=fsc+(pdat.iloc[ipk,1])/(const*pdat.iloc[ipk,2])
                            hain=1
                        else:
                            a_bat+=fsc
                            hain=1
                if hain==0:
                    a_bat+=fsc
    b_bat=0
    for sco in range(len(team_b_bat)):
        hain=0
        if float(team_b_bat.iloc[sco,2])>=10:
            f1=math.sqrt(float(team_b_bat.iloc[sco,2])/float(team_b_bat.iloc[sco,1]))
            f2=float(team_b_bat.iloc[sco,6])
            f3=float(team_b_bat.iloc[sco,4])
            f4=float(team_b_bat.iloc[sco,9])*100+ 200*float(team_b_bat.iloc[sco,10])+50*float(team_b_bat.iloc[sco,11])
            f5=float(team_b_bat.iloc[sco,5])
            if f4==0:
                fac=f5
            else:
                fac=f4
            f6=float(team_b_bat.iloc[sco,8])
            fsc=f1*(0.6*(f2/(f3/fac))+0.4*f6)
            if fsc>25:
                for ipk in range(len(pdat)):
                    if pdat.iloc[ipk,0]==team_b_bat.iloc[sco,0]:
                        const=10
                        if pdat.iloc[ipk,1]!=0:
                            b_bat+=fsc+(pdat.iloc[ipk,1])/(const*pdat.iloc[ipk,2])
                            hain=1
                        else:
                            b_bat+=fsc
                            hain=1
                if hain==0:
                    b_bat+=fsc
                
    a_bowl=0
    for sco in range(len(team_a_bowl)):
        if float(team_a_bowl.iloc[sco,2])>=10:
            f1=math.sqrt(float(team_a_bowl.iloc[sco,2])/float(team_a_bowl.iloc[sco,1]))
            f2=float(team_a_bowl.iloc[sco,9])+float(team_a_bowl.iloc[sco,10])
            f3=float(team_a_bowl.iloc[sco,11])
            f4=float(team_a_bowl.iloc[sco,8])
            f5=float(team_a_bowl.iloc[sco,2])
            fsc=f1*((100-(f2)+((10*f3)/f5))/f4)
            if fsc>8:
                a_bowl+=fsc
    b_bowl=0
    for sco in range(len(team_b_bowl)):
        if float(team_b_bowl.iloc[sco,2])>=10:
            f1=math.sqrt(float(team_b_bowl.iloc[sco,2])/float(team_b_bowl.iloc[sco,1]))
            f2=float(team_b_bowl.iloc[sco,9])+float(team_b_bowl.iloc[sco,10])
            f3=float(team_b_bowl.iloc[sco,11])
            f4=float(team_b_bowl.iloc[sco,8])
            f5=float(team_b_bowl.iloc[sco,2])
            fsc=f1*((100-(f2)+((10*f3)/f5))/f4)
            if fsc>8:
                b_bowl+=fsc
    if w[index][1]==tm[0]:
        if w[index][1]>w[index][2]:
            temp=a_bat
            a_bat=b_bat
            b_bat=temp
            temp=a_bowl
            a_bowl=b_bowl
            b_bowl=temp
    else:
        if w[index][2]>w[index][1]:
            temp=a_bat
            a_bat=b_bat
            b_bat=temp
            temp=a_bowl
            a_bowl=b_bowl
            b_bowl=temp
            
    dataset = pd.read_csv('match_new.csv')
    new=pd.DataFrame({"a":[w[index][1]],
                      "b":[w[index][2]],
                      "winner":['win'],
                      "location":[w[index][0]],
                      "date":['date'],
                      "a_bat":[a_bat],
                      "a_bowl":[a_bowl],
                      "b_bat":[b_bat],
                      "b_bowl":[b_bowl]})
    
    dataset=dataset.append(new,ignore_index=True)
    
    
    xt=dataset.iloc[:,[0,1,3,5,6,7,8]].values
    yt=dataset.iloc[:,[2]].values
        


    from sklearn.preprocessing import LabelEncoder
    labelencoder_y=LabelEncoder()
    yt=labelencoder_y.fit_transform(yt)

    import category_encoders as ce
    ohe = ce.OneHotEncoder(handle_unknown='ignore', use_cat_names=True)
    xt= ohe.fit_transform(xt)

    
    
    x_train=xt.iloc[:-1,:]
    x_test=xt.iloc[-1:,:]
    y_train=yt[:-1]
    y_test=yt[-1:]
    


    from sklearn.preprocessing import StandardScaler
    sc_x=StandardScaler()
    x_train=sc_x.fit_transform(x_train)
    x_test=sc_x.transform(x_test)


    from sklearn.linear_model import LogisticRegression
    classifier=LogisticRegression(multi_class='ovr',solver='liblinear')
    classifier.fit(x_train,y_train)
    y_pred2=classifier.predict(x_test)
    
    lbl_head=tkinter.Label(window,text="Prediction",font=10)
    lbl_head.grid(column=1,row=33)
    lbl_win=tkinter.Label(window,text="",fg="brown",font=10)
    lbl_win.grid(column=1,row=34)
    for seq in range(len(seq_name)):
        if w[index][1]==seq_name[seq]:
            seq_a=seq
        if w[index][2]==seq_name[seq]:
            seq_b=seq
    if y_pred2==seq_a:
        lbl_win.configure(text=w[index][1])
    if y_pred2==seq_b:
        lbl_win.configure(text=w[index][2])
       
            
lbl_live=tkinter.Label(window,text="Upcoming Matches",bg="cyan",font=10,anchor="w")
lbl_live.grid(column=1,row=27)
btnl=tkinter.Button(window,text="View List",command=livem)
btnl.grid(row=28,column=0)
window.mainloop()