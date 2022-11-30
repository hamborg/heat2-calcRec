import os
import re
import statistics as st
import time
import traceback
import inquirer

### NOTE: Scriptet virker nu.
# Forbedringer: vælg alle filer


### DEFINITIONS ###

def starttext():
    printline(1,0)
    intro = [
    '| - Script by Lasse Hamborg - 24.11.2022 -',
    '| ',
    '| This script reads record files from HEAT2 transient analyses.',
    '| Make sure your .REC file is located in the same folder as this script.',
    '| (NB: In the following queries, press ENTER for default input.)',
    '| ',
    '- - - - - - - - - - - - - - - - - - - - -',
    '| ',
    '| First:\tIf you have multiple .REC files, choose what files should be run.',
    '| \t\tIn the end, the script script repeats if you want to go through more files.',
    '| \t\tIf you choose all files, the following choices will apply to all files!',
    '| ',
    '| Second:\tChoose your summerization period.',
    '| \t\tThis depends on how your transient analysis was setup in HEAT2.',
    '| \t\t(Default choice is Choose file from the listbis needed for yearly analyses.)',
    '| ',
    '| Third:\tChoose what statistics should be included in the result file.',
    '| \t\tAll statistics are calculated for each data point from HEAT2.',
    '| \t\t(As default, only average is included.',
    '| \t\tOther available statistics are: Minimum, Maximum and Sum.)',
    '| ',
    '| Lastly:\tChoose how many of the last record periods (period chosen above) that should be included.',
    '| \t\tThis can be handy if the transient analysis is e.g. 30 years.',
    '| \t\tFor example, choose 13 to include the last year and very month before.',
    '| \t\t(By default, all record periods are included.)',
    '| ',
    '| The script prompts for re-run. (Default is to run again untill all .REC files are collected.)',
    '| The resulting file can then be located in the folder as \"(filename) - RESULTS.csv\".'
    ]
    for text in intro: print(text)
    printline(0,1)
    time.sleep(2)

def printline(x,y):
    if x: start = '\n'
    else: start = ''
    if y: end = '\n'
    else: end = ''
    print(start+'- - - - - - - - - - - - - - - - - - - - -'+end)

def finish():
    if all_files: return True
    else: printline(1,1); time.sleep(0.5)
    if input('- Run again? (\'x\' to exit.) \n- ').lower() not in ['exit','quit','x','n','no']:
        print('\nScript runs again')
        for _ in [1,2,3]:
            time.sleep(0.5)
            print('')
        printline(1,1)
        time.sleep(0.5)
        return True
    
def afslutter():
    time.sleep(0.5)
    printline(1,1)
    time.sleep(0.5)
    print('Script terminates...')
    time.sleep(2)
    print('\n- Goodbye -')
    time.sleep(10)
    quit()

def groupDataValues():
    for cidx, dataCol in enumerate(Data[1:]): ValueCollection[cidx].append(dataCol[start:slut])

def intNum(num):
    try: newNum = int(num)
    except: newNum = num
    return newNum

def fullTimeName(tc):
    name = ''
    for i in range(0,periodeID+1):
        if i != 0: name += ' '
        match codestring[i]:
            case 'y': name += 'year '
            case 'q': name += 'month '
            case 'd': name += 'day '
            case 'h': name += 'hour '
            case 'm': name += 'minute '
            case 's': name += 'second '
        name += str(intNum(tc[i]))
    return name

def groupName(tc):
    fullname = fullTimeName(tc)
    nameCollection.append(fullname)

def checkInput(besked):
    inp = input('- Should '+besked+' be calculated? (Y/N) - ')
    if inp.lower() not in ['y','j','n','yes','no'] and len(inp) > 0: print('(Invalid input. Calculation of '+besked+' is included.)')
    if inp.lower() in ['n','no']: inp = False
    else: inp = True
    return inp


### START ###
starttext()

### Filer lokaliseres:
files = []
dirfiles = os.listdir()
recs = [x for x in dirfiles if x.endswith(".rec")]
rec_count = len(recs)

if len(recs) > 0:
    print('\n- - - REC FILES IN FOLDER: - - -')
    for i in recs: print(i)
    printline(0,1)
    time.sleep(2)
else:
    print('Oops! There are no .REC files in the folder.')
    afslutter()


### Script kører:
run_count = 1
all_files = False
speed_run = False
scriptOn = True
while scriptOn:
    ### 1: Filer vælges:
    if all_files:
        rec = recs[0]
        speed_run = True
    else:
        print('- - - 1: Choose file: - - -')
        msgREC = "Which of the .REC files do you want analysed?"
        if len(recs) > 1:
            try:
                choices = [r for r in recs]
                choices.append('(All files)')
                # traceback()
                questions = [inquirer.List('rec',
                            msgREC+" (use arrow keys ↓ ↑)",
                            choices)]
                answers = inquirer.prompt(questions)
                
                rec = answers['rec']
                all_files = rec == choices[-1]
                if all_files: rec = recs[0]

            except:
                print(msgREC)
                ch = 1
                for fil in choices: print(str(ch) + ')\t' + fil); ch += 1
                recCh = input('File number? - ')
                all_files = recCh == str(len(choices))
                while True:
                    if all_files:
                        rec = recs[0]
                        break
                    try: int(recCh)
                    except: recCh = input('\nInvalid choice. - Choose file from the list (number).\n- '); continue
                    if int(recCh) not in range(1,len(choices)+1):
                        recCh = input('\nInvalid choice. - Choose file from the list (number).\n- ')
                        continue
                    else:
                        rec = recs[int(recCh)-1]
                        break
        else:
            rec = recs[0]
            time.sleep(0.5)
            if run_count > 1 and len(recs) == 1: print('\nLast file in the folder automatically chosen.\n')
            elif len(recs) > 1: print('')
            else: print('(1: Only one file found.)')
        
        if all_files:
            print('All files will be analysed.\nHence, the following choices will apply for ALL the files!')
            speed_recs = [rec for rec in recs]
    
        time.sleep(0.5)
    
    if not all_files: print('\nChosen file:\n- '+rec)
    # quit()

    ### Åbn .rec-fil:
    recfile = rec.split('.')[0]
    fr = open(recfile + '.rec',"r")

    resfile = recfile + ' - RESULTS.csv' # Resultatfil
    files.append(resfile)

    
    if not speed_run:
        ### 2: Bruger vælger summeringsperiode:
        time.sleep(0.5)
        valg = input("\n- - - 2: Choose summerization period: - - -\nCollect: ([y]ears, [m]onths, [d]ays, [h]ours, mi[n]utes, [s]econds) - [Default: Months]\n- ").lower()
        validPeriode = ['y','m','q','d','h','n','s']
        time.sleep(0.5)
        while valg not in validPeriode:
            if len(valg) < 1:
                print('Default value chosen: Summerisation over MONTHS.')
                valg = 'm'
            else: valg = input('\nOBS: Choose either \'y\', \'m\', \'d\', \'h\', \'n\' or \'s\'! \n- ').lower()
        
        printline(0,1)

        periode = valg
        if periode in ['m','M']: periode = 'q'
        elif periode in ['n','N']: periode = 'm'

        codestring = 'yqdhms'
        periodeID = codestring.find(periode)

        ### 3: Vælg beregninger:
        time.sleep(0.5)
        print('- - - 3: Choose statistics: - - -')
        if not all_files: print('For the file \''+recfile+'\' - which information should be analysed?')
        stats = input('Include other statistics than average (Y/N)? [Default: No]\n- ')
        if len(stats) < 1 or stats.lower() in ['no','n']:
            chAvr     = True
            chMaxMin  = False
            chSum     = False

        else:
            print('\nChoose specifically what should be included: [Default: Yes]')
            chAvr = checkInput('average')
            chMaxMin = checkInput('minimum and maksimum')
            chSum = checkInput('sum')

        calcs = chAvr*1 + chMaxMin*2 + chSum*1
        moreCalcs = calcs > 1

        time.sleep(0.5)
        if calcs < 1: print('Nothing chosen! - Average value is included as default.\n'); chAvr = True; calcs = 1
        print('\nThe following statistic'+moreCalcs*'s'+ (1-moreCalcs)*' is' + moreCalcs*' are' + ' included:\n-'\
                 + chAvr*' Average' + chAvr*chMaxMin*',' + chMaxMin*' Maximum and Minimum' + chMaxMin*chSum*',' + chSum*moreCalcs*' and' + chSum*' Sum'+'.')
        printline(0,1)
        time.sleep(1)


    ##### MAIN CALCULATION ENGINE: #####        

    ### Læs .rec-fil:
    rec_lines = fr.readlines()[2:]
    rec_rows = [line for line in rec_lines]

    translate_file = []
    for line in rec_rows:
        ### Trim data:
        row = line.replace(" [","_[").replace('%','').split()

        trans_line = ""
        ### Skriv trimmet data til csv-fil:
        for i in row: trans_line += i.replace('_',' ') + ';'
        trans_line += '\n'
        translate_file.append(trans_line)


    rLines = translate_file
    header = rLines[0].split(';')[:-1] # Linje med overskriftsnavne - bruges i slutfil
    rows = [line.split(';') for line in rLines[1:]]
    
    ### Lav data-tabel med values:
    Data = []
    if rows[-2] == rows[-1]: rows.pop(-1) # Sidste to linjer er tit ens. Sidste af disse fjernes således.
    for col in range(len(rows[0])-1): # sidste element er liste med '\n'
        Data.append([value[col] for value in rows])

    ### Konvertér values fra string til float:
    for ix, col in enumerate(Data[1:]):
        for jx, e in enumerate(col):
            Data[ix+1][jx] = float(Data[ix+1][jx])

    ### Match time-strings som keys til sammenligning. Sættes som ny første-kolonne i Data:
    NewTimeKeys = []        # Liste med nye sorterede tidsværdier
    for t in Data[0]:
        timekeys    = re.findall('[a-z]+',t)
        timevalues  = re.findall('[0-9]+',t)

        newKey = [0]*len(codestring) # Laver en 0-liste til sortering af tidskoder
        for keyID, key in enumerate(timekeys):
            idplace = codestring.find(key) # Finder key i "yqdhms"
            newKey[idplace] = float(timevalues[keyID])

        NewTimeKeys.append(newKey)
    Data[0] = NewTimeKeys

    ### Sammenlign timekeys med forrige timekey. Gem start- og slut-listeindex til samling af lister:
    ValueCollection = [[] for _ in Data[1:]] # Liste til sorterede og samlede dataværdier
    nameCollection = [] # Liste til tidsperioder

    nystart = None
    for idx, tc in enumerate(Data[0]):
        if nystart: start = nystart
        
        ### Første værdi
        if idx == 0: 
            start = 0
            if len(Data[0]) < 2:
                slut = 1
                groupName(tc)
                groupDataValues() # Putter opdelte data i ValueCollection
            continue
        
        ### Samme som forrige værdi
        elif NewTimeKeys[idx][periodeID] == NewTimeKeys[idx-1][periodeID]:
            if tc == Data[0][-1]:
                slut = idx+1
                groupName(tc)
                groupDataValues() # Putter opdelte data i ValueCollection
            continue
        
        ### Forskellig fra forrige værdi
        else:
            slut = idx
            groupName(Data[0][idx-1])
            groupDataValues() # Putter opdelte data i ValueCollection
            
            nystart = idx

    ### Vi har nu en 'nameCollection'-liste med tidsnavne for hver liste i 'ValueCollection'-matricen.

    ### NOTE: OBS: Overstående loop sorterer KUN for den angivne periode! Dvs. hvis der f.eks. summeres over dage, betragtes der ikke, om året eller måneden har ændret sig, selvom dagen måske ikke har!
    ### Det burde ikke blive et problem, men vær obs. på dette, hvis tidsintervallerne er meget skæve.



   

    ### Udfør og saml beregninger af værdier - Opbyg underoverskrift:
    avrs = []; maxs = []; mins = []; sums = []
    subHeader = ';'

    for c in ValueCollection:
        cAvr = []; cMax = []; cMin = []; cSum = []

        for vl in c:
            if chAvr: cAvr.append(round(st.mean(vl),3))
            if chMaxMin: cMax.append(round(max(vl),3)); cMin.append(round(min(vl),3))
            if chSum: cSum.append(round(sum(vl),3))

        if chAvr: avrs.append(cAvr);                        subHeader += "Average;"
        if chMaxMin: maxs.append(cMax); mins.append(cMin);  subHeader += "Maximum;Minimum;"
        if chSum: sums.append(cSum);                        subHeader += "Sum;"

        if calcs > 1: subHeader += ";"
    subHeader += "\n"

    MathTable = [l for l in [avrs,maxs,mins,sums] if len(l)>0]

    ### Saml linjer til indskrivning:
    wLines = [[] for _ in nameCollection] # Skriv én linje (i ny fil) pr. sammenlagt tidsperiode (i 'nameCollection')

    for tidx, t in enumerate(nameCollection):
        wLines[tidx].append(t)
        for i in range(0,len(Data[1:])):
            for cidx, c in enumerate(MathTable):
                wLines[tidx].append(c[i][tidx])
            if moreCalcs and i != len(Data[1:])-1: wLines[tidx].append('-')

    if not speed_run:
        ### 4: Spørg bruger om datamængde:
        print('- - - 4: Choose no. of records: - - -')
        try:
            last_periods = input('How many of the last periods should be included? [Default: All]\n- ')
            ammount = int(last_periods)
            time.sleep(0.5)
            if ammount < 1: traceback()
        except:
            if last_periods.lower() in ['a','all','alle']: invalid = False
            else: invalid = True
            print(invalid*'Invalid value. - '+'All', len(wLines), 'periods are being included.')
            time.sleep(1)
            ammount = 0
        if ammount > len(wLines): ammount = len(wLines)

        printline(0,1)
        time.sleep(0.5)

        if all_files:
            print('\nRUNNING THROUGH ALL FILES!\n')
            time.sleep(1)
            

    ### Lav ny Results-CSV-fil.
    fw = open(resfile, "w")

    ### Skriv overskrift på data:
    headPush = 1*moreCalcs+calcs
    fw.write(header[0]+';')
    for h in header[1:]: fw.write(h+';'*headPush)
    fw.write('\n')

    if headPush > 2 : fw.write(subHeader) # Skriver kun sub-header, hvis der er flere beregninger pr. værdi-kolonne.

    ### Skriv resultatdata til CSV-fil:
    for l in wLines[-ammount:]:
        wline = ''
        for e in l:
            wline += str(e)#.replace('.',',') # Komma-tal i Excel
            wline += ";"
        wline += "\n"
        fw.write(wline) # Skriv til fil

        
    ##### SCRIPT CONCLUSION #####

    ### Luk filer:
    fr.close()
    fw.close()

    if not all_files:
        print('- - - RESULTS: - - -')
        print('A results file was created:',resfile)
        time.sleep(0.5)
        print('It is located in the folder.')
    
    ### Automatiske beskeder:
    if speed_run and len(recs) == 1:
        print('\nD O N E !')
        printline(1,1)
        time.sleep(0.5)
        print('These files were automatically analysed:')
        for f in speed_recs: print("- \""+f+"\"")
        time.sleep(2)
        print('\nThey were all analysed with the same inputs:')
        print('- Summerisation period:\t'+periode)
        print('- The following statistic'+moreCalcs*'s'+ (1-moreCalcs)*' was' + moreCalcs*' were' + ' included:' + chAvr*' Average' + chAvr*chMaxMin*',' + chMaxMin*' Maximum and Minimum' + chMaxMin*chSum*',' + chSum*moreCalcs*' and' + chSum*' Sum'+'.')
        print('- The last '+str(ammount)+' records were included.')
        time.sleep(2)
        print('\nThe files are located in the folder.')
        time.sleep(5)

    if run_count != rec_count > 1:
        run_count += 1
        scriptOn = finish()
        recs.pop(recs.index(rec))
        continue
    else:
        break


if len(files) > 1:
    printline(1,1)
    print('Multiple result files was created:\n')
    for f in files: print("- \""+f+"\"")
    printline(0,1)

time.sleep(5)
afslutter()