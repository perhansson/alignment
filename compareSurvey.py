#!/usr/bin/python

import sys,string, re, subprocess
from ROOT import TCanvas, TGraph




def getVal(sv,i):
    return float(string.replace(sv.split()[i],',',''))

def printCompare(ideal,surv,name):
    f = open(name+'.txt','w')
    for k in sorted(ideal):
        if k in surv:
            v = ideal[k]
            vs = surv[k]
            s = '%20s: %40s ->  %40s (%.4f,%.4f,%.4f)' %(k,v, vs, getVal(v,0)- getVal(vs,0), getVal(v,1)- getVal(vs,1), getVal(v,2)- getVal(vs,2))
            print s
            f.write(s+'\n')
    f.close()

def plotCompare(ideal,surv,name):
    grD = [ TGraph() , TGraph(), TGraph()]
    binLabels = {}
    ix = 0
    for k in sorted(ideal):
        if k in surv:
            v = ideal[k]
            vs = surv[k]
            delta = [ getVal(v,0)- getVal(vs,0), getVal(v,1)- getVal(vs,1), getVal(v,2)- getVal(vs,2) ]            
            for i in range(len(grD)):
                np = grD[i].GetN()
                grD[i].SetPoint(np,ix,delta[i])
            binLabels[ix] = k
            ix = ix + 1
    print binLabels
    c = TCanvas('c','c',10,10,1200,700)
    c.Print(name + '.ps[')
    for i in range(len(grD)):
        c1 = TCanvas('c'+str(i),'c'+str(i),10,10,1200,700)
        c1.SetBottomMargin(0.25)
        c1.SetGridy()
        grD[i].SetTitle(name + ' survey;;' + ' Ideal-Surveyed in ' + ['x','y','z'][i] + ' (mm)')
        grD[i].SetMarkerSize(1.0)
        grD[i].SetMarkerStyle(20)
        h = grD[i].GetHistogram()
        for k,v in binLabels.iteritems():
            b = h.FindBin(k)
            h.GetXaxis().SetBinLabel(b, v)
        grD[i].Draw('ALP')
        #cans.append(c)
        c1.Print(name + '.ps')
    c.Print(name + '.ps]')
    status = subprocess.call('ps2pdf ' + name + '.ps',shell=True)
    ans = raw_input('continue?')





def getSensorPos(lines):

    res = {}
    for line in lines:
        if ' in ' not in line or 'sensor' in line or 'in mod' not in line or 'mm' not in line:
            continue
        m = re.search('module_L([1-6])([tb])_halfmodule_(\S+)',line)
        if m!=None:
            print line
            res[ m.group(1)+m.group(2)+'_'+m.group(3) ] = line.split('[')[1].split(']')[0]
    return  res


def getPinPos(lines):
    res = {}
    for line in lines:
        m = re.search('module_L([1-6])([tb]) (.*) base.* \[(.*)\] ',line)
        if m !=None:
            res[ m.group(1)+m.group(2) ] = m.group(4)
    return  res

def getUChannelPos(lines):
    res = {}
    for line in lines:
        #print line
        m = re.search('^support_([a-z]+)_(L\d+)\s.*base.*\[(.*)\].*mm.*',line)
        if m !=None:
            res[ 'U-ch ' + m.group(1)+m.group(2) ] = m.group(3)
    return  res



fs = open(sys.argv[1],'r')
fs_lines = fs.readlines()
fd = open(sys.argv[2],'r')
fd_lines = fd.readlines()
linesSurvey = list(fs_lines)
linesIdeal = list(fd_lines)




sensorSurveyed = getSensorPos(linesSurvey)    
sensorIdeal = getSensorPos(linesIdeal)    

pinSurveyed = getPinPos(linesSurvey)    
pinIdeal = getPinPos(linesIdeal)    

channelSurveyed = getUChannelPos(linesSurvey)    
channelIdeal = getUChannelPos(linesIdeal)    

printCompare(sensorIdeal,sensorSurveyed,'sensorDiff')
plotCompare(sensorIdeal,sensorSurveyed,'sensorDiff')

printCompare(pinIdeal,pinSurveyed,'pinDiff')
plotCompare(pinIdeal,pinSurveyed,'pinDiff')

printCompare(channelIdeal,channelSurveyed,'channelDiff')
plotCompare(channelIdeal,channelSurveyed,'channelDiff')


fs.close()
fd.close()
