import os
import time
#import keyboard #root ...
from pynput import keyboard
from prompt_toolkit import prompt #23-2-2026 - previous values etc.
# import cmds_ext #below --> #cmds_ext.py
"""
#cmds_ext.py
#18-4-2026, 23:30 - extend the list dynamically etc. - import before call ...
cmds_add = ["sudo ssh user@192.168.123.11,printenv","cat /proc/meminfo"]
cmds_win_str = "echo %PATH%"
cmds_win = cmds_win_str.split(',') #check if there are cmds with , - no?
print(cmds_win)
"""
# log-cmd.txt ...
#import getpass
#prompt("What is your name: ", default=f"{getpass.getuser()}")

# Author: Todor Arnaudov - Tosh/Twenkid
# The Sacred Computer: Thinking Machines, Creativity and Human Development: AGI & Transhumanism Pioneer since the year 2000
# https://github.com/twenkid
# Linux Cmd utility, Command Tools, Cmds ... Quick access to commands etc. Jan 2026+
# Part of Vsy/Вседържец/Allmighty

"""
#python - input - how to add default values for the user to edit
#google
#reddit ...
#prompt_toolit
...


#single keys, no enter

import asyncio

from prompt_toolkit.input import create_input
from prompt_toolkit.keys import Keys

async def main() -> None:
    done = asyncio.Event()
    input = create_input()

    def keys_ready():
        for key_press in input.read_keys():
            print(key_press)

            if key_press.key == Keys.ControlC:
                done.set()

    with input.raw_mode():
        with input.attach(keys_ready):
            await done.wait()
"""            
            

def on_press(key):
    try:
        print(f'Key pressed: {key.char}')
    except AttributeError:
        print(f'Special key pressed: {key}')
    return False  # Stop listener after first key

def a_key():
  print("Press key...")
  with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    
#import cv2
#from cv2 import waitKey

# pip3 install keyboard 
#def hotkey_callback():
#    print("Space was pressed!")


#keyboard.add_hotkey('space', hotkey_callback)

# Stops the program when you hit esc
#print("press a key")
#keyboard.wait() #'esc')
#a = keyboard.read_key()  from keyboard, not pynput
#cv2.waitKey but I don't want to use it

#a = cv2.waitKey(0) #0) #9999)
#print(a) #???!

#cmds 30-1-2026

#version: 26-3-2026, 17:06
#cmds4: snapshot ... #10-7-2026
help1 = "mame contra -record timestamp"
p = ["xset dpms - blank screen (mouse, key)", "Irfan View i_view64", "gnome-disks", "Temperature (lmsensors, sensors)","Sound Volume - alsamixer", "htop - performance monitor","NES: fceux", "NES: flatpak run ca._0ldsk00l.Nestopia", "MAME - arcade emulator", "See last records (10.2.2026: contra8) ls /home/idr/.mame/inp", "Enable Wifi", "watch /proc/cpuinfo", "restart xrdp remote desktop - sudo systemctl restart xrdp", "Stop docker: sudo systemctl stop docker", "lsblk && fdisk -l - Check usb drives", "mount usb drive sdb1: mkdir and sudo mount /dev/sdb1 ...", "gnome-control-center - power etc.", "sudo swapon /swapfile ", "sudo swapoff", "du /swapfile -h", "Disk free space: df -h", "python -c ' ... '", "free -h", "cat /proc/sys/vm/swappiness", "sysctl vm.swappiness=30", "sleep 3 && gnome-snapshot" ]

cmds = ["xset dpms force off", "wine /home/idr/.wine/drive_c/Program\ Files/IrfanView/i_view64.exe &", "gnome-disks &", "sensors", "alsamixer", "htop", "fceux", "flatpak run ca._0ldsk00l.Nestopia &", "mame", "ls /home/idr/.mame/inp", "nmcli radio wifi on", 'watch -n 2 "grep MHz /proc/cpuinfo"', 'sudo systemctl restart xrdp', 'sudo systemctl stop docker', "lsblk && fdisk -l", "sudo mkdir -p /media/usb && sudo mount /dev/sdb1 /media/usb", "gnome-control-center", "sudo swapon /swapfile", "sudo swapoff", "du /swapfile -h", "df -h", "python -c '  '", "free -h", "cat /proc/sys/vm/swappiness", "sudo sysctl vm.swappiness=35", "sleep 3 && gnome-snapshot"]

import cmds_ext
cmds.extend(cmds_ext.cmds_add)
p.extend(cmds_ext.cmds_add)

#mark some to be with prompt_toolkit - editable 
#separate lists! #27-3-2026

#sudo sysctl vm.swappiness=10
#sudo cat /sys/kernel/debug/dri/0/i915_gem_objects
#nvtop -h --gpu-select 

"""
cat /sys/class/drm/card0/device/mem_info_gtt_total
cat /sys/class/drm/card0/device/mem_info_gtt_used

"""

prev_set = set() #{} #23-2-2026

def log1(f,s):
  f.write("\r\n")
  f.write(s)
  f.flush()
  
def help():
  print("*"*40)
  print("HELP")
  #linux cmd monitor blank
  global p
  #p = ["xset dpms - blank screen (mouse, key)", "Irfan View i_view64"]
  #n=0
  print("*"*40)
  for n,i in enumerate(p):
      print(n,i)
  print("="*40)
  a_key()
  #input("Enter ...")

f = open("log-cmd.txt", "at", encoding="UTF-8")
n=0
previous = " "
max_width = 80 #per line ... #cmds3.py, #5-4-2026
new_lines = False

while True:
        print("*"*40)
        n=0
        curpos = 0 # 5-4-2026
        for i,t in zip(cmds,p):
           #print(t)
           #print("-"*50)
           #if (len(i)+curpos<max_width): end = '\t'; curpos+=len(i)+12; print(f"{n}::{i}", end=end)
           if not new_lines:
               if (len(i)+curpos<max_width): end = '\t'; curpos+=len(i)+12; print(f"[{n}]::[{i}]", end=end)           
               else: print(f"[{n}]::[{i}]"); curpos = 0; 
           else:
                print(f"[{n}]::[{i}]"); curpos = 0; 
           #print("-"*50)
           
           n+=1
        if curpos==0: print("#"*60)
        else: print("\n"+"#*"*60)
        print("[c] - Free cmd",end='\t') 
        print("[m] - Mame contra -record contra_timestamp",end='\t')                 
        print("[q] - Quit, end",end='\t')
        print("[h] - Help",end='\t')
        print("[p] - Previous c command",end='\t')
        print("[l] - Select from Previous",end='\t')
        print(f"[n] - toggle new_lines = {new_lines}")        
        b_cancel = False
        b_list = False
        en = input("?")
        if en=='n': new_lines = not new_lines
        if en=="l":        
           #l1 = prev_set.to_list()
           l1 = list(prev_set) #.to_list()
           for n1,t1 in enumerate(l1): #prev_set.to_list()):
             print(f"{n1}: {t1}")
           print("-1: Cancel")
           n2 = input("?")
           if int(n2)==-1: b_cancel = True; b_list = True #False
           print("b_cancel =", b_cancel)
           if not b_cancel:
             #en = l1[int(n2)]                #prev_list
             #cm = l1[int(n2)] #en
             cm = prompt("? ", default=l1[int(n2)] )
             b_list = True
             print("<===========>")
             print(f"{en}, [{cm}], {b_list}")
             print("<===========>")
             
                
        if en=="p":        
            cm = prompt("? ", default=previous)
            #cm = en
            previous = cm
        #        print(en)
        if en=="c" or en=='p' or (en=='l' and not b_cancel): #!!! not elif p - the same!  #24-2-2026
            #print(f"c,p,l,b_cancel = {c},{p},{l},{b_cancel})")
            print(f"en,b_cancel = {en},{b_cancel})")
            if en!='l' and en!='p':
               cm = input("Enter cmd... (q, c, n, 0 to cancel) ")
            if cm == "q" or cm == "c" or cm == "n" or cm == "0" or b_cancel: pass  #en=='l or b_list
            else: #l .. 
                print("            else: #l .. ")	
                #print("pppppppppp")                
                #verify, protect, watchdog etc. #23-2-2-206
                previous = cm
                prev_set.add(cm)
                log1(f, cm)
                os.system(cm) #check, ... guard etc.
                continue #skip en = int(en)
        if en=="q":break
        if en=="m":                 
              from datetime import datetime
              timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #should read files, get last number etc. or remember ...
              cm = f"mame contra -record contra_{timestamp}"
              print(cm)
              log1(f, cm)
              prev_set.add(cm)
              os.system(cm)
              print("^"*50) 
              continue
        if en=="h":help();continue
        try:
          en = int(en)
        except:
          print("Invalid: pass")
          continue
        if en==0: print("monitor off in 2.5 sec!"); time.sleep(2.5) #to prevent mouse movement immediately #7-2-2026  #xset dpms         
        #if en==99:break
        #if en==-1:help()
        print("B_CANCEL?", b_cancel)
        if not b_cancel: 
           log1(f, cmds[en])  
           prev_set.add(cmds[en])
           #b_cancel: 
           os.system(cmds[en])
        else: print("CANCEL")
        print("^"*50)  
        
        #k1 = input("...Enter...")
        a_key() #10-2-2026

f.close()


"""1.Python script which has a timer on every 10 seconds.
2. The function stores the last ticks with time.now
3. Compares the difference = diff
4. A switch/map: when the diff is > thresholds --> calls scripts
5. One of the scripts: nmcli radio enable
(It watches for turning on after suspend)
"""
