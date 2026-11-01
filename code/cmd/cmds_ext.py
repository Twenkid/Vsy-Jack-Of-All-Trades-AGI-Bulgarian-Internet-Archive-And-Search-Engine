#cmds_ext.py
#18-4-2026, 23:30 - dynamically extend the list etc. - import before call ...
cmds_add = ["sudo ssh user@192.168.100.1,printenv","cat /proc/meminfo"]
cmds_win_str = "echo %PATH%"
cmds_win = cmds_win_str.split(',') #check if there are cmds with , - no?
print(cmds_win)

