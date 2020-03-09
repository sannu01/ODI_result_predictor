import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
from pycricbuzz import Cricbuzz
import datetime
import numpy as np
import math
import csv


#-----------------------------Updating match details---------------------
    
first='http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id='
last=';type=year'


t_name=["India","Pakistan","Australia","Bangladesh","England","Afghanistan","Sri Lanka","New Zealand","South Africa","West Indies"]
ts_file=["ind","pak","aus","bdesh","eng","afg","sl","nz","sa","wi"]
date=datetime.datetime.now()
y1=date.year
y2=date.year
w=[]

for k in range(y1-1,y2+1):
    print("for year",k)
    year=str(k)
    url=first+year+last
    while (1):
        response=requests.get(url)
        if response.status_code==200:
            break
        else:
            print("couldn't fetch website\n")
        
    soup =BeautifulSoup(response.content,'html.parser')

    x=len(soup.find_all('td'))

    y=int(x/7)
    print("total match:",y)
    i=0
    t=y
    for p in range(t):
        v=[]
        for j in range(7):
            z=(soup.find_all('td')[i].get_text())
            v.append(z)
            i+=1
        w.append(v)
        
for j in w:
    del j[6]
    del j[3]

d_all=pd.DataFrame(w)
d_all.columns=['a','b','winner','location','date']

fixed='https://www.cricbuzz.com'
q1=(d_all.a=="India") | (d_all.a=="Pakistan") | (d_all.a=="Australia") | (d_all.a=="Bangladesh") | (d_all.a=="England") | (d_all.a=="Afghanistan") | (d_all.a=="Sri Lanka") | (d_all.a=="New Zealand") | (d_all.a=="South Africa") | (d_all.a=="West Indies")
q2=(d_all.b=="India") | (d_all.b=="Pakistan") | (d_all.b=="Australia") | (d_all.b=="Bangladesh") | (d_all.b=="England") | (d_all.b=="Afghanistan") | (d_all.b=="Sri Lanka") | (d_all.b=="New Zealand") | (d_all.b=="South Africa") | (d_all.b=="West Indies")
query=q1 & q2
matches=d_all[query]
q1=(d_all.winner=="India") | (d_all.winner=="Pakistan") | (d_all.winner=="Australia") | (d_all.winner=="Bangladesh") | (d_all.winner=="England") | (d_all.winner=="Afghanistan") | (d_all.winner=="Sri Lanka") | (d_all.winner=="New Zealand") | (d_all.winner=="South Africa") | (d_all.winner=="West Indies")
matches=matches[q1]

data_m=pd.read_csv('match_new.csv')

print("updating match details")

for tem in range(len(t_name)):
    for jt in range(tem+1,len(t_name)):
        
        q1=(matches.a==t_name[tem]) | (matches.a==t_name[jt])
        q2=(matches.b==t_name[tem]) | (matches.b==t_name[jt])
        query=q1 & q2
        data_team=matches[query]
        q1=(data_team.winner==t_name[tem]) | (data_team.winner==t_name[jt])
        data_team=data_team[q1]
        nup=0
        for ite in range(len(data_team)):
            for ste in range(len(data_team)):
                update=0
                for sjte in range(len(data_m)-1,len(data_m)-300,-1):
                    if data_m.iloc[sjte,2]==data_team.iloc[ste,2] and data_m.iloc[sjte,3]==data_team.iloc[ste,3] and data_m.iloc[sjte,4]==data_team.iloc[ste,4]:
                        update=1
                        break
                if data_team.iloc[ste,2]=='-':
                    update=1
            if update==0:
                first='http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id='
                last=';type=year'
                yt=data_team.iloc[ite,4]
                yy=yt.split(", ")
                xy=(yy[1])
                year=xy
                url=first+year+last
                while (1):
                    response=requests.get(url)
                    if response.status_code==200:
                        break
                    else:
                        print("couldn't fetch website")
                        
                soup =BeautifulSoup(response.content,'html.parser')
                x=len(soup.find_all('td'))
                y=int(x/7)
                print("----year:-----",year)
                i=0
                t=y
                test=0
                for p in range(t):
                    v=[]
                    case=0
                    for j in range(7):
                        if (soup.find_all('td')[i].get_text())==data_team.iloc[ite,3]:
                            print(soup.find_all('td')[i].get_text())
                            it=i
                            if (soup.find_all('td')[it+1].get_text())==data_team.iloc[ite,4]:
                                z=(soup.find_all('td')[it+2].get_text())
                                print(soup.find_all('td')[it+1].get_text())
                                zx=len(soup.find_all('a',class_='data-link'))
                                for px in range(zx):
                                    if z==(soup.find_all('a',class_='data-link')[px].get_text()):
                                        link=(soup.find_all('a',class_='data-link')[px].get('href'))
                                        case=1
                                        test=1
                                        break
                        i+=1
                        if case==1:
                            break
                    if case==1:
                        break
                if test==1:
                    urlse='http://stats.espncricinfo.com'
                    lur=urlse+link
                    while (1):
                        response=requests.get(lur)
                        if response.status_code==200:
                            break
                        else:
                            print("couldn't fetch website\n")
                    soup =BeautifulSoup(response.content,'html.parser')
                    k=len(soup.find_all('div',class_='cell batsmen'))
                    a=[]
                    b=[]
                    c=0
                    team_a=(soup.find_all('span',class_='cscore_name cscore_name--long')[0].get_text())
                    team_b=u=(soup.find_all('span',class_='cscore_name cscore_name--long')[1].get_text())
                    if team_a<team_b:
                        at=team_a
                        bt=team_b
                    else:
                        at=team_b
                        bt=team_a
                    
                    while 1:
                        if at==t_name[0]:
                            at='ind'
                            break
                        if at==t_name[1]:
                            at='pak'
                            break
                        if at==t_name[2]:
                            at='aus'
                            break
                        if at==t_name[3]:
                            at='bdesh'
                            break
                        if at==t_name[4]:
                            at='eng'
                            break
                        if at==t_name[5]:
                            at='afg'
                            break
                        if at==t_name[6]:
                            at='sl'
                            break
                        if at==t_name[7]:
                            at='nz'
                            break
                        if at==t_name[8]:
                            at='sa'
                            break
                        if at==t_name[9]:
                            at='wi'
                            break
                    while 1:
                        if bt==t_name[0]:
                            bt='ind'
                            break
                        if bt==t_name[1]:
                            bt='pak'
                            break
                        if bt==t_name[2]:
                            bt='aus'
                            break
                        if bt==t_name[3]:
                            bt='bdesh'
                            break
                        if bt==t_name[4]:
                            bt='eng'
                            break
                        if bt==t_name[5]:
                            bt='afg'
                            break
                        if bt==t_name[6]:
                            bt='sl'
                            break
                        if bt==t_name[7]:
                            bt='nz'
                            break
                        if bt==t_name[8]:
                            bt='sa'
                            break
                        if bt==t_name[9]:
                            bt='wi'
                            break
                        
                    for i in range(k):
                        z=soup.find_all('div',class_='cell batsmen')[i].get_text()
                        p=z.split(" (c)")
                    
                        if p[0]=="BATSMEN" and i==0:
                            c=1
                        if p[0]=="BATSMEN" and i>0:
                            c=2
                        if p[0]!="BATSMEN":
                            xyz=p[0]
                            if xyz[-2]==" ":
                                ty=xyz[0:-2]
                            else:
                                ty=p[0]
                            if team_a<team_b:
                                if c==1:
                                    a.append(ty)
                                if c==2:
                                    b.append(ty)
                            else:
                                if c==1:
                                    b.append(ty)
                                if c==2:
                                    a.append(ty)
                    
                    if team_a<team_b:
                        if len(a)<11:
                            indi=2
                            z=soup.find_all('div',class_='wrap dnb')[0].get_text()
                            p=z.split("Did not bat: ")
                            k=11-len(a)
                            if k>1:
                                z=p[1].split(", ")
                            else:
                                z=p[1]
                            for i in range(k):
                                if k>1:
                                    p=z[i].split(" (c)")
                                else:
                                    p=z.split(" (c)")
                                xyz=p[0]
                                if xyz[-2]==" ":
                                    ty=xyz[0:-2]
                                else:
                                    ty=p[0]
                                a.append(ty)
                        else:
                            indi=1
            
                        if len(b)<11:
                            z=soup.find_all('div',class_='wrap dnb')[indi].get_text()
                            p=z.split("Did not bat: ")
                            k=11-len(b)
                            if k>1:
                                z=p[1].split(", ")
                            else:
                                z=p[1]
                            for i in range(k):
                            
                                if k>1:
                                    p=z[i].split(" (c)")
                                else:
                                    p=z.split(" (c)")
                                xyz=p[0]
                                if xyz[-2]==" ":
                                    ty=xyz[0:-2]
                                else:
                                    ty=p[0]
                                b.append(ty)
                    else:
                        if len(b)<11:
                            indi=2
                            z=soup.find_all('div',class_='wrap dnb')[0].get_text()
                            p=z.split("Did not bat: ")
                            k=11-len(b)
                            if k>1:
                                z=p[1].split(", ")
                            else:
                                z=p[1]
                            for i in range(k):
                                if k>1:
                                    p=z[i].split(" (c)")
                                else:
                                    p=z.split(" (c)")
                                xyz=p[0]
                                if xyz[-2]==" ":
                                    ty=xyz[0:-2]
                                else:
                                    ty=p[0]
                                b.append(ty)
                        else:
                            indi=1
            
                        if len(a)<11:
                            z=soup.find_all('div',class_='wrap dnb')[indi].get_text()
                            p=z.split("Did not bat: ")
                            k=11-len(a)
                            if k>1:
                                z=p[1].split(", ")
                            else:
                                z=p[1]
                            for i in range(k):
                                if k>1:
                                    p=z[i].split(" (c)")
                                else:
                                    p=z.split(" (c)")
                                xyz=p[0]
                                if xyz[-2]==" ":
                                    ty=xyz[0:-2]
                                else:
                                    ty=p[0]
                                a.append(ty)
                    file_a=ts_file[tem]
                    file_b=ts_file[jt]
                    player=file_a+'_'+file_b+'_score.csv'
                    
                    first='http://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=2;id='
                    last=';type=year'
                    yt=data_team.iloc[ite-1,4]
                    yy=yt.split(", ")
                    xy=(yy[1])
                    year1=xy
                    url=first+year1+last
                    while (1):
                        response=requests.get(url)
                        if response.status_code==200:
                            break
                        else:
                            print("couldn't fetch website\n")
                    
                    soup =BeautifulSoup(response.content,'html.parser')
                    x=len(soup.find_all('td'))
                    y=int(x/7)
                    print("         ----year:-----",year1)
                    i=0
                    t=y
                    test=0
                    for p in range(t):
                        v=[]
                        case=0
                        for j in range(7):
                            if (soup.find_all('td')[i].get_text())==data_team.iloc[ite-1,3]:
                                print("         ",soup.find_all('td')[i].get_text())
                                it=i
                                if (soup.find_all('td')[it+1].get_text())==data_team.iloc[ite-1,4]:
                                    z=(soup.find_all('td')[it+2].get_text())
                                    print("       ",soup.find_all('td')[it+1].get_text())
                                    zx=len(soup.find_all('a',class_='data-link'))
                                    for px in range(zx):
                                        if z==(soup.find_all('a',class_='data-link')[px].get_text()):
                                            link=(soup.find_all('a',class_='data-link')[px].get('href'))
                                            case=1
                                            test=1
                                            break
                            i+=1
                            if case==1:
                                break
                        if case==1:
                            break
                    if test==1:
                        urlse='http://stats.espncricinfo.com'
                        lur=urlse+link
                        while (1):
                            response=requests.get(lur)
                            if response.status_code==200:
                                break
                            else:
                                print("couldn't fetch website\n")
                    
                        
                        soup =BeautifulSoup(response.content,'html.parser')
                        k=len(soup.find_all('div',class_='cell batsmen'))
                        az=[]
                        bz=[]
                        c=0
                        team_a=(soup.find_all('span',class_='cscore_name cscore_name--long')[0].get_text())
                        team_b=u=(soup.find_all('span',class_='cscore_name cscore_name--long')[1].get_text())
                        for i in range(k):
                            z=soup.find_all('div',class_='cell batsmen')[i].get_text()
                            p=z.split(" (c)")
                            if p[0]=="BATSMEN" and i==0:
                                c=1
                            if p[0]=="BATSMEN" and i>0:
                                c=2
                            if p[0]!="BATSMEN":   
                                    xyz=p[0]
                                    if xyz[-2]==" ":
                                        ty=xyz[0:-2]
                                    else:
                                        ty=p[0]
                                    if c==1:
                                        az.append(ty)
                                    if c==2:
                                        bz.append(ty)

                        for ist in range(10):
                            z=soup.find_all('div',class_='cell runs')[ist].get_text()
                            if z.isdigit()==True:
                                break
                           
                        diff=ist
                        ast=[]
                        bst=[]
                        for i in range(len(az)):
                            z=soup.find_all('div',class_='cell runs')[ist].get_text()
                            ast.append(z)
                            ist+=diff
                        diff=-1
                        for istn in range(ist,ist+10):
                            z=soup.find_all('div',class_='cell runs')[istn].get_text()
                            diff+=1
                            if z.isdigit()==True:
                                break
                        ist=istn
                        for i in range(len(bz)):
                            z=soup.find_all('div',class_='cell runs')[ist].get_text()
                            bst.append(z)
                            ist+=diff
                    
                
                        pdat=pd.read_csv(player)
                        f = open(player, "w")
                        f.truncate()
                        f.close()
                        f=open(player,"a",newline="")
                        with f:
                            writer=csv.writer(f)
                            writer.writerows([['name','score','freq']])
                    
                        for i in range(len(az)):
                            hain=0
                            if ast[i]!=' - ':
                                for ipk in range(len(pdat)):
                                    if az[i]==pdat.iloc[ipk,0]:
                                        pcp=float(pdat.iloc[ipk,1])
                                        tcp=float(ast[i])
                                        scp=pcp+tcp
                                    
                                        myfile=open(player,"a",newline="")
                                        with myfile:
                                            writer=csv.writer(myfile)
                                            writer.writerows([[az[i],scp,float(pdat.iloc[ipk,2])+1]])
                                        hain=1
                                if hain==0:
                                    myfile=open(player,"a",newline="")
                                    with myfile:
                                        writer=csv.writer(myfile)
                                        writer.writerows([[az[i],float(ast[i]),1]])
                                    
                        for i in range(len(bz)):
                            hain=0
                            if bst[i]!=' - ':
                                for ipk in range(len(pdat)):
                                    if bz[i]==pdat.iloc[ipk,0]:
                                        scp=float(pdat.iloc[ipk,1])+float(bst[i])
                                    
                                        myfile=open(player,"a",newline="")
                                        with myfile:
                                            writer=csv.writer(myfile)
                                            writer.writerows([[bz[i],scp,float(pdat.iloc[ipk,2])+1]])
                                        hain=1
                                if hain==0:
                                    myfile=open(player,"a",newline="")
                                    with myfile:
                                        writer=csv.writer(myfile)
                                        writer.writerows([[bz[i],float(bst[i]),1]])
                        for ipk in range(len(pdat)):
                           hain=0
                           for i in range(len(az)):
                               if pdat.iloc[ipk,0]==az[i]:
                                   hain=1
                           for i in range(len(bz)):
                               if pdat.iloc[ipk,0]==bz[i]:
                                   hain=1
                           if hain==0:
                                 myfile=open(player,"a",newline="")
                                 with myfile:
                                     writer=csv.writer(myfile)
                                     writer.writerows([[pdat.iloc[ipk,0],float(pdat.iloc[ipk,1]),float(pdat.iloc[ipk,2])]])
                                 myfile.close()
                    pdat=pd.read_csv(player)      
                                
                    s="_bat_"
                    x=".csv"
                    w=at+s+x
                    data=pd.read_csv(w)
                    a_bat=0
                    for i in a:
                        hain=0
                        for j in range(len(data)):
                            if data.iloc[j,0]==i:
                                if data.iloc[j,1]>25:
                                    for ipk in range(len(pdat)):
                                        if pdat.iloc[ipk,0]==data.iloc[j,0]:
                                            const=10
                                            if pdat.iloc[ipk,1]!=0:
                                                a_bat+=data.iloc[j,1]+(pdat.iloc[ipk,1])/(const*pdat.iloc[ipk,2])
                                                hain=1
                                            else:
                                                a_bat+=data.iloc[j,1]
                                                hain=1
                                    if hain==0:
                                        a_bat+=data.iloc[j,1]
                                    
                    
                    s="_bat_"
                    w=bt+s+x
                    b_bat=0
                    data=pd.read_csv(w)
                    for i in b:
                        hain=0
                        for j in range(len(data)):
                            if data.iloc[j,0]==i:
                                if data.iloc[j,1]>25:
                                    for ipk in range(len(pdat)):
                                        if pdat.iloc[ipk,0]==data.iloc[j,0]:
                                            const=10
                                            if pdat.iloc[ipk,1]!=0:
                                                b_bat+=data.iloc[j,1]+(pdat.iloc[ipk,1])/(const*pdat.iloc[ipk,2])
                                                hain=1
                                            else:
                                                b_bat+=data.iloc[j,1]
                                                hain=1
                                    if hain==0:
                                        b_bat+=data.iloc[j,1]
                                
                    
                    s="_bowl_"
                    w=at+s+x
                    a_bowl=0
                    data=pd.read_csv(w)
                    for i in a:
                        for j in range(len(data)):
                            if data.iloc[j,0]==i:
                                if data.iloc[j,1]>8:
                                    a_bowl+=data.iloc[j,1]
                                    
                    s="_bowl_"
                    w=bt+s+x
                    b_bowl=0
                    data=pd.read_csv(w)
                    for i in b:
                        for j in range(len(data)):
                            if data.iloc[j,0]==i:
                                if data.iloc[j,1]>8:
                                    b_bowl+=data.iloc[j,1]
                
                
                
                    myfile=open("match_new.csv","a",newline="")
                    with myfile:
                        writer=csv.writer(myfile)
                        writer.writerows([[data_team.iloc[ite,0],data_team.iloc[ite,1],data_team.iloc[ite,2],data_team.iloc[ite,3],data_team.iloc[ite,4],a_bat,a_bowl,b_bat,b_bowl]])
                

#--------------------updating player details----------------------------
print("updating player details")                  
first='http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=start;orderbyad=reverse;size=200;spanmax1=31+dec+'
second=';spanmin1=1+jan+1996;spanval1=span;team='
last=';template=results;type=batting'
index=[1,2,3,4,5,6,7,8,25,40]
date=datetime.datetime.now()
y1=date.year
for cont in range(len(index)):
    
    for ib in range(y1,y1+1):
        dcount=0
        mid=str(ib)
        tid=str(index[cont])
        burl=first+mid+second+tid+last;
        while 1:
            response=requests.get(burl)
            if response.status_code==200:
                break
            else:
                print("couldn't fetch website")
        soup =BeautifulSoup(response.content,'html.parser')

        x=len(soup.find_all('td'))
    
        cb=0
        for rb in range(50):
            if soup.find_all('td')[rb].get_text()=='':
                cb+=1
                if cb==1:
                    fc=rb
                if cb==2:
                    sc=rb
                
        print("--------",ib,"---------")
        rb=sc-fc
        cb=(x-10)//rb
        
        cb-=1
        i=10
        for k in range(cb):
            vb=[]
            proceed=1
            if k==0:
                for j in range(rb):
                    zb=soup.find_all('th')[j].get_text()
                    vb.append(zb)
                    score='Score'
                    till=ib
            else:
                
                for j in range(rb):
                    if j==1:
                        zb=soup.find_all('td')[i].get_text()
                        sx=zb.split('-')
                        till=sx[1]
                    zb=soup.find_all('td')[i].get_text()
                    sx=zb.split('*')
                    vb.append(sx[0])

                    i+=1
                
                if vb[2]=='-':
                    vb[2]=0
                if vb[3]=='-':
                    vb[3]=0
                if vb[5]=='-':
                    vb[5]=0
                if vb[6]=='-':
                    vb[6]=0
                if vb[7]=='-':
                    vb[7]=0
                if vb[9]=='-':
                    vb[9]=0
                if vb[10]=='-':
                    vb[10]=0
                if vb[11]=='-':
                    vb[11]=0
        
                if float(vb[3])<10:
                    score=0
                
                else:
                
                    v1=math.sqrt(float(vb[3])/float(vb[2]))
            
                    run6_4=100*float(vb[10])+50*float(vb[11])
                    runs=float(vb[5])
                    hs=float(vb[6])
                    if run6_4==0:
                        v2=runs/hs
                    else:
                        v2=runs/run6_4
        
                    v3=float(vb[7])/v2
                    v4=float(vb[9])
            
                    score=v1*(0.6*v3+0.4*v4)
                        
                if k!=0:
                    if float(vb[3])<10:
                        proceed=0

            if float(till)>ib-1 and proceed==1:
                
                
                while 1:
                    
                    if index[cont]==1:
                        country='eng'
                        break
                    if index[cont]==2:
                        country='aus'
                        break
                    if index[cont]==3:
                        country='sa'
                        break
                    if index[cont]==4:
                        country='wi'
                        break
                    if index[cont]==5:
                        country='nz'
                        break
                    if index[cont]==6:
                        country='ind'
                        break
                    if index[cont]==7:
                        country='pak'
                        break
                    if index[cont]==8:
                        country='sl'
                        break
                    if index[cont]==25:
                        country='bdesh'
                        break
                    if index[cont]==40:
                        country='afg'
                        break
        
                an='_bat_'
                en='.csv'
                name=country+an+en
    
                if k==0:
                    f = open(name, "w")
                    f.truncate()
                    f.close()
                
                myfile=open(name,"a",newline="")
                with myfile:
                    writer=csv.writer(myfile)
                    writer.writerows([[vb[0],score,vb[1],vb[2],vb[3],vb[4],vb[5],vb[6],vb[7],vb[8],vb[9],vb[10],vb[11],vb[12]]])


first='http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=start;orderbyad=reverse;size=200;spanmax1=31+dec+'
second=';spanmin1=1+jan+1996;spanval1=span;team='
last=';template=results;type=bowling'
date=datetime.datetime.now()
y1=date.year
for cont in range(len(index)):
    for ib in range(y1,y1+1):
        dcount=0
        mid=str(ib)
        tid=str(index[cont])
        burl=first+mid+second+tid+last;
        while 1:
            response=requests.get(burl)
            if response.status_code==200:
                break
            else:
                print("couldn't fetch website")
        soup =BeautifulSoup(response.content,'html.parser')

        x=len(soup.find_all('td'))
    
        cb=0
        for rb in range(50):
            if soup.find_all('td')[rb].get_text()=='':
                cb+=1
                if cb==1:
                    fc=rb
                if cb==2:
                    sc=rb
                
        print("--------",ib,"---------")
        rb=sc-fc
        cb=(x-10)//rb
        
        cb-=1
        i=10
        for k in range(cb):
            vb=[]
            proceed=1
            if k==0:
                for j in range(rb):
                    zb=soup.find_all('th')[j].get_text()
                    vb.append(zb)
                    score='Score'
                    till=ib
            else:
                
                for j in range(rb):
                    
                    if j==1:
                        zb=soup.find_all('td')[i].get_text()
                        sx=zb.split('-')
                        till=sx[1]
                    zb=soup.find_all('td')[i].get_text()
                    sx=zb.split('*')
                    vb.append(sx[0])

                    i+=1
                    
                if vb[2]=='-':
                    vb[2]=0
                if vb[3]=='-':
                    vb[3]=0
                if vb[9]=='-':
                    vb[9]=0
                if vb[10]=='-':
                    vb[10]=0
                if vb[11]=='-':
                    vb[11]=0
                if vb[13]=='-':
                    vb[13]=0
        
                if float(vb[3])<10:
                    score=0
                
                else:
                
                    v1=math.sqrt(float(vb[3])/float(vb[2]))
                
                    v2=100-(float(vb[9])+float(vb[11])/6)+(10*float(vb[13]))/float(vb[3])
                    v3=float(vb[10])
            
                    score=v1*(v2/v3)
            
                if k!=0:
                    if float(vb[3])<10:
                        proceed=0
            if float(till)>ib-1 and proceed==1:
                
                
                while 1:
                
                    if index[cont]==1:
                        country='eng'
                        break
                    if index[cont]==2:
                        country='aus'
                        break
                    if index[cont]==3:
                        country='sa'
                        break
                    if index[cont]==4:
                        country='wi'
                        break
                    if index[cont]==5:
                        country='nz'
                        break
                    if index[cont]==6:
                        country='ind'
                        break
                    if index[cont]==7:
                        country='pak'
                        break
                    if index[cont]==8:
                        country='sl'
                        break
                    if index[cont]==25:
                        country='bdesh'
                        break
                    if index[cont]==40:
                        country='afg'
                        break
        
                an='_bowl_'
                en='.csv'
                name=country+an+en
                
                if k==0:
                    f = open(name, "w")
                    f.truncate()
                    f.close()
        
                myfile=open(name,"a",newline="")
                with myfile:
                    writer=csv.writer(myfile)
                    writer.writerows([[vb[0],score,vb[1],vb[2],vb[3],vb[4],vb[5],vb[6],vb[7],vb[8],vb[9],vb[10],vb[11],vb[12],vb[13]]])
