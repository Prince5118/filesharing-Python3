from crontab import CronTab

my_cron = CronTab(user='root')
job = my_cron.new(command=' /root/pjlogin/fus-3/fus/script.py >> ~/pjlogin/fus-3/fus/deletingfolders.txt 2>&1',comment='Deleting Folders')
job.minute.every(5)

my_cron.write()

