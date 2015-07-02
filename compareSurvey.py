#!/usr/bin/python

import sys,string, re, subprocess,os, argparse
from ROOT import TCanvas, TGraph


def getArgs():
    parser = argparse.ArgumentParser(description='Survey study')
    parser.add_argument('-f','--files', nargs='+', required=True, help='Input files.')
    parser.add_argument('-p','--position', action='store_true', help='Position analysis.')
    parser.add_argument('-r','--rotation', action='store_true', help='Position analysis.')
    args = parser.parse_args()
    print args
    return args

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


def printCompare(txtfile,name):
    f = open(name+'.txt','w')
    for k in sorted(txt):
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




def plotCompareRotations(rotations,name):
    print rotations
    
    grD = [ TGraph() , TGraph(), TGraph()]
    binLabels = {}
    ix = 0
    for k in sorted(rotations):
        values = rotations[k].replace(',',' ')
        for i in range(len(grD)):
            np = grD[i].GetN()
            grD[i].SetPoint(np,ix,getVal(values,i)*1e3)
        binLabels[ix] = k
        ix = ix + 1
    print binLabels
    c = TCanvas('c','c',10,10,1200,700)
    c.Print(name + '.ps[')
    for i in range(len(grD)):
        c1 = TCanvas('c'+str(i),'c'+str(i),10,10,1200,700)
        c1.SetBottomMargin(0.25)
        c1.SetGridy()
        grD[i].SetTitle(name + ' survey;;' + ' Cardan XYZ in ' + ['x','y','z'][i] + ' (mrad)')
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


def getSensorRot(lines):

    res = {}
    for line in lines:
        m = re.search('module_L([1-6])([tb])_halfmodule_(\S+)_active\sin\smodule_L[1-6][tb]\s.*XYZ\:(.*)', line)
        if m!=None:
            #print line
            res[ m.group(1) + m.group(2) + '_' + m.group(3) ] = m.group(4)
    return  res

def getModuleRot(lines):

    res = {}
    for line in lines:
        m = re.search('module_L([1-6])([tb])\sin\sbase\s.*XYZ\:(.*)', line)
        if m!=None:
            #print line
            res[ m.group(1) + m.group(2) ] = m.group(3)
    return  res

def getChannelRot(lines):

    res = {}
    for line in lines:
        m = re.search('support_(\S+)\sin\sbase\s.*XYZ\:(.*)', line)
        if m!=None:
            #print line
            res[ m.group(1) ] = m.group(2)
    return  res


def getSensorPosGlobal(lines):

    res = {}
    for line in lines:
        m = re.match('^module_L([1-6])([tb])_halfmodule_(\S+)_active\s.*tracking.*\[(.*)\].*mm.*',line)
        if m!=None:
            print line
            res[ m.group(1)+m.group(2)+'_'+m.group(3) ] = m.group(4)
    return  res


def getSensorRotGlobal(lines):

    res = {}
    for line in lines:
        m = re.match('module_L([1-6])([tb])_halfmodule_(\S+)_active\s.*tracking.*XYZ\:(.*)',line)
        #print line
        if m!=None:
            #print line
            res[ m.group(1)+m.group(2)+'_'+m.group(3) ] = m.group(4)
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






def positionCmp(args):

    fs = open(args.files[0],'r')
    fs_lines = fs.readlines()
    fd = open(args.files[1],'r')
    fd_lines = fd.readlines()
    linesSurvey = list(fs_lines)
    linesIdeal = list(fd_lines)

    tag1 = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    tag2 = os.path.splitext(os.path.basename(sys.argv[2]))[0]
    tag = tag1 + '-vs-' + tag2

    sensorSurveyedGlobal = getSensorPosGlobal(linesSurvey)
    sensorIdealGlobal = getSensorPosGlobal(linesIdeal)

    sensorSurveyed = getSensorPos(linesSurvey)    
    sensorIdeal = getSensorPos(linesIdeal)    

    pinSurveyed = getPinPos(linesSurvey)    
    pinIdeal = getPinPos(linesIdeal)    

    channelSurveyed = getUChannelPos(linesSurvey)    
    channelIdeal = getUChannelPos(linesIdeal)    


    printCompare(sensorIdeal,sensorSurveyed,'sensorDiff-'+tag)
    plotCompare(sensorIdeal,sensorSurveyed,'sensorDiff-'+tag)

    printCompare(pinIdeal,pinSurveyed,'pinDiff-'+tag)
    plotCompare(pinIdeal,pinSurveyed,'pinDiff-'+tag)

    printCompare(channelIdeal,channelSurveyed,'channelDiff-'+tag)
    plotCompare(channelIdeal,channelSurveyed,'channelDiff-'+tag)

    printCompare(sensorIdealGlobal,sensorSurveyedGlobal,'sensorDiffGlobal-'+tag)
    plotCompare(sensorIdealGlobal,sensorSurveyedGlobal,'sensorDiffGlobal-'+tag)


    fs.close()
    fd.close()


def rotationCmp(args):

    print 'analyze rotations'
    
    fs = open(args.files[0],'r')
    fs_lines = fs.readlines()

    tag = os.path.splitext(os.path.basename(args.files[0]))[0]


    sensorRotGlobal = getSensorRotGlobal(fs_lines)
    sensorRot = getSensorRot(fs_lines)
    moduleRot = getModuleRot(fs_lines)    
    channelRot = getChannelRot(fs_lines)    
    print sensorRotGlobal
    
    plotCompareRotations(sensorRot,'sensorDiffRot-'+tag)
    plotCompareRotations(moduleRot,'moduleDiffRot-'+tag)
    plotCompareRotations(channelRot,'channelDiffRot-'+tag)
    plotCompareRotations(sensorRotGlobal,'sensorDiffRotGlobal-'+tag)
    
    
    fs.close()


def main():

    args = getArgs()

    if args.position:
        positionCmp(args)

    if args.rotation:
        rotationCmp(args)


if __name__ == '__main__':
    main()
