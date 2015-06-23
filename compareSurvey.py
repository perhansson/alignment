import sys,string, re





def getVal(sv,i):
    return float(string.replace(sv.split()[i],',',''))

def printcompare(ideal,surv,name):
    f = open(name+'.txt','w')
    for k in sorted(ideal):
        if k in surv:
            v = ideal[k]
            vs = surv[k]
            s = '%20s: %40s ->  %40s (%.4f,%.4f,%.4f)' %(k,v, vs, getVal(v,0)- getVal(vs,0), getVal(v,1)- getVal(vs,1), getVal(v,2)- getVal(vs,2))
            print s
            f.write(s+'\n')
    f.close()




def getSensorFramePos(f):

    res = {}
    for line in f.readlines():
        if ' in ' not in line or 'sensor' in line or 'in mod' not in line or 'mm' not in line:
            continue
        m = re.search('module_L([1-6])([tb])_halfmodule_(\S+)',line)
        if m!=None:
            res[ m.group(1)+m.group(2)+'_'+m.group(3) ] = line.split('[')[1].split(']')[0]
    return  res


def getPinFramePos(f):
    #print 'getpinfr ', len(f.readlines())
    res = {}
    #print 'getpinfr ', len(f.readlines())    
    for line in f.readlines():
        #print line
        #continue
        #if ' in ' not in line or 'sensor' in line or 'in mod' not in line or 'mm' not in line:
        #    continue
        m = re.search('module_L([1-6])([tb]) (.*) base.* \[(.*)\] ',line)
        if m !=None:
            #print m.group(1), ' ', m.group(4)
            res[ m.group(1)+m.group(2) ] = m.group(4)
    return  res



fs = open(sys.argv[1],'r')
fd = open(sys.argv[2],'r')

print fs

sensorFrameSurveyed = getSensorFramePos(fs)    
sensorFrameIdeal = getSensorFramePos(fd)    

#pinFrameSurveyed = getPinFramePos(fs)    
#pinFrameIdeal = getPinFramePos(fd)    

#print pinFrameSurveyed

#print 'hej'
#print pinFrameIdeal


#printcompare(pinFrameIdeal,pinFrameSurveyed,'pinFrameDiff')
printcompare(sensorFrameIdeal,sensorFrameSurveyed,'sensorFrameDiff')

fs.close()
fd.close()
