# Natural Language Processing
# DB:
#    TABLE 26x ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']_words
#    COLUMN 9x (id_word INTEGER PRIMARY KEY, word TEXT UNIQUE, word_utf TEXT, name_of_pos TEXT, pos INTEGER, sentiment_score REAL, weight REAL, classification REAL, unit REAL)
#    ('id_word',)('uid_word',)('word',)('word_utf',)('name_of_pos',)('pos',)('sentiment_score',)('weight',)('classification',)('unit',)
#
#    classification:
#    0  = normalne slova
#    10 = klucove slova ktore vyjadruju nejaku funkciu/cinnnost (cpk,ftq,korelacia,info,...) [what]
#    11 = nazvy pre ktore sa konkretna funkcia spusta (assyName) [where]
#    12 = konkretne nazvy/mena spojene z nizsimi klasifikaciami (nameStationPc, Station) [who]
#    13 = konkretne nazvy/mena spojene z nizsimi klasifikaciami (Measure, emails,... ) [this one]
#    AHA priklad klasifikacie:
#                najdi korelaciu medzi stanicou ST10 a ST20 na MQB1 . pridaj a@marelli.com do projektu MQB2 .
#                  0       10      0       0     12     12   0  11      0         13       0     0      11
#                  |_______|                                            |_________|
#
#

import re
import sqlite3
import requests
import os
import json
import sys
from time import perf_counter, sleep

class NLPdb():
    
    def create(db, cur, table):
        try:       
            sql_cmd = "CREATE TABLE IF NOT EXISTS "+table+" (id_word INTEGER PRIMARY KEY, uid_word INTEGER UNIQUE, word TEXT UNIQUE, word_utf TEXT, name_of_pos TEXT, pos INTEGER, sentiment_score REAL, weight REAL, classification REAL, unit REAL)"
            print('[SQL3] {}'.format(sql_cmd))
            cur.execute(sql_cmd)
            db.commit()        
        except:
            print('[!] SQlite3 : Error create table !')
    
    
    def show(cur, table):
        
        sql_cmd = 'SELECT rowid,* FROM ' + table
        print('[SQL3] {}'.format(sql_cmd))
        row = cur.execute(sql_cmd).fetchall()

        for i in row:
            print(i)
            
        return row
    
    
    def show_tables(cur):
        
        #cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        cur.execute("SELECT name FROM pragma_table_info('a_words')")
        tables = cur.fetchall()
        
        for table in tables:
            print(table)
            
    
    def delete(db,cur,inject8):
        
        #DELETE FROM CRICKETERS WHERE LAST_NAME = 'Sangakkara'
        id_word = inject8[0]
        uid_word = inject8[1]
        word = inject8[2]
        word_utf = utf_word(word)
        table = word_utf[0]
        table = table + '_words' 
        
        sql_cmd = "DELETE FROM " + table + " WHERE word_utf='{}'".format(word_utf)
        print('[SQL3] {}'.format(sql_cmd))
        cur.execute(sql_cmd)
        
        print(db.total_changes)
        db.commit()        
        
    
    def add(db, cur, inject8):
        
        word = inject8[0]
        word_utf = utf_word(word)
        pos = int(inject8[1])
        
        if pos == 1:
            name_of_pos = 'podstatné'
        elif pos == 2:
            name_of_pos = 'prídavné'
        elif pos == 3:
            name_of_pos = 'zámená' # 'opytovací','vymedzovací',privlastňovací'
        elif pos == 4:
            name_of_pos = 'číslovka'
        elif pos == 5:
            name_of_pos = 'sloveso'
        elif pos == 6:
            name_of_pos = 'príslovka'
        elif pos == 7:
            name_of_pos = 'predložka'
        elif pos == 8:
            name_of_pos = 'spojka'
        elif pos == 9:
            name_of_pos = 'častica'
        elif pos == 10:
            name_of_pos = 'citoslovce'
        else:
            name_of_pos = ''
      
        sentiment_score = inject8[2]
        weight = inject8[3]
        classification = inject8[4]
        unit = inject8[5]
        
        table = word_utf[0]
        table = table + '_words'
        
        last = NLPdb.show(cur, table)
        last = last[-1]
        
        id_word = int(last[1])+1
        uid_word = int(last[2])+1        
        
        sql_cmd = "INSERT INTO " + table + " (id_word, uid_word, word, word_utf, name_of_pos, pos, sentiment_score, weight, classification, unit) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        
        try:
            cur.execute(sql_cmd, (id_word, uid_word, word, word_utf, name_of_pos, pos, sentiment_score, weight, classification, unit))
            print('[SQL3] {} << ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(sql_cmd , id_word, uid_word, word, word_utf, name_of_pos, pos, sentiment_score, weight, classification, unit))
            print(db.total_changes)
            db.commit()
        except sqlite3.IntegrityError:
            print('[SQL3]  UNIQUE constraint failed: EXIST {}'.format(word))
    
    
    def update(db, cur, uword, upos):
        
        #find()
        data = NLPdb.find(db, cur, uword)
        print(data)
        if len(data) != 0:
            utf_uword = data[0][4]
            uid_uword = data[0][2]
        
            table = uword.lower()[0]
            table = utf_word(table)
            table = table + '_words'        
        
            sql_cmd = "UPDATE " + table + " SET name_of_pos='sloveso', pos={} WHERE word_utf='{}' AND uid_word={}".format(upos, utf_uword, uid_uword)
            print('[SQL3] {}'.format(sql_cmd))
            cur.execute(sql_cmd)
            db.commit()
        else:
            print('[-] nlu: update fail - "{}" not in database.'.format(uword))
        
        pass
       
    
    def find(db, cur, fword):
        row = []
        
        abeceda = ['a','b','c','d','e','f','g','h','ch','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','znak']
        znaky = ['.',',','!','?','%', ':', '_', '-', '+', '=', '<', '>', '@', '*', '^']
        znak = fword.lower()[0]    # zober iba prvy znak
        znak = utf_word(znak)     # dekoduj znak do utf
        if znak in abeceda:    
            table = znak + '_words'    # vytvor meno tabulky
            sql_cmd = "SELECT rowid,* FROM " + table
            sql_cmd +=" WHERE word_utf='{}'".format(fword)
            sql_cmd +=" OR word='{}'".format(fword)
            print('[SQL3] {}'.format(sql_cmd))
            row = cur.execute(sql_cmd).fetchall()

            for i in row:
                print(i)
        elif znak in znaky:
            table = 'znak_words'    # vytvor meno tabulky
            sql_cmd = "SELECT rowid,* FROM " + table
            sql_cmd +=" WHERE word_utf='{}'".format(fword)
            sql_cmd +=" OR word='{}'".format(fword)
            print('[SQL3] {}'.format(sql_cmd))
            row = cur.execute(sql_cmd).fetchall()

            for i in row:
                print(i)
                
        return row
            
              
# ------------------------------------------------------------------------------------------------------------------------------------
# Vykradanie webu kvoly KSSJ https://slovnik.aktuality.sk/pravopis/kratky-slovnik/ & https://slovnik.aktuality.sk/pravopis/?q=ahoj
# Vytvory slovniky vo formate json
def robbery_sj():
    
    current_path = os.getcwd()
    jfile = current_path + '\\kssj.json' # kratky-slovnik
    #jfile = current_path + '\\ssj.json' # slovnik-sj
    #jfile = current_path + '\\scs.json' # slovnik-cudzich-slov
    #jfile = current_path + '\\synss.json' # synonymicky slovnik slovenciny
    
    url = "https://slovnik.aktuality.sk/pravopis/kratky-slovnik/a/1/"
    #url = "https://slovnik.aktuality.sk/pravopis/slovnik-sj/a/1/"
    #url = "https://slovnik.aktuality.sk/slovnik-cudzich-slov/a/1/"
    #url = "https://slovnik.aktuality.sk/synonyma/a/1/"
    
    abeceda = ['a','b','c','d','e','f','g','h','ch','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    data = {}
    
    for pismeno in abeceda:
        data_web = []
        for cislo in range(1,99):
 
            url = "https://slovnik.aktuality.sk/pravopis/kratky-slovnik/{}/{}/".format(pismeno, cislo)
            #url = "https://slovnik.aktuality.sk/pravopis/slovnik-sj/{}/{}/".format(pismeno, cislo)
            #url = "https://slovnik.aktuality.sk/pravopis/slovnik-cudzich-slov/{}/{}/".format(pismeno, cislo)
            #url = "https://slovnik.aktuality.sk/pravopis/synonyma/{}/{}/".format(pismeno, cislo)
    
            try:
                page = requests.get(url)
                text = page.text
                robbery = re.findall('<a href=/pravopis/kratky-slovnik/\?q=.*</a>', text)
                #robbery = re.findall('<a href=/pravopis/slovnik-sj/\?q=.*</a>', text)
                #robbery = re.findall('<a href=/pravopis/slovnik-cudzich-slov/\?q=.*</a>', text)
                #robbery = re.findall('<a href=/pravopis/synonyma/\?q=.*</a>', text)
                if len(robbery) == 0:
                    break
                
                for r in robbery:
                    r.replace('<a href=/pravopis/kratky-slovnik/?q=', '')
                    #r.replace('<a href=/pravopis/slovnik-sj/?q=', '')
                    #r.replace('<a href=/pravopis/slovnik-cudzich-slov/?q=', '')
                    #r.replace('<a href=/pravopis/synonyma/?q=', '')
                    r = r.replace('</a>', '')
                    r = r.split('>')
                    print(r[-1])
                    data_web.append(r[-1])
            except:
                print('[!] Fail connection: check network, firewall, proxy!')
                input('[-] Press any key to quit.')
                return 404
        
        data[pismeno] = data_web
    
    
    with open(jfile, "w", encoding='utf8') as json_file:
        data = json.dumps(data, ensure_ascii=False, indent=4)
        json_file.write(str(data))        

    print('[+] Create file: {}!'.format(jfile))
    
        #print('[-] Failed create file: {}!'.format(jfile))
        #return True        

# Vyskrabaj z webu data pre urcenie slovnych druhov
# Nahod serveru slovo zo slovnika a zisti slovny druh
# 16 minut = 10%, 9730.13s = 100%
def scraping_sj():

    start_timer = perf_counter()
    abeceda = ['a','b','c','d','e','f','g','h','ch','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    current_path = os.getcwd()
    
    nlp_path = current_path + '\\NLP'
    if not os.path.isdir(nlp_path):
        try:
            os.mkdir(nlp_path)
            print('[+] Dir created: {}.'.format(nlp_path))
        except: 
            print('[-] Dir not created: {}!'.format(nlp_path))
            nlp_path = current_path
            
    
    jfile = current_path + '\\kssj.json' # kratky-slovnik
    #jfile = current_path + '\\ssj.json' # slovnik-sj
    #jfile = current_path + '\\scs.json' # slovnik-cudzich-slov
    #jfile = current_path + '\\synss.json' # synonymicky slovnik slovenciny
    
    #url = "https://slovnik.aktuality.sk/pravopis/?q={}".format('akosi')
    url = "https://slovnik.aktuality.sk/pravopis/kratky-slovnik/?q={}".format('amen') #ale amen
    data = {}

    if os.path.exists(jfile):
        
        db = sqlite3.connect('nlu1.db')
        cur = db.cursor()        

        with open(jfile, 'r', encoding='utf8') as f:
            slovnik = json.load(f)
        
        # spocitaj kolko slov je v slovniku
        pocet_slov = 0
        for c in abeceda:
            pocet_slov += int(len(slovnik[c]))

        c = 0
        time_check = True
        for pismeno in slovnik:
            data_pismeno = {}
        
            for slovo in slovnik[pismeno]:
                if int(c/pocet_slov*100) >= 10 and time_check:
                    time_check = False
                    end_timer = perf_counter()
                    print('[TIME] {} s'.format(format((end_timer - start_timer),'.2f')))
                    sleep(3)
                    
                print('[{}/{}]{}% {}'.format(c, pocet_slov, format((c/pocet_slov*100), '.2f'),slovo))
                c += 1
                #url = "https://slovnik.aktuality.sk/pravopis/?q={}".format(slovo)
                url = "https://slovnik.aktuality.sk/pravopis/kratky-slovnik/?q={}".format(slovo)
                
                for cr in range(10):
                    try:
                        page = requests.get(url)
                        break
                    except:
                        print('[!] Fail connection: check network, firewall, proxy!')
                        sleep(1)
                    
                text = page.text

                robbery = re.findall('<span class="b0"><a href="/pravopis/.*', text, re.DOTALL)    # najde riadok kde je pattern
                
                if len(robbery) != 0:
                    for j in range(len(robbery)):
                        robbery[j] = robbery[j].replace('"', '')
                        robbery[j] = re.findall('title=\w+', robbery[j])
                    robbery = [ a for b in robbery for a in b]                        
                    
                    titles = []
                    for r in robbery:
                        r = r.replace('title=','')
                        titles.append(r)
                    
                    if len(titles) > 10:
                        titles = titles[:10]
                        
                    title = 0
                    if len(titles) > 0: # ak zozname nie je prazdny
                        
                        if len(titles) == 1: # ak je v zozname iba jedna moznost
                            if titles[0] in ['podstatné' , 'prídavné' , 'spojka' , 'príslovka' , 'sloveso' , 'častica' , 'citoslovce', 'číslovka', 'predložka',  'opytovací' ,'vymedzovací', 'privlastňovací']:
                                title = titles[0] # ulozit ak je v zozname
                            else:
                                title = 0 # ulozit 0
                        else:
                            if len(titles) > 1: # ak je ich viac
                                list_of_pos = []
                                if titles[0] in ['podstatné' , 'prídavné' , 'spojka' , 'príslovka' , 'sloveso' , 'častica' , 'citoslovce', 'číslovka', 'predložka',  'opytovací' ,'vymedzovací', 'privlastňovací']:
                                    title = titles[0] # ulozit ak je v zozname
                                else:
                                    for pos in titles: # prejde cely zoznam a vyfiltruje iba slovne druhy
                                        if pos in ['podstatné' , 'prídavné' , 'spojka' , 'príslovka' , 'sloveso' , 'častica' , 'citoslovce', 'číslovka', 'predložka',  'opytovací' ,'vymedzovací', 'privlastňovací']:
                                            list_of_pos.append(pos) # ulozi do noveho zoznamu iba slovne druhy 
                                        
                                    if len(list_of_pos) == 0: # ak v novom zozname nie je nic
                                        title = 0 # ulozit 0
                                    elif len(list_of_pos) >= 1: # ak v novom zozname je aspon jeden slovny druh
                                        aladin = False
                                        for l in list_of_pos: # prejde cely zoznam a ak su vsetky druhy rovnake tak ulozi
                                            if l != list_of_pos[0]:
                                                aladin = True
                                        if aladin == False:
                                            title = list_of_pos[0]
                                        else:
                                            title = titles                               
                    else: # ak je zoznam prazdny
                        title = 0
                        print('{} | {}'.format( slovo, titles ))

                    data[slovo] = title
                    data_pismeno[slovo] = title
                    
                #if slovo[1] == 'd':
                #    print(data)
                #    break
            #break
            
            # uloz subor po kazdom pismene 
            jfile_plus_pismeno = nlp_path + '\\kssj_plus_' + pismeno + '.json'
            with open(jfile_plus, "w", encoding='utf8') as json_file:
                data_pismeno = json.dumps(data_pismeno, ensure_ascii=False, indent=4)
                json_file.write(str(data_pismeno))         
            print('[ok]')
        
        jfile_plus = nlp_path + '\\kssj_plus.json'
        with open(jfile_plus, "w", encoding='utf8') as json_file:
            data = json.dumps(data, ensure_ascii=False, indent=4)
            json_file.write(str(data))    
            
        print('[ok]')
        db.commit()
        
# Manualne urcenie chybajucich priradeni. NIKDY NEPOUZITE
def manual_pos():
    
    current_path = os.getcwd()
    jfile_plus = current_path + '\\kssj_plus.json'
    
    if os.path.exists(jfile_plus):
        with open(jfile_plus, 'r', encoding='utf8') as f:
            slovnik = json.load(f)
        i = 0
        for slovo, value in slovnik.items():
            print('{} {}'.format(slovo, value))

# Naplni databazu z json slovnika
def json2sql():
    
    abeceda = ['a','b','c','d','e','f','g','h','ch','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','znak']
    name_pos = ['podstatné', 'prídavné' 'zámená', 'opytovací', 'vymedzovací', 'privlastňovací', 'číslovka', 'sloveso', 'príslovka', 'predložka', 'spojka', 'častica', 'citoslovce']
    
    current_path = os.getcwd()
    jfile_plus = current_path + '\\kssj_plus.json'    
    
    db = sqlite3.connect('nlu1.db')
    cur = db.cursor()
    
    for pismeno in abeceda:
        table_name = pismeno + "_words"
        NLPdb.create(db, cur, table_name)
        
    NLPdb.show_tables(cur)
    
    if os.path.exists(jfile_plus):
        with open(jfile_plus, 'r', encoding='utf8') as f:
            slovnik = json.load(f)
        i = 0
        ui = 0
        pos = 0
        prev_table_name = '_words'
        for slovo, value in slovnik.items():
            
            if value == 'podstatné':
                pos = 1
            elif value == 'prídavné':
                pos = 2
            elif value == 'opytovací' or value == 'vymedzovací' or value == 'privlastňovací' or value == 'zámená':
                pos = 3
            elif value == 'číslovka':
                pos = 4
            elif value == 'sloveso':
                pos = 5
            elif value == 'príslovka':
                pos = 6
            elif value == 'predložka':
                pos = 7
            elif value == 'spojka':
                pos = 8
            elif value == 'častica':
                pos = 9
            elif value == 'citoslovce':
                pos = 10
            else:
                pos = 0
                #if isinstance(value, (list, tuple)):
                #    value.count('podstatné')
                                
            
            #print('[+] {} \t\t{} \t\t{}'.format(slovo, value, pos))
            
            table_name = slovo.lower()[0]
            table_name = utf_word(table_name)
            table_name = table_name + '_words'
            
            if table_name != prev_table_name:
                prev_table_name = table_name
                i = 0
                
            inject8 = [i, ui ,slovo, pos, 0, 0, 0, 0]
            NLPdb.add(db, cur, table_name, inject8) #inject8 = (id_word, uid_word, word, pos, sentiment_score, weight, classification, unit)
            i += 1
            ui += 1
            
    #clasifikacia 0 = ziadna
    #clasifikacia 1 = pozdrav
  

# ------------------------------------------------------------------------------------------------------------------------------------
# Prevod slova do UTF-8 kodovania
def utf_word(word):
    word = re.sub('á','a', word)
    word = re.sub('é','e', word)
    word = re.sub('í','i', word)
    word = re.sub('ó','o', word)
    word = re.sub('ú','u', word)
    word = re.sub('ý','y', word)
    word = re.sub('ä','a', word)
    word = re.sub('ô','o', word)
    
    word = re.sub('ď','d', word)
    word = re.sub('ť','t', word)
    word = re.sub('ň','n', word)
    word = re.sub('ľ','l', word)
    word = re.sub('č','c', word)
    word = re.sub('ž','z', word)
    word = re.sub('š','s', word)
    word = re.sub('ŕ','r', word)   
    
    return word
    
# Rozdeli vetu na pole slov
def tokenize_words(body):
    
    utf = True
    if utf:
        #body = unidecode.unidecode(body)
        #body = re.sub('[^0-9a-zA-Z_-]', '', body)
        body = body.lower()
        body = re.sub('á','a', body)
        body = re.sub('é','e', body)
        body = re.sub('í','i', body)
        body = re.sub('ó','o', body)
        body = re.sub('ú','u', body)
        body = re.sub('ý','y', body)
        body = re.sub('ä','a', body)
        body = re.sub('ô','o', body)
        
        body = re.sub('ď','d', body)
        body = re.sub('ť','t', body)
        body = re.sub('ň','n', body)
        body = re.sub('ľ','l', body)
        body = re.sub('č','c', body)
        body = re.sub('ž','z', body)
        body = re.sub('š','s', body)
        body = re.sub('ŕ','r', body)
        
    body = body.replace('. ', ' . ')
    body = body.replace(',', ' , ')
    body = body.replace('?', ' ? ')
    body = body.replace('!', ' ! ')

    return body.split(' ')


# Oprava pravopisu
def correct():
    pass

# Rozdeli vstup na pole viet. 
def sentence(body):
    pass

# Roztriedi pole slov podla tagov POS - Part-of-speech Tagging
def tags(db, cur, body_token):
 
    poradie = 0
    output = []

    for gram in body_token:
        if len(gram) != 0:
            #print('slovo={} len={}'.format(gram, len(gram)))
            ret = NLPdb.find(db, cur, gram)
            
            if len(ret) == 0 and gram.isnumeric():
                #print('{} = ciiiiiislo to je'.format(int(gram)))
                output.append(int(gram))
            elif len(ret) == 0:
                output.append('None')
            elif len(ret) > 0:
                output.append(ret)
            
    return output

# Zisti postoj (emocialny efekt) a polaritu spravy - emotion AI/opinion mining
# nazor moze by positiv, negativ alebo neutral
# return (classification[pos/neg/neutral], p_pos=[0-1], p_neg[0-1])
# return (polarity[-1-1], subjectivity[0-1]) 0.0 is very objective and 1.0 is very subjective.
def sentiment():
    pass

def statement_ai(lines_array, body_token):
    pass
        
        
def run(lines_array, body): 
    
    print(body)
    
    match1 = re.search('From:', body) # predchadzajuca sprava, preposielana medzi viacerimi
    
    if match1:      
        start_position = match1.start()
        body = body[:start_position] 
        print(body)
    
    # ----- tokenizen
    print('[NLP] tokenizing...')
    body_token = tokenize_words(body)
    print('[NLP] length of tokenize_words = {}'.format(len(body_token)))
    print(body_token)

    db = sqlite3.connect('nlu1.db')
    cur = db.cursor()
    
    # ----- hashlib.md5(str('lines_array').encode("utf-8")).hexdigest()
    if '12662a4b78e19ac27361b005a6dbb3d7' == body:
        print('[+] Checking new lines...')
        for la in lines_array:
            if len( NLPdb.find(db, cur, la[0]['assyName'].lower()) ) == 0:
                inject8 = [la[0]['assyName'].lower(), 1, 0, 0, 11, 0] 
                NLPdb.add(db, cur, inject8) # add
    
    
    #statement_ai(lines_array, body_token)
    
    body_token_tags = tags(db, cur, body_token)
    print(body_token_tags)
    
    #NLPdb.show_tables(cur)
    
    
    slovo = 'cw'      # <<<
    pos = 1             # <<<
    classification = 0 # <<<
    #NLPdb.update(db, cur, slovo, pos)

    inject8 = [slovo, pos, 0, 0, classification, 0] #<<<
    #NLPdb.delete(db, cur, inject8)
    #NLPdb.add(db, cur, inject8)
    
    
    #NLPdb.find(db, cur, slovo)
    #NLPdb.find(db, cur, 'hovno')
    #NLPdb.find(db, cur, '_')
    #NLPdb.find(db, cur, '>')
    #NLPdb.find(db, cur, 'a')
    #json2sql()
    
    #NLPdb.show(cur, 'b_words')
    db.close()
    
    #print(body_token)
    #print(body_token_tags)
    return body_token, body_token_tags
        
test = 0
if test > 0:
    lines_array= [[{'assyName': 'MQB1', 'projectName': 'SMT1', 'nameStationPc': '46E1SHI1', 'Station': 'SHI', 'ID_Station': 598, 'Measure': ['F0', 'F1', 'F2', 'F2_Zmax']}, {'assyName': 'MQB1', 'projectName': 'SMT1', 'nameStationPc': '46E1MOT1', 'Station': 'MOT', 'ID_Station': 597, 'Measure': ['RPM_Assembly_Force_Cel1', 'RPM_Assembly_Force_Cel2', 'SPEED_Assembly_Force_Cel1', 'SPEED_Assembly_Force_Cel2', 'TEMP_Assembly_Force_Cel1', 'TEMP_Assembly_Force_Cel2', 'FUEL_Assembly_Force_Cel1', 'FUEL_Assembly_Force_Cel2']}, {'assyName': 'MQB1', 'projectName': 'MQB', 'nameStationPc': '46E1ST05', 'Station': 'ST05', 'ID_Station': 581, 'Measure': ['Rear_strip_glueing_force', 'Front_strip_glueing_force', 'Front_tape_distance', 'Rear_tape_distance', 'FrontLeft_tape_distance', 'RearLeft_tape_distance']}, {'assyName': 'MQB1', 'projectName': 'MQB', 'nameStationPc': '46E1ST10', 'Station': 'ST10', 'ID_Station': 582, 'Measure': ['Sticking_force', 'Profilometer_Top_Right', 'Profilometer_Side_Top', 'Profilometer_Side_Bottom']}, {'assyName': 'MQB1', 'projectName': 'MQB', 'nameStationPc': '46E1ST20', 'Station': 'ST20', 'ID_Station': 589, 'Measure': ['PCB_position_Left', 'PCB_position_Right2', 'Clipping_LR', 'Clipping_LF', 'Clipping_RR', 'Clipping_RF', 'Camera_Connector_Angle', 'Camera_3_Flat_cable_Angle', 'Camera_3_Flat_cable_Top', 'Camera_3_Flat_cable_Bottom']}, {'assyName': 'MQB1', 'projectName': 'MQB', 'nameStationPc': '46E1ST30', 'Station': 'ST30', 'ID_Station': 584, 'Measure': ['Mask_Clip_LF', 'Mask_Clip_RL', 'Mask_Clip_RR', 'Mask_Clip_LR', 'Force_of_left_supply', 'Force_of_right_supply', 'Force_of_middle_supply']}, {'assyName': 'MQB1', 'projectName': 'MQB', 'nameStationPc': '46E1ST40', 'Station': 'ST40', 'ID_Station': 585, 'Measure': ['ST2_Force_Temp_MAX', 'ST2_Height_Temp_g', 'ST2_Angle_of_pointer_press_Temp', 'ST2_Force_Fuel_MAX', 'ST2_Height_Fuel_g', 'ST2_Angle_of_pointer_press__Fuel', 'ST3_Force_Speed_MAX', 'ST3_Height_Speed_g', 'ST3_Angle_of_pointer_press__Speed', 'ST3_Force_RPM_MAX', 'ST3_Height_RPM_g', 'ST3_Angle_of_pointer_press__RPM', 'Delta_of_small_pointers_hight', 'Delta_of_big_pointers_hight']}, {'assyName': 'MQB1', 'projectName': 'MQB', 'nameStationPc': '46A1ST60', 'Station': 'ST60', 'ID_Station': 586, 'Measure': ['Mask_Clip_Down_Left', 'Mask_Clip_Down_Right', 'Mask_Clip_Up_Left', 'Mask_Clip_Up_Right', 'Screwing_Torque_Result_3', 'Screwing_Torque_Result_4', 'Screwing_Torque_Result_1', 'Screwing_Torque_Result_2', 'Screw_Hight_LeftDown', 'Screw_Hight_RightDown', 'Screw_Hight_LeftUp', 'Screw_Hight_RightUp']}], [{'assyName': 'MQB2', 'projectName': 'MQB', 'nameStationPc': '46E2ST05', 'Station': 'ST05', 'ID_Station': 668, 'Measure': ['Rear_strip_glueing_force', 'Front_strip_glueing_force', 'Front_tape_distance', 'Rear_tape_distance', 'FrontLeft_tape_distance', 'RearLeft_tape_distance']}, {'assyName': 'MQB2', 'projectName': 'MQB', 'nameStationPc': '46E2ST10', 'Station': 'ST10', 'ID_Station': 669, 'Measure': ['Location_of_Difuzor_1', 'Location_of_Difuzor_2', 'Photoprism_value', 'Sticking_force', 'Camera_Top_Left', 'Camera_Bott_Left', 'Camera_Bottom_']}, {'assyName': 'MQB2', 'projectName': 'MQB', 'nameStationPc': '46E2ST20', 'Station': 'ST20', 'ID_Station': 670, 'Measure': ['PCB_Position_Left', 'PCB_Position_Right', 'Clipping_LR', 'Clipping_LF', 'Clipping_RR', 'Clipping_RF', 'Camera_Connector_Angle', 'Camera_2_Flat_cable_Angle', 'Camera_2_Flat_cable_Top', 'Camera_2_Flat_cable_Bottom']}, {'assyName': 'MQB2', 'projectName': 'MQB', 'nameStationPc': '46E2ST30', 'Station': 'ST30', 'ID_Station': 671, 'Measure': ['Mask_Clip_LF', 'Mask_Clip_RF', 'Mask_Clip_RR', 'Mask_Clip_LR', 'Force_of_left_supply', 'Force_of_right_supply', 'Force_of_middle_supply']}, {'assyName': 'MQB2', 'projectName': 'MQB', 'nameStationPc': '46E2ST40', 'Station': 'ST40', 'ID_Station': 672, 'Measure': ['ST2_Force_Temp_MAX', 'ST2_Height_Temp_g', 'ST2_Angle_of_pointer_press_Temp', 'ST2_Force_Fuel_MAX', 'ST2_Height_Fuel_g', 'ST2_Angle_of_pointer_press__Fuel', 'ST3_Force_Speed_MAX', 'ST3_Height_Speed_g', 'ST3_Angle_of_pointer_press__Speed', 'ST3_Force_RPM_MAX', 'ST3_Height_RPM_g', 'ST3_Angle_of_pointer_press__RPM', 'Delta_of_small_pointers_hight', 'Delta_of_big_pointers_hight']}, {'assyName': 'MQB2', 'projectName': 'MQB', 'nameStationPc': '46A2ST60', 'Station': 'ST60', 'ID_Station': 673, 'Measure': ['Mask_Clip_Down_Left', 'Mask_Clip_Down_Right', 'Mask_Clip_Up_Left', 'Mask_Clip_Up_Right', 'Screwing_Torque_Result_3', 'Screwing_Torque_Result_4', 'Screwing_Torque_Result_1', 'Screwing_Torque_Result_2', 'Screw_Hight_LeftDown', 'Screw_Hight_RightDown', 'Screw_Hight_LeftUp', 'Screw_Hight_RightUp']}]]
        
    #run(lines_array, 'ADD JAN.GRAF@MARELLI.COM TO THE MQB2 11')
    
    #run(lines_array, 'zisti vsetko o ST40 MQB1')
    #run(lines_array, 'HOW ARE YOU?')
    #run(lines_array, 'SHOW DATA CPK CW 33 SHI')
    #run(lines_array, 'Čau, pridaj ma prosím ťa do projektu MQB1. Diky')
    #robbery_sj()
    #start_timer_all = perf_counter()
    #scraping_sj()
    #manual_pos()
    #end_timer_all = perf_counter()
    #print('[TIME] {} s'.format(format((end_timer_all - start_timer_all),'.2f')))    
       