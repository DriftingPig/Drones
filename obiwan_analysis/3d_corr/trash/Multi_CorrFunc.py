#DD_i.txt,DR_i.txt,RR_i.txt
Sep_interval = 31
import numpy as np
import os
import math
import numpy.polynomial.legendre as lgd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
filename = 'NewData_subfiles'
def JKnife_CorrFunc(Njob, Jacknife=-1,k0=1, order=0,name = filename):
    #    pp = PdfPages('Correlation_Function_of_order_No'+str(order)+'.pdf')
    #    b2=np.loadtxt('xi0isoChallenge_matterpower6.0.dat').transpose()
    #    plt.plot(b2[0],b2[1]*b2[0]*b2[0]*k0)
    filenameDD=[]
    filenameDR=[]
    filenameRR=[]
    for i in range(0,Njob):
        for j in range(i,Njob):
            filenameDD.append(name+'/D'+str(i)+'D'+str(j)+'.dat')
    for i in range(0,Njob):
        for j in range(0,Njob):
                filenameDR.append(name+'/D'+str(i)+'R'+str(j)+'.dat')
    for i in range(0,Njob):
        for j in range(i,Njob):
            filenameRR.append(name+'/R'+str(i)+'R'+str(j)+'.dat')

    FilelistDD = []
    FilelistRR = []
    FilelistDR = []
    COUNT = 0
    void_pair_line = [0]*100 #interval of angular scales
    void_pair = []
    for i in range(0,Sep_interval):
        void_pair.append(void_pair_line)
    for i in range(0,Njob):
        for j in range(i,Njob):
            if i!=Jacknife and j!=Jacknife :
                aDD = np.loadtxt(filenameDD[COUNT])
                FilelistDD.append(aDD)
            else:
                FilelistDD.append(void_pair)
            COUNT+=1
    COUNT = 0
    for i in range(0,Njob):
        for j in range(0,Njob):
            if i!=Jacknife and j!=Jacknife :
                aDR = np.loadtxt(filenameDR[COUNT])
                FilelistDR.append(aDR)
            else:
                FilelistDR.append(void_pair)
            COUNT+=1
    COUNT = 0
    for i in range(0,Njob):
        for j in range(i,Njob):
            if i!=Jacknife and j!=Jacknife :
                aRR = np.loadtxt(filenameRR[COUNT])
                FilelistRR.append(aRR)
            else:
                FilelistRR.append(void_pair)
            COUNT+=1
    DD_total=[]
    DR_total=[]
    RR_total=[]
    for i in range(0,len(aDD[0])):
             DD_total.append([0]*len(aDD.transpose()))
             DR_total.append([0]*len(aDD.transpose()))
             RR_total.append([0]*len(aDD.transpose()))
    for i in range(0,int((Njob+1)*Njob/2)):
        for j in range(0,len(aDD)):
            for k in range(0,len(aDD.transpose())):
                DD_total[j][k]+=FilelistDD[i][j][k]
    for i in range(0,Njob*Njob):
        for j in range(0,len(aDD)):
            for k in range(0,len(aDD.transpose())):
                DR_total[j][k]+=FilelistDR[i][j][k]
    for i in range(0,int(Njob*(Njob+1)/2)):
        for j in range(0,len(aDD)):
            for k in range(0,len(aDD.transpose())):
                RR_total[j][k]+=FilelistRR[i][j][k]
    import pdb;pdb.set_trace()
    TotalPoints=np.loadtxt(name+'/TotalPoints.txt')
    DD_total_num=0
    DR_total_num=0
    RR_total_num=0
    #import pdb
    #pdb.set_trace()
    for i in range(0,len(TotalPoints)):
        if TotalPoints[i][3]!=Jacknife and TotalPoints[i][4]!=Jacknife :
             DD_total_num+=TotalPoints[i][0]
             DR_total_num+=TotalPoints[i][1]
             RR_total_num+=TotalPoints[i][2]
             #print(RR_total_num)
    print('DD_total_num='+str(DD_total_num)+' DR_total_num='+str(DR_total_num)+' RR_total_num='+str(RR_total_num))
    Final_total=[]
    for i in range(0,len(aDD)):
         Final_total.append([0]*(len(aDD.transpose())))
    #print str(Final_total[0][0])
    for i in range(0,len(aDD)):
        for j in range(0,len(aDD.transpose())):
             Final_total[i][j] = ((DD_total[i][j]/DD_total_num)-(DR_total[i][j]/DR_total_num)*2+(RR_total[i][j]/RR_total_num))/((RR_total[i][j]/RR_total_num))
    import pdb;pdb.set_trace()
    return Final_total

def CorrFunc(Njob,k0=1, order=0,name_corr = filename):
    Final_total = []
    Final_total = JKnife_CorrFunc(Njob,-1,k0,order,name = name_corr)
    d=[0]*len(Final_total[0])
    d[order]+=1
    b=[0]*len(Final_total)
    for i in range(0,len(Final_total)):
         for j in range(0,len(Final_total[0])):
                 b[i]=b[i]+0.01*Final_total[i][j]*lgd.legval(Final_total[i][j],d)
         b[i]=(2*order+1)*b[i]
    c=[(i+0.5)*8 for i in range(0,len(Final_total))]
    for i in range (0,len(Final_total)):
        b[i]=b[i]*c[i]*c[i]


    Jacknife_list = []
    for i in range(0,Njob):
        Jacknife_list.append(JKnife_CorrFunc(Njob,i,k0,order,name = name_corr))
    CorrFun_Err_temp = [0]*len(Final_total)
    CorrFun_Err = [0]*len(Final_total)
    for k in range(0,Njob):
        for i in range(0,len(Final_total)):
            for j in range(0,len(Final_total[0])):
                CorrFun_Err_temp[i]+=0.01*Jacknife_list[k][i][j]*lgd.legval(Jacknife_list[k][i][j],d)
            CorrFun_Err_temp[i] = (2*order+1)*CorrFun_Err_temp[i]
            CorrFun_Err_temp[i]=c[i]*c[i]*CorrFun_Err_temp[i]
            CorrFun_Err[i]+=(CorrFun_Err_temp[i]-b[i])*(CorrFun_Err_temp[i]-b[i])
            CorrFun_Err_temp[i]=0
    dat2 = np.loadtxt('./data/xi0gebossELG_NGC4_mz0.6xz1.1fkp8st0.dat').transpose()
    plt.plot(dat2[0],dat2[1]*dat2[0]*dat2[0])
    for i in range (0,len(Final_total)):
        CorrFun_Err[i]=math.sqrt(CorrFun_Err[i]*(Njob-1)/Njob)
    plt.errorbar(c,b,yerr=CorrFun_Err,fmt='-o')
    import pdb;pdb.set_trace()
    f = open('./data/'+os.path.basename(name_corr)+'.txt','w')
    for i in range(0,len(c)):
        f.write(str(c[i])+' '+str(b[i])+' '+str(CorrFun_Err[i])+'\n')
    f.close()
    plt.xlabel('Mpc',size=16)
    plt.show()
    return True
    
def CorrFunc_Add(Njob=20,k0=1, order=0):
    b2=np.loadtxt('xi0isoChallenge_matterpower6.0.dat').transpose()
    plt.plot(b2[0],b2[1]*b2[0]*b2[0]*k0)
    plt.xlabel('Mpc',size=16)
    CorrFunc(Njob,name_corr = 'NewData_subfiles_chunk21')
    CorrFunc(Njob,name_corr = 'NewData_subfiles_chunk22')
    CorrFunc(Njob,name_corr = 'NewData_subfiles_chunk23')
    plt.show()     

def CorrFunc_ALL_sub(index,Njob=20,k0=1,order=0):
    Final_total = []
    Final_total = JKnife_CorrFunc(Njob,index,k0,order)
    d=[0]*len(Final_total[0])
    d[order]+=1
    b=[0]*len(Final_total)
    for i in range(0,len(Final_total)): 
        for j in range(0,len(Final_total[0])):
             b[i]=b[i]+0.01*Final_total[i][j]*lgd.legval(Final_total[i][j],d)
        b[i]=(2*order+1)*b[i]
    c=[(i+0.5)*5 for i in range(0,len(Final_total))]
    for i in range (0,len(Final_total)):
        b[i]=b[i]*c[i]*c[i]
    plt.plot(c,b)
    return True

def CorrFunc_ALL(Njob=20):
    for i in range(0,20):
        CorrFunc_ALL_sub(i,Njob)
    plt.show()
    return True

def JKnife_show(index):
    import sys
    CorrFunc_ALL_sub(index)
    plt.show()
    print('continue?')
    sys.stdin.readline()
    plt.clf()
    return True

def weighed_tot(k0=1):
    chunk21 = np.loadtxt('./data/NewData_subfiles_chunk21.txt').transpose()
    chunk22 = np.loadtxt('./data/NewData_subfiles_chunk22.txt').transpose()
    chunk23 = np.loadtxt('./data/NewData_subfiles_chunk23.txt').transpose()
    chunk_tot = [0]*len(chunk21[0])
    chunk_err_tot = [0]*len(chunk21[0])
    for i in range(0,len(chunk_tot)):
        chunk_tot[i]+=chunk21[1][i]/chunk21[2][i]**(2)
        chunk_tot[i]+=chunk22[1][i]/chunk22[2][i]**(2)
        chunk_tot[i]+=chunk23[1][i]/chunk23[2][i]**(2)
        chunk_tot[i]=chunk_tot[i]/(chunk21[2][i]**(-2)+chunk22[2][i]**(-2)+chunk23[2][i]**(-2))
        chunk_err_tot[i] = (chunk21[2][i]**(-2)+chunk22[2][i]**(-2)+chunk23[2][i]**(-2))**(-0.5)
    #p21 = plt.errorbar(chunk21[0],chunk21[1],yerr=chunk21[2],fmt='-o')
    #p22 = plt.errorbar(chunk22[0],chunk22[1],yerr=chunk22[2],fmt='-o')
    #p23 = plt.errorbar(chunk23[0],chunk23[1],yerr=chunk23[2],fmt='-o')
    ptot = plt.errorbar(chunk21[0],chunk_tot,yerr=chunk_err_tot,fmt='-o')
    b2 = np.loadtxt('xi0isoChallenge_matterpower6.0.dat').transpose()
    ptheory = plt.plot(b2[0],b2[1]*b2[0]*b2[0]*k0)
    #plt.legend((p21, p22,p23,ptot,ptheory), ('chunk21', 'chunk22','chunk23','total','theory'))
    plt.show()


CorrFunc(20,name_corr='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/obiwan_corr/3d/elg_clustering_chunk23/BinHist/uniform/')
