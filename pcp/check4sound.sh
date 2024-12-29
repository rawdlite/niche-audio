tc@pCP:~$ vim check4sound.sh 
#!/bin/sh
#
export LOG=/var/log/check4sound.log
date > $LOG
echo "check4sound started" >> $LOG
while true
do
  sudo -u tc /home/tc/check4sound.py -v >> $LOG 2>&1
  date >> $LOG
  /bin/sleep 1
done

exit 0
