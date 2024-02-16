import csv

softwares = ['Mysql','Nginx','Lighttpd','Redis','Httpd','Mapreduce','HDFS']

blackwords = ['file', 'path', 'port', 'address', 'version', 'legacy', 'host', 'ui','admin','login','dir','scheduler','mod','id','debug','log','names']




def nameparse(softwarename):
    csvfile = open(f'{softwarename}/{softwarename}Config.csv','r')
    reader = csv.reader(csvfile)

    csvfile = open(f'ManualPerConf/{softwarename}PerConfig.csv','w')
    writer = csv.writer(csvfile)
    i=1
    for line in reader:
        flag=0
        for word in blackwords:
            if line[0].find(word)!=-1:
                flag = 1
                break
        if(flag==0):
            print(str(i)+' '+line[0])
            i=i+1
            writer.writerow([line[0]])

    csvfile.close()

if __name__ == '__main__':
    for softwarename in softwares:
        nameparse(softwarename)
