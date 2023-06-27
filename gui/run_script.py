import subprocess
import sys
import PySimpleGUI as sg
import progress




def runCommand(cmd, timeout=None, window=None):  
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)    
    output = ''
    progress.run()
    print("Result are as follows."+"\n")
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)

    return (retval, output)                         # also return the output just for fun

