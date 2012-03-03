import csv
import sys
import MySQLdb as mdb

mysql_user = 'root'
mysql_pass = 'root'

try:
    con = mdb.connect(host='127.0.0.1', port=3306, user=mysql_user,
            passwd=mysql_pass)

    with con:
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS fountains")
        cur.execute("USE fountains")
        cur.execute("DROP TABLE IF EXISTS fountain")
        cur.execute("CREATE TABLE IF NOT EXISTS \
                fountain(ID INT PRIMARY KEY AUTO_INCREMENT, \
                Latitude float, Longitude float, Location VARCHAR(200),\
                Maintainer VARCHAR(25), Status VARCHAR(25))\
                ")


        cur.execute("SELECT VERSION()")
        cur.execute("DELETE FROM fountain")
        csvfile = open('data.csv', 'rb')
        reader = csv.DictReader(csvfile)
        for row in reader:
            Latitude = row['Latitude']
            Longitude = row['Longitude']
            label, Location = row['Location'].split(':')
            Maintainer = row['Maintainer']
            Status = row['Status']

            if(Latitude == None or Longitude == None or Location == None
                    or Maintainer == None or Status == None):
                continue

            cur.execute("INSERT INTO fountain(Latitude,Longitude,\
                    Location,Maintainer,Status) VALUES(%s, %s, %s, %s, %s)",
                    (Latitude, Longitude, Location, Maintainer, Status))

        cur.execute("SELECT * FROM fountain")

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    if con:
        con.close()

