import os
myCmd = os.popen('grep -iw "Booting" /var/log/messages.?').read()
print(myCmd)