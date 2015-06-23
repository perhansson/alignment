import sys,string



class survey:
    def __init__(self,desc):
        self.desc = desc
    def add(self,words):
        self.origin = words[:3]
        self.x = words[3:6]
        self.y = words[6:9]
        self.z = words[9:12]
    def getxml(self):
        s = '<SurveyVolume name="" desc=\"' + self.desc + '\">\n'
        s += '\t<origin x=\"' + self.origin[0] + '\" y=\"' + self.origin[1] + '\" z=\"' + self.origin[2] + '\"/>\n'
        s += '\t<unitvec name=\"X\" x=\"' + self.x[0] + '\" y=\"' + self.x[1] + '\" z=\"' + self.x[2] + '\"/>\n'
        s += '\t<unitvec name=\"Y\" x=\"' + self.y[0] + '\" y=\"' + self.y[1] + '\" z=\"' + self.y[2] + '\"/>\n'
        s += '\t<unitvec name=\"Z\" x=\"' + self.z[0] + '\" y=\"' + self.z[1] + '\" z=\"' + self.z[2] + '\"/>\n'
        s += '</SurveyVolume>\n'
        return s

        

def clean(s):
    s = string.replace(s,'\n','')
    s = string.replace(s,' ','')
    s = string.replace(s,'[','')
    s = string.replace(s,']','')
    s = string.replace(s,'(','')
    s = string.replace(s,')','')
    s = string.replace(s,'array','')
    s = string.replace(s,',','')
    return s

f = open(sys.argv[1],'r')

active=False
desc = ''
v = []
sur = None
iline = 0
lines = f.readlines()
for line in lines:

    
    if active and not 'frame' in line:
        l = line.split()
        for w in l:
           w = clean(w)
           #print w
           if w!='':
               v.append(w)
        #print v
    if 'frame' in line or iline==(len(lines)-1):
        if sur != None:
            sur.add(v)
            v= []
            print sur.getxml()
        active=True
        desc = line.split('\n')[0]
        sur = survey(desc)
        #print desc
    iline = iline + 1

f.close()
