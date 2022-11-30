import os

dirfiles = os.listdir()
recs = [x for x in dirfiles if x.endswith(".rec")]

files = []

### Løb igennem REC-filer.
for rec in recs:
    filename = rec.split('.')[0]
    files.append(filename + ' csv.csv')

    ### Åbn .rec- og lav/åbn .csv-fil:
    fr = open(filename + '.rec',"r")
    fw = open(filename + ' csv.csv',"w")

    ### Læs .rec-fil:
    lines = fr.readlines()[2:]
    rows = [line for line in lines]

    for line in rows:
        ### Trim data:
        row = line.replace(" [","_[").replace('%','').split()
        # print(row)

        ### Skriv trimmet data til csv-fil:
        for i in row: fw.write(i.replace('_',' ') + ';')
        fw.write('\n')

    ### Luk filer:
    fr.close()
    fw.close()


### Flere REC-filer?
if len(recs) > 1:
    print("- - - - -\nOBS!\nDer er flere REC-filer.\nDer er lavet en CSV-fil for hver REC-fil. Se herunder:\n")
    for f in files: print("\""+f+"\"")
    print("- - - - -")

