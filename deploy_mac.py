import sys
import os

def main():
    appId = 'zouber-bookmark'
    appVersion = '1'

    # Only one input argument
    if len(sys.argv) <= 1:
        print "No appId detected, use default appId: sambardeer-tech"
        print "No appVersion detected, use default appVersion: zouber"
    # two input arguments
    elif len(sys.argv) == 2:
        arg1 = sys.argv[1]
        try:
            appVersion = int(arg1)
        except:
            appId = arg1
    # three input arguments
    else:
        appId = sys.argv[1]
        appVersion = sys.argv[2]

    print "using appId: %s, appVersion: %s" % (appId, appVersion)
        

    # Update Main System
    # for macbook air environment
    #cmd = r'python "C:\Program Files (x86)\Google\google_appengine\appcfg.py"'
    cmd = r'appcfg.py'
    # for normal environment
    #cmd = r'"C:\Program Files (x86)\Google\google_appengine\appcfg.py"'
    #cmd = r'"appcfg.py"'
    os.system(cmd + " --oauth2 update . " + " -A %s -e zouber129@gmail.com -V %s --passin"% (appId, appVersion))


if __name__ == "__main__":
    main()