import numpy as np
import math
import numpy.polynomial.legendre as lgd
import matplotlib.pyplot as plt
from file_system import *


class corr_3d(object):
      def __init__(self,survey_name, ang_interv = 100, radial_interv = 31,Type = 'uniform',Njob=20, k0=1,order = 0):
          self.Njob = Njob
          self.Type = Type
          self.name = survey_name
          self.radial_binsize = 8
          self.ang_interv = ang_interv
          self.radial_interv = radial_interv
          self.k0 = k0
          self.order = order
          dirs = surveyname(self.name, self.Type)
          func_name = 'dirs.'+self.name
          func = eval(func_name)
          func()
          self.survey_name = survey(dirs)
          self._filename_gen()
   
      def _filename_gen(self):
          filenameDD=[]
          filenameDR=[]
          filenameRR=[]
          topdir = self.survey_name.binhist_topdir
          for i in range(0,self.Njob):
             for j in range(i,self.Njob): 
                 filenameDD.append(topdir + '/D'+str(i)+'D'+str(j)+'.dat')
          for i in range(0,self.Njob):
              for j in range(0,self.Njob): 
                  filenameDR.append(topdir + '/D'+str(i)+'R'+str(j)+'.dat') 
          for i in range(0,self.Njob):
              for j in range(i,self.Njob):
                  filenameRR.append(topdir + '/R'+str(i)+'R'+str(j)+'.dat') 
          self.filenameDD = filenameDD
          self.filenameDR = filenameDR
          self.filenameRR = filenameRR

      def JKnife_CorrFunc(self,Jacknife=-1):
          """
          load files from filenames, set data to 0 in JK cutted regions
          """
          FilelistDD = []
          FilelistRR = []
          FilelistDR = []
          COUNT = 0
          for i in range(0,self.Njob):
              for j in range(i,self.Njob):
                  if i!=Jacknife and j!=Jacknife : 
                       FilelistDD.append(np.loadtxt(self.filenameDD[COUNT]))
                  else:
                       FilelistDD.append(np.zeros_like(np.loadtxt(self.filenameDD[COUNT])))
                  COUNT+=1
          COUNT = 0
          for i in range(0,self.Njob):
              for j in range(0,self.Njob):
                  if i!=Jacknife and j!=Jacknife:
                      FilelistDR.append(np.loadtxt(self.filenameDR[COUNT]))
                  else:
                      FilelistDR.append(np.zeros_like(np.loadtxt(self.filenameDR[COUNT])))
                  COUNT+=1
          COUNT = 0
          for i in range(0,self.Njob): 
              for j in range(i,self.Njob):
                  if i!=Jacknife and j!=Jacknife :
                     FilelistRR.append(np.loadtxt(self.filenameRR[COUNT]))
                  else:
                     FilelistRR.append(np.zeros_like(np.loadtxt(self.filenameRR[COUNT])))
                  COUNT+=1
          DD_total=np.zeros_like(np.loadtxt(self.filenameDD[0]))
          DR_total=np.zeros_like(np.loadtxt(self.filenameDR[0]))
          RR_total=np.zeros_like(np.loadtxt(self.filenameRR[0]))
          for i in range(0,int((self.Njob+1)*self.Njob/2)):
              DD_total+=FilelistDD[i]
              RR_total+=FilelistRR[i]
          for i in range(0,self.Njob*self.Njob):
               DR_total+=FilelistDR[i]
          topdir = self.survey_name.binhist_topdir
          TotalPoints=np.loadtxt(topdir+'/TotalPoints.txt')
          DD_total_num=0;DR_total_num=0;RR_total_num=0  
          for i in range(0,len(TotalPoints)):
                if TotalPoints[i][3]!=Jacknife and TotalPoints[i][4]!=Jacknife :
                    DD_total_num+=TotalPoints[i][0]
                    DR_total_num+=TotalPoints[i][1] 
                    RR_total_num+=TotalPoints[i][2]
          print('DD_total_num='+str(DD_total_num)+' DR_total_num='+str(DR_total_num)+' RR_total_num='+str(RR_total_num))
          Final_total=np.zeros_like(np.loadtxt(self.filenameDD[0]))
          assert(len(Final_total)==self.radial_interv)
          assert(len(Final_total[0])==self.ang_interv)
          #import pdb;pdb.set_trace()
          Final_total=(DD_total/DD_total_num - 2*DR_total/DR_total_num + RR_total/RR_total_num)/(RR_total/RR_total_num)
          #import pdb;pdb.set_trace()
          return Final_total

      def CorrFunc(self):
          """
          correlation function
          """
          Final_total = self.JKnife_CorrFunc(-1)
          d=[0]*len(Final_total[0])
          d[self.order]+=1 
          b=[0]*len(Final_total)
          #import pdb;pdb.set_trace()
          for i in range(0,len(Final_total)):
               for j in range(0,len(Final_total[0])): 
                   b[i]=b[i]+0.01*Final_total[i][j]*lgd.legval(j*0.01,d)
               if self.order==0:
                   b[i]=(2*self.order+1)*b[i]
               else:
                   b[i]=(2*self.order+1)*b[i]/2.
          c=[(i+0.5)*self.radial_binsize for i in range(0,len(Final_total))]
          #import pdb;pdb.set_trace()
          bxx=np.array(b)
          for i in range (0,len(Final_total)): 
               b[i]=b[i]*c[i]*c[i]
          print(bxx)
          Jacknife_list = []
          CorrFun_Err_temp = [0]*len(Final_total)
          CorrFun_Err = [0]*len(Final_total)
          for i in range(0,self.Njob):
              Jacknife_list.append(self.JKnife_CorrFunc(i))
          for k in range(0,self.Njob):
              for i in range(0,len(Final_total)):
                   for j in range(0,len(Final_total[0])): 
                       CorrFun_Err_temp[i]+=0.01*Jacknife_list[k][i][j]*lgd.legval(j*0.01,d)
                   if self.order==0:
                       CorrFun_Err_temp[i] = (2*self.order+1)*CorrFun_Err_temp[i]
                   else:
                       CorrFun_Err_temp[i] = (2*self.order+1)*CorrFun_Err_temp[i]/2.
                   CorrFun_Err_temp[i]=c[i]*c[i]*CorrFun_Err_temp[i]
                   CorrFun_Err[i]+=(CorrFun_Err_temp[i]-b[i])*(CorrFun_Err_temp[i]-b[i])
                   CorrFun_Err_temp[i]=0 
          dat2 = np.loadtxt('./data/xi0gebossELG_NGC4_mz0.6xz1.1fkp8st0.dat').transpose()
          plt.plot(dat2[0],dat2[1]*dat2[0]*dat2[0]) 
          for i in range (0,len(Final_total)):
               CorrFun_Err[i]=math.sqrt(CorrFun_Err[i]*(self.Njob-1)/self.Njob)
          plt.errorbar(c,b,yerr=CorrFun_Err,fmt='-o') 
          if self.order!=0:
              self.survey_name.corr_output = self.survey_name.corr_output.replace('.out','_order%d.out'%self.order)
          f = open(self.survey_name.corr_output,"w")
          #import pdb;pdb.set_trace()
          for i in range(0,len(c)):
             f.write(str(c[i])+' '+str(bxx[i])+' '+str(CorrFun_Err[i])+'\n') 
          print('output saved to %s'%self.survey_name.corr_output)
          f.close()
          plt.xlabel('Mpc',size=16)
          plt.show() 
          return True
      def CorrFunc_no_errorbar(self):
          print('start')
          Final_total = self.JKnife_CorrFunc(-1)
          d=[0]*len(Final_total[0])
          d[self.order]+=1
          b=[0]*len(Final_total)
          for i in range(0,len(Final_total)):
               for j in range(0,len(Final_total[0])):
                   b[i]=b[i]+0.01*Final_total[i][j]*lgd.legval(j*0.01,d)
               if self.order==0:
                   b[i]=(2*self.order+1)*b[i]
               else:
                   b[i]=(2*self.order+1)*b[i]/2.
          c = [(i+0.5)*self.radial_binsize for i in range(0,len(Final_total))]
          f = open(self.survey_name.corr_output.replace('.out','_order%d.out'%self.order),"w")
          print(self.survey_name.corr_output.replace('.out','_order%d.out'%self.order))
          for i in range(0,len(c)):
              f.write(str(c[i])+' '+str(b[i])+'\n')
          f.close()
          print('end')

name = 'elg_ngc_run_conbimed_uniform'

corr = corr_3d(survey_name=name,order=0)
corr.CorrFunc_no_errorbar() 
corr = corr_3d(survey_name=name,order=2)
corr.CorrFunc_no_errorbar() 
'''
corr = corr_3d(survey_name=name,order=4)
corr.CorrFunc_no_errorbar()
'''
