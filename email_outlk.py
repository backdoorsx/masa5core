import win32com.client as win32
import pythoncom
import os
import json

# vytvor json subor pre uzivatelov(email) s ktorymi sa bude komunikovat
# na zaciatku sa vytvory iba jeden uzivatel(email) s pravami ROOT.
# vytvori sa prva email sprava pre roota.
def create_file_address(jfile, root):
    
    data_address = {
        'ROOT' : [root]
    }
    
    json_object = json.dumps(data_address, indent = 4) # Serializing json 
      
    # ----- Writing to json file
    try:
        with open(jfile, "w") as outfile:
            outfile.write(json_object)
        print('[+] Create file: {}!'.format(jfile))
        
        msg = '<h2>Hi {}</h2>'.format(str(root.split('.')[0].upper()))
        msg += '<p>welcome in <b>MASA</b> - Statistical process control (SPC) is a method of quality control which employs statistical methods to monitor and control a process.<p/>'
        msg += '<p>You are root, you can carry out all actions of the superuser account.<br>'
        msg += 'Account for root is save in the json file and can by changed manualy or you can delete the file and restart to default.<p/>'
        msg += '<p>Curret file: {}<p/>'.format(jfile)
        msg += '<p>This json file is update by me! '
        msg += 'The first object in file serves the root. Other objects are assy lines. Who is assigned to which assy line.<br>'
        msg += 'Write me an email to add and write to the subject.<p/>'
        
        msg += '<h3>SPC tests:</h3>'
        msg += '<p>'
        msg += 'Every 120 seconds, data is loaded from the database and is tested for these tests: <br>'
        msg += '/* TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV */<br>'
        msg += '/* TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole */<br>'
        #patern 1 = "01010101010101"
        #patern 2 = "10101010101010"
        # # VYTVOR STRING z nameranych dat z postupnostou 0 alebo 1
        # for m in range(len(data)-1):
        #  if data[m+1] > data[m]:
        #   up_down += "0"
        #  elif data[m+1] < data[m]:
        #   up_down += "1"
        #  else:
        #   up_down += "2"
        # # NAJDI PATERNy vo vytvorenem stringu
        #data_quarter = data[start_position:end_position]
        # (abs(min(test2_quarter))+abs(max(test2_quarter))) > ((abs(lim_min)+abs(lim_max))/4)
        msg += '/* TEST 3 : 6 po sebe iducich bodov klesa alebo stupa */<br>'
        msg += '/* TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL */<br>'
        msg += '/* TEST 5 : 6 bod po sebe iducich ma rovnaku hodnotu */<br>'
        msg += '/* TEST 6 : ziadny z 8 po sebe iducich bodov nelezi v pasme C */<br>'
        msg += '<br>'
        msg += 'The data sample size is default 50.'
        msg += '<b>We want to know every single piece. No losses and no filters!</b>'        
        #msg += 'In progress: /* TEST A : data za posledne 4 tyzdne : padajuce alebo stupajuce meranie */'
        msg += '<p/>'

        msg += '<h3>Data of line:</h3>'
        msg += '<p>'
        msg += 'The first time you run the program, a file is generated SAMPLES.line<br>'
        msg += 'The file type is json. One file must be created for each assy line.<br>'
        msg += 'The file will contain machines and measurements data.<br>'
        msg += 'Data of lines, stations and available measurements you get if you write me an email and write to the subject DATA OF LINES or something like this.<br>'
        msg += 'Example for MQB1 SHIELD station :<br>'
        msg += '<span style="color:black">[	<br>'
        msg += '<span style="color:black">&nbsp;&nbsp;{ <br>'
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"assyName": <span style="color:mediumblue">"MQB1",<br>'
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"projectName": <span style="color:mediumblue">"SMT1",<br>'
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"nameStationPc": <span style="color:mediumblue">"46E1SHI1",<br>'
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"Station": <span style="color:mediumblue">"SHI",<br>'
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"ID_Station": <span style="color:mediumblue">598,<br>'
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"Measure": <span style="color:black">[<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F0",<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F1",<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F2",<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F2_Zmax"<br>'
        msg += '<span style="color:black">&nbsp;&nbsp;&nbsp;&nbsp;]<br>'
        msg += '<span style="color:black">&nbsp;&nbsp;}<br>'
        msg += '<span style="color:black">]	<br>'
        msg += '</span>'
        msg += '<p/>'
        
        msg += '<p>'
        msg += '<h5>About "assyName":</h5>'
        msg += '&nbsp;&nbsp;The name of assyembly line. Should be the same as the file name.<br>'
        msg += '&nbsp;&nbsp;It serves only as a mark<br> '
        msg += '<p/>'

        msg += '<p>'
        msg += '<h5>About "Station":</h5>'
        msg += '&nbsp;&nbsp;The name of station.<br>'
        msg += '&nbsp;&nbsp;It serves only as a mark<br> '
        msg += '<p/>'

        msg += '<p>'
        msg += '<h5>About "ID_Station":</h5>'
        msg += '&nbsp;&nbsp;The unique ID of station in databese.<br>'
        msg += '&nbsp;&nbsp;This ID is find by the request to find the station<br>'
        msg += '&nbsp;&nbsp;Requrement procedure for finding stations ID:<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Send email with Subject: DATA OF LINES<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Returns a list of line IDs:<br>'
        msg += '<samp>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ID &nbsp;&nbsp;&nbsp; NAME &nbsp;&nbsp;&nbsp; DESCRIPTION<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 - BMW_1 (BMW line 1)<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2 - BMW_2 (BMW line 2)<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3 - BMW_3 (BMW line 3)<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4 - NSF (NSF line)<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...<br>'
        msg += '</samp>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Send email with Subject: DATA OF ASSY ID_LINE '
        msg += '<span style="color:orange">ID_OF_LINE<br>'
        msg += '<span style="color:black">'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Returns a list of station IDs:<br>'
        msg += '<samp>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ID &nbsp;&nbsp;&nbsp; NAME &nbsp;&nbsp;&nbsp; DESCRIPTION_IP<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;811 - PORSCHE-MAGELAN (10.129.34.38 )<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;823 - PORSCHE-ST95 (10.129.34.35 )<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;835 - DESKTOP-KM4Q6GO (10.129.34.40 )<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...<br>'
        msg += '</samp>'
        msg += '<p/>'
        
        msg += '<p>'
        msg += '<h5>About "Measure":</h5>'
        msg += '&nbsp;&nbsp;List of measurement names.<br>'
        msg += '&nbsp;&nbsp;The measurement name can be found in the datalog or request to find it.<br>'
        msg += '&nbsp;&nbsp;Requrement procedure for finding measurement names:<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Send email with Subject: DATA OF ASSY ID_BENCH '
        msg += '<span style="color:orange">ID_OF_BENCH<br>'
        msg += '<span style="color:black">'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Returns a list of measurement names on station:<br>'
        msg += '<samp>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Screw08_Depth<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Screw09_Torque<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Screw09_Heigth<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Screw07_Torque<br>'
        msg += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...<br>'
        msg += '</samp><br>'
        msg += '<p/>'
        
        msg += '<p>'
        msg += '<h5>About SKIP "Measure":</h5>'
        msg += '&nbsp;&nbsp;Skip any measure test.<br>'
        msg += '&nbsp;&nbsp;A key string is simply added after the measurement name <span style="color:red">::skip <span style="color:black">.<br>'
        msg += '&nbsp;&nbsp;Example for skip TEST1 and TEST3 for measure F1:<br> '
        msg += '<span style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;"Measure": <span style="color:black">[<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F0",<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F1::skip13",<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F2",<br>'
        msg += '<span style="color:mediumblue">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"F2_Zmax"<br>'
        msg += '<span style="color:black">&nbsp;&nbsp;&nbsp;&nbsp;]<br>'
        msg += '<span style="color:black">&nbsp;&nbsp;}<br>'
        msg += '<span style="color:black">]<br>'
        msg += '</span>'
        msg += '<p/>'
        
        # pridat ::filter
        # filter stahuje 2x viac dat pretoze je mozne ze vo vzorke 50pcs bude iba polovica jednej referencie.
        # z databazi sa stahuju data pre celu stanicu
        
        send([root], 'Welcome Root!', msg, [])
        return False
    except:
        print('[-] Failed create file: {}!'.format(jfile))
        return True


# nacitaj json subor z uzivatelmi
# funkcia vracia dict
def get_address(jfile):

    data_address = {}
    
    try:
        with open(jfile, 'r') as f:
            data_address = json.load(f)
    except:
        print('[-] Failed read file: {}!'.format(jfile))    
            
    print(data_address)
    
    return data_address
    

# pridaj do json zoznamu uzivatela(email)
# adresa uzivatela je priradena pod dany projekt
def add_address(jfile, assy, person):
    # load json
    data_address = get_address(jfile)
    
    # write json
    try:
        data_address[assy]
    except KeyError:
        data_address.update({assy:[]})
        
    data_address[assy].append(person)
    print(data_address)
     
    # save json
    with open(jfile, 'w') as json_file:
        json.dump(data_address, json_file, indent=4, separators=(',',': '))
        

# vymaz uzivatela(email) zo zoznamu z daneho projektu
def del_address(jfile, assy, person):
    # load json
    data_address = get_address(jfile)
    
    # delete item
    try:
        data_address[assy].remove(person)
        print(data_address)    
    
        # save json
        with open(jfile, 'w') as json_file:
            json.dump(data_address, json_file, indent=4, separators=(',',': '))
    except ValueError:
        print('[-] email_outlk: deleting not exist person {} | {}'.format(assy, person))
    

# posli email
# vytvor objekt mail a pouzi outlook API
# vstup do funkcie je pole emailov, subjekt emailu, sprava v emaile, pole priloh
def send(address, subject, msg, attach): # (ARRAY_OF_ADDRESS, STRING, STRING, ARRAY_OF_FILE_PATH)
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    
    address_list = ''
    
    for a in address:
        address_list += a
        address_list += ';'    
    
    mail.To = address_list
    mail.Subject = subject
    mail.Body = 'Message body'

    mail.HTMLBody = msg

    if len(attach) != 0: #To attach a file to the email
        for a in attach:
            mail.Attachments.Add(a)

    mail.Send()
    print('[EMAIL] to: {}'.format(address))
    print('[+] Send email OK')


# citaj email a presun do kosa
# vytvor objekty inbox a delete s outlook API
# email objekt musi byt klasifikovany pod cislom 43 a typom EX
# funkcia vracia dict
def read():
    
    #https://docs.microsoft.com/en-us/office/vba/api/outlook.olobjectclass
    print('[+] Reading email...')
    sender = ''
    name_sender = ''
    subject = ''
    body = ''
    pythoncom.CoInitialize()
    outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # "6" refers to the index of a folder - in this case, the inbox.
                                        #3  Deleted Items
                                        #4  Outbox
                                        #5  Sent Items
                                        #6  Inbox
                                        #9  Calendar
                                        #10 Contacts
                                        #11 Journal
                                        #12 Notes
                                        #13 Tasks
                                        #14 Drafts
    out_delete = outlook.GetDefaultFolder(3)
    
    messages = inbox.Items
    if messages[len(messages)-1].Class == 43: #  MailItem object that represents a new mail message.
        if messages[len(messages)-1].SenderEmailType == 'EX':
            sender = messages[len(messages)-1].Sender.GetExchangeUser().PrimarySmtpAddress
            name_sender = messages[len(messages)-1].SenderName
        else:
            sender = messages[len(messages)-1].SenderEmailAddress
            name_sender = messages[len(messages)-1].SenderName
            
        subject = messages[len(messages)-1].Subject
        body = messages[len(messages)-1].Body
        body = body.replace('\n','^')
        body = body.replace('\r','*')
        body = body.replace('*^*^',' ')
        body = body.replace('  ','')
        #body = body.upper()
        if len(body) > 2048:
            body = body[:2048]        
        
    
    print('[+] Email read: name={} address={} Subject={} body={}'.format(name_sender, sender, subject, body))
    
    ret = {'name_sender': name_sender, 'sender': sender, 'subject': subject, 'body': body}
    #messages[len(messages)-1].move(out_delete)
    
    return ret

