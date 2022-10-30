# MASA5CORE
# LICENSE: WTFPL
# 
#                              The Tree of Life
#                                     |
#           +-------------------------+-------------------------+
#           |                                                   |
#      INFINITY LOOP thread main                           INFINITY LOOP thread fifth
#    1. SQL connection                                1. Check email
#    2. If timer FTQ & Fails                          2. Run NLP Natural language procesing
#    3. Run SPC                                       3. If CPK, FTQ, PLT...
#    4. SQL close connection                          4. Sleep timer
#    5. Sleep timer
#    6. Check is alive fifth
#
# 1. Current spc test (1-F):
#    TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV
#    TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole
#    TEST 3 : 6 po sebe iducich bodov klesa alebo stupa
#    TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL
#    TEST 5 : 6 bod po sebe iducich ma rovnaku hodnotu
#    TEST 6 : ziadny z 8 po sebe iducich bodov nelezi v pasme C

# COMPILATION:
# CD C:\Users\f93918b\Documents\python\MASA5core>
# pyinstaller.exe --clean --onefile main_cli_v5x02.py --name masa5core.exe --icon masa_icon_320.ico

import os
import sys
import fnmatch
import numpy as np
import math
import random
from time import localtime, sleep, time, perf_counter
from functools import partial
import datetime
from decimal import Decimal
import re
import hashlib
from operator import itemgetter, attrgetter
import threading

# --- MAIL ---
import win32com.client as win32
import pythoncom

# --- EXCEL ---
#from openpyxl import Workbook
#from openpyxl.styles import PatternFill
#from openpyxl.styles.borders import Border, Side, BORDER_THIN
#from openpyxl.styles import Alignment
# #from openpyxl import load_workbook
# #from openpyxl.styles import colors
# #from openpyxl.styles import Font, Color, Fill, PatternFill, GradientFill

# --- COPY ---
import shutil

# --- JSON ---
import json

# --- SQL DB ---
#import sqlite3

# --- MATPLOTLIB ----
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# --- Garbage Collector interface ---
import gc

# --- THREAD ---
import threading

# --- MY MODULS ---
import sql_db
import email_outlk
import nlu1

def main(nameOfthread, lines_array, jfile, v2):
    global spc_running
    global how_much
    
    while True:
    
        print('[+] run...')
        main_start_timer = perf_counter()
        
        # ----- OPEN SQL connection
        conn, cursor = sql_db.connection_sql()
    
        only_pass = 'True' # 'False'/'True'/''
        run_all = 2 # 0 = jedna stanica, 1 = cela linka, 2 = vsetko
        run_line = 'PORSCHE'
        run_station = 'ST20'
        print(lines_array)
        print(len(lines_array))
        run_spc(cursor, lines_array, only_pass, run_all, run_line, run_station, StartTime, StopTime)

        # ----- close sql connection
        cursor.close()
        conn.close()
    
        main_end_timer = perf_counter()
        how_much += 1
        print('[+] Done {}s | {} | count={}\n\n'.format(format((main_end_timer - main_start_timer),'.2f'), datetime.datetime.now(), how_much))
    
        sequnce_time_data.append(format((main_end_timer - main_start_timer),'.2f'))
    
        debug_main_function = True
    
        if debug_main_function:
            f = open("debug_main_function.log", "a")        
            f.write('\n')
            f.write('[+] Done {}s | {} | count={}\n'.format(format((main_end_timer - main_start_timer),'.2f'), datetime.datetime.now(), how_much))
            f.write('sequnce_time_data={}\n'.format(sequnce_time_data))
            f.write('data_all_spc={}\n'.format(data_all_spc))
            f.write('[gc] get_count={}\n'.format(gc.get_count()))  #(youngest generation, objects in the next generation,object in the oldest generation)
            f.close()

        sleep(uptime) # waiting    
    
    


def fifth(nameOfthread, lines_array, jfile, v2):
    
    global spc_running
    global how_much
    
    CPK__ = 0
    FTQ__ = 0
    PLT__ = 0
    ONE__ = 0
    ADD__ = 0
    DEL__ = 0
    SQL__ = 0
    INF__ = 0
    SKP__ = 0
    VNC__ = 0 # pip3 install vncdotool
    
    # requred CPK__:
    only_pass = 'True' # 'False'/'True'/''
    run_all = 1 # 0 = jedna stanica, 1 = cela linka, 2 = vsetko
    run_line = ''
    run_station = ''
    
    # requred FTQ__:
    ftq_run_all = 1 # 0 = jedna stanica, 1 = cela linka, 2 = vsetko
    ftq_run_line = 'MQB1'
    ftq_run_station = 'ST30'      
    
    # requred:
    w_l, StartTime_l, StopTime_l = week_last(0) # predchadajuci week 7
    print('week={} {} - {}'.format(w_l, StartTime_l, StopTime_l))
    #StartTime_l = '2022-04-26 08:00'
    #StopTime_l = '2022-04-26 23:59'
    #print(StartTime_l)
    #print(StopTime_l)
    Top = 0
    
    # calculate when input is week
    #my_week = 35
    #set_week = w - my_week
    #w, StartTime_l, StopTime_l = week_last(set_week) # predchadajuci week 7
    #print('week={} {} - {}'.format(w, StartTime_l, StopTime_l))    
    
    
    # HTML STYLE for email
    style0 = 'style="border: 1px solid black; border-collapse: collapse; width:50%"'
    style1 = 'style="border: 1px solid black; border-collapse: collapse"'
    #style2 = 'style="border: 1px solid black; border-collapse: collapse;background-color: #96D4D4"'
    style2 = 'style="border: 1px solid black; border-collapse: collapse; background-color: #00baff"'
    style3 = 'style="border: 1px solid black; border-collapse: collapse; width:100%"'
    
    
    
    while True:
        
        welcome = '' # string for save new email
        fifth_start_timer = perf_counter()
        ai = 0
        CON__ = 0
        
        # ----- Vytvor zoznam ludi z address.json
        try:
            people = []
            address_data = email_outlk.get_address(jfile)
            
            for p in address_data:
                people.append(address_data[p])

            people = [person for sublist in people for person in sublist] # Flatten, spoji 2D list do jedneho
        except:
            people = []
            print('[!] Error: email_outlk.get_address(jfile)')
    
        # ----- Precitaj najnovsi email
        try:
            data_email = email_outlk.read() # {'name_sender': name_sender, 'sender': sender, 'subject': subject, 'body': body}
        except:
            data_email = {'name_sender': '', 'sender': '', 'subject': '', 'body': ''}
            print('[!] Error: email_outlk.read()')
    
        print(data_email['sender'].lower())             # Celu adresu prevedie na male znaky
        
        if data_email['sender'].lower() in people:      # Ak sa nachadza sender v zozname address.json
            send_to_address = []                                    # vytvory/vyprazdni pole
            send_to_address.append(data_email['sender'].lower())    # ulozi do pola emailovu adresu pre odoslanie spravy
            
            nlp_subject, nlp_tags = nlu1.run(lines_array, data_email['subject'])
            print(nlp_subject)
            print(nlp_tags)
            
            
            # ----- TEST NA SKIP SPC TESTU
            #desus = data_email['subject'].upper().split(' ')        # vytvory posle slov zo subject v emaile
            score_ = 0
            for gram1 in nlp_subject:
                if gram1 in ['skip', 'the', 'test', 'test1']:
                    score_ += 1
            if score_ >= 3:
                SKP__ = 1              
            
            # ----- TEST NA INFO OKOLO MASA
            #desus = data_email['subject'].upper().split(' ')        # vytvory posle slov zo subject v emaile
            score_ = 0
            for gram1 in nlp_subject:
                if gram1 in ['how', 'are', 'you', 'what', 'is', 'spc', 'masa', 'masa5core', 'welcome']:
                    score_ += 1
            if score_ >= 3:
                ONE__ = 1            
            
            # ----- TEST NA DATA LINIEK A STOJOV Z SQL
            #desus = data_email['subject'].upper().split(' ')        # vytvory posle slov zo subject v emaile
            score_ = 0
            for gram1 in nlp_subject:
                if gram1 in ['data', 'of', 'line', 'lines', 'find', 'assy', 'st', 'station', 'info', 'about']:
                    score_ += 1
            if score_ >= 3:
                SQL__ = 1
                
            # ----- TEST NA PRIDANIE ALEBO ODOBRANIE ZO ZOZNAMU
            #desus = data_email['subject'].upper().split(' ')        # vytvory posle slov zo subject v emaile
            score_ = 0
            for gram1 in nlp_subject:
                if gram1 in ['add', 'me', 'to', 'list', 'del', 'delete', 'remove', 'from', 'for', 'the', 'project', 'line', 'assy']:
                    score_ += 1
            if score_ >= 3:
                ADD__ = 1
                
            # ----- TEST NA CPK
            #desus = data_email['subject'].upper().split(' ')        # vytvory posle slov zo subject v emaile
            score_ = 0
            for gram1 in nlp_subject:
                if gram1 in ['show', 'data', 'cpk', 'cw']:
                    if gram1 == 'cpk':
                        score_ += 1
                    score_ += 1
            if score_ >= 3:
                CPK__ = 1
                
            # ----- TEST NA FTQ
            #desus = data_email['subject'].upper().split(' ')        # vytvory posle slov zo subject v emaile
            score_ = 0
            for gram1 in nlp_subject:
                if gram1 in ['show', 'data', 'ftq', 'cw']:
                    if gram1 == 'ftq':
                        score_ += 1                    
                    score_ += 1
            if score_ >= 3:
                FTQ__ = 1
        
            # ----- TEST NA ZOZNAM MIC V EMAILE
            #if data_email['subject'].upper() in ['BODY L9', 'PORSCHE', 'RE: BODY L9', 'RE: PORSCHE']:
            #    print('yeeeeeeeeeees')
            #    sleep(3)
            #    rovnake4zasebou = 0 
            #    for n in range(len(nlp)-1):
            #        if len(nlp[n]) == len(nlp[n+1]) and len(nlp[n]) == 12: # velkost slova je rovnaka ako nasledujuce a ma velkost 12
            #            rovnake4zasebou += 1
            #            if rovnake4zasebou >= 4:
            #                CON__ = 1 # continuity
            #        else:
            #            rovnake4zasebou = 0
            
    
        #print('sleeping...')
        #sleep(10000)
        msg = ''
        subject = ''
        # ------------------------------------------------------------------------------------------------------------------------------
        if ONE__:
            ai = 1
            ONE__ = 0
            
            msg = '<h2>Hi {}</h2>'.format(str(data_email['sender'].split('.')[0].upper()))
            msg += '<p>welcome in <b>MASA</b> - Statistical process control (SPC) is a method of quality control which employs statistical methods to monitor and control a process.<p/>'
            msg += '<h3>SPC tests:</h3>'
            msg += '<p>'
            msg += 'Every {} seconds, data is loaded from the database and is tested for these tests: <br>'.format(str(uptime))
            msg += '/* TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV */<br>'
            msg += '/* TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole */<br>'
            msg += '/* TEST 3 : 6 po sebe iducich bodov klesa alebo stupa */<br>'
            msg += '/* TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL */<br>'
            msg += '/* TEST 5 : 6 bod po sebe iducich ma rovnaku hodnotu */<br>'
            msg += '/* TEST 6 : ziadny z 8 po sebe iducich bodov nelezi v pasme C */<br>'
            msg += '<br>'
            msg += 'The data sample size is default 50. Current is {}<br>'.format(str(amount_of_data))
            msg += '<b>We want to know every single piece. No losses and no filters!</b>'
            # LIST OF LINES
            # USED SKIP AND FILTERS
            
        # ------------------------------------------------------------------------------------------------------------------------------
        if SQL__:
            ai = 1
            SQL__ = 0
            
            # ----- OPEN SQL connection
            conn_l, cursor_l = sql_db.connection_sql()
            
            if 'id_line' in nlp_subject: # najde 'ID_LINE' v hlavicke mailu
                for gram1 in nlp_subject:
                    if gram1.isnumeric():                
                        ID_ = int(gram1)
                        break
                    
                list_of_bench = sql_db.find_stations(cursor_l, ID_)
                
                subject = 'Stations from SQL'
                msg = ''
                msg += '<samp>'
                msg += '&nbsp; ID &nbsp;&nbsp;&nbsp; NAME &nbsp;&nbsp;&nbsp; IP<br>'
                for i in list_of_bench:
                    if len(i) > 7:
                        msg += str(i[0]) + ' - ' + str(i[6]) + ' (' + str(i[7]) + ')<br>'
                    
                msg += '</samp>'
                msg += '<p>Next step for more info about the station:</p>'
                msg += '<p> Example in subject:<br>DATA OF ASSY ID_BENCH 819</p>'                
                
                
            elif 'id_bench' in nlp_subject: # najde 'ID_BENCH' v hlavicke mailu
                for gram1 in nlp_subject:
                    if gram1.isnumeric():                
                        ID_ = int(gram1)
                        break
                    
                list_of_bench = sql_db.find_measures(cursor_l, ID_)
                
                subject = 'Measures from SQL'
                msg = ''
                msg += '<samp>'
                msg += '&nbsp; Measures:<br>'
                for i in list_of_bench:
                    msg += str(i[0]) + '<br>'
                    
                msg += '</samp>'                
            
            else:
                list_of_lines = sql_db.find_assy(cursor_l)
                
                subject = 'Line from SQL'
                msg = ''
                msg += '<samp>'
                msg += '&nbsp; ID &nbsp;&nbsp;&nbsp; NAME &nbsp;&nbsp;&nbsp; DESCRIPTION<br>'
                for i in list_of_lines:
                    msg += str(i[0]) + ' - ' + str(i[1]) + ' (' + str(i[2]) + ')<br>'
                    
                msg += '</samp>'
                msg += '<p>Next step for more info about the assy line:</p>'
                msg += '<p> Example in subject:<br>DATA OF ASSY ID_LINE 74</p>'
            
            
            # ----- close sql connection
            cursor_l.close()
            conn_l.close()            
        
        # ------------------------------------------------------------------------------------------------------------------------------
        if CON__:
            ai = 1
            CON__ = 0
            
            MIC_LIST = []
            for n in range(len(nlp)-1):
                if len(nlp[n]) == len(nlp[n+1]) and len(nlp[n]) == 12: # velkost slova je rovnaka ako nasledujuce a ma velkost 12
                    MIC_LIST.append(nlp[n].upper())
                elif len(MIC_LIST) >= 4 and len(nlp[n]) == 12 and len(nlp[n+1]) != 12: # posledne MIC ak idu za sebou je ak uz nie je prazdny MIC_LIST a dalsie slovo nema 12 znakov tak zapise a zastavy for
                    MIC_LIST.append(nlp[n].upper())
                    break

            if len(MIC_LIST) >= 4:
                #mic_continuity.run(MIC_LIST, data_email['subject'])
                sql_db.get_continuity_MIC(MIC_LIST)
            
            print(MIC_LIST)
            print('[+] CON__')
        
        # ------------------------------------------------------------------------------------------------------------------------------
        if CPK__ or PLT__:
            ai = 1
            CPK__ = 0
            
            cw = int(w_l) # aktualny tyzden ako defaultny
            
            #data_email_subject = data_email['subject']
            #nlp_subject, nlp_tags = nlu1.run(lines_array, data_email_subject)            
            
            # NAJDE CPK
            if 'cpk' in nlp_subject:
                
                # NAJDE CW S CISLOM
                if 'cw' in nlp_subject:
                    
                    for gram1 in nlp_subject:
                        if gram1.isnumeric():
                            if int(gram1) <= int(w_l) and int(gram1) >= 1:
                                cw = int(gram1)
                                # calculate when input is week
                                set_week = w_l - cw
                                w_l, StartTime_l, StopTime_l = week_last(set_week) # predchadajuci week 7                                
                                #break
                else: # ak nenajde osamotene 'CW' lebo je spojene z cislom alebo znakom
                    for gram1 in nlp_subject:
                        if len(gram1) > 2: # CWnieco
                            if gram1[0] == 'c' and gram1[1] == 'w':
                                gram1_split = gram1.split('cw') # Ex:['', '39'] Ex:['', '=32']
                                if len(gram1_split) >=2:
                                    gram1 = gram1_split[-1] # uloz posledny prvok
                                    gram1_clean = gram1.replace('=', '')
                                    gram1_clean = gram1_clean.replace('.', '')
                                    gram1_clean = gram1_clean.replace('-', '')
                                    if gram1_clean.isnumeric():
                                        cw = int(gram1_clean)
                                        # calculate when input is week
                                        set_week = w_l - cw
                                        w_l, StartTime_l, StopTime_l = week_last(set_week) # predchadajuci week 7                                             
                                        #break
                
 
                # NAJDI LINKU
                for tag in nlp_tags: 
                    if isinstance(tag, list):
                        if tag[0][9] == 11: # na pozicii 9 sa nachadza classification. EX:[(2256, 2256, 17597, 'mqb2', 'mqb2', 'podstatné', 1, 0.0, 0.0, 11.0, 0.0)]
                            run_line = tag[0][4].upper() # na pozicii je string UTF8 lower case
                            run_all = 1 #0 = jedna stanica, 1 = cela linka, 2 = vsetko
                            run_station = ''
                            
                # NAJDI STANICU
                # AKO BUDE HLADAT STANICU ZO ZOZNAMU ALEBO Z DB?
                
            print('cw={} | w_l={} | run_line={}'.format(cw, w_l, run_line))
            print('----')
            
            #input('CW >')
            
            if run_line != '' and run_all == 1 and run_station == '':
                
                msg = '<p>[+] Getting cpk data from {} Week: {} from: {} - to: {}<p/>'.format(run_line, w_l, StartTime_l, StopTime_l)
                msg += '<p> Please wait a moment...<p/>'
                
                email_outlk.send(send_to_address, 'CPK Status', msg, []) # SEND EMAIL ABOUT STATUS
                
                msg = '<h3> Week: {} from: {} - to: {}</h3>'.format(w_l, StartTime_l, StopTime_l)
                        
                
                
                # ----- OPEN SQL connection
                conn_l, cursor_l = sql_db.connection_sql()
        
                final_data = [] # [ASSY, STATION, [MDATA]]
            
                #only_pass = 'True' # 'False'/'True'/''
                #run_all = 1 # 0 = jedna stanica, 1 = cela linka, 2 = vsetko
                #run_line = 'MQB1'
                #run_station = 'SHI'
            
                print('{} - {}'.format(StartTime_l, StopTime_l))
            
                for i in range(len(lines_array)):
                    print('THREAD 2 ================================================================================================')
                
                    for j in range(len(lines_array[i])):
                    
                        if (lines_array[i][j]['assyName'] == run_line and lines_array[i][j]['Station'] == run_station and 
                            run_all == 0) or (lines_array[i][j]['assyName'] == run_line and run_all == 1) or run_all == 2:
                        
                            #Top = amount_of_data*(len(lines_array[i][j]['Measure'])) # pocet kusov krat pocet merani.
 
                            print(' {} - {} - {} - {}'.format(lines_array[i][j]['assyName'], lines_array[i][j]['Station'], lines_array[i][j]['ID_Station'], lines_array[i][j]['Measure'] ))

                            mdata = get_spc_data(cursor_l, only_pass, lines_array[i][j]['assyName'], lines_array[i][j]['Station'], lines_array[i][j]['ID_Station'], Top, lines_array[i][j]['Measure'], StartTime_l, StopTime_l) # SQL
                            final_data.append([lines_array[i][j]['assyName'], lines_array[i][j]['Station'], mdata])            
            
        
                # ----- close sql connection
                cursor_l.close()
                conn_l.close()
            
                        
                style = style1
            
                msg += '<br>'
                msg += '<table {}>'.format(style0)
                msg += '<tr {}>'.format(style)
                msg += '<th {}> ASSEMBLY </th>'.format(style)
                msg += '<th {}> STATION </th>'.format(style)
                msg += '<th {}> MEASURE </th>'.format(style)
                msg += '<th {}> CPL </th>'.format(style)
                msg += '<th {}> CPU </th>'.format(style)
                msg += '<th {}> CPK </th>'.format(style)
                msg += '</tr>'            
            
                for i in final_data:
                    print('')
                    style = style2
                    for j in range(len(i[2])):
                        if len(i[2][j][5]) > 0:
                            print('ASSY={} ST={} MEASURE={} CPK={} CPL={} CPU={}'.format(i[0], i[1], i[2][j][0], i[2][j][5][3], i[2][j][5][4], i[2][j][5][5])) # assy, st, measure, cpk, cpl, cpu
                        
                            msg += '<tr {}>'.format(style)
                            msg += '<td {}>{}</td>'.format(style, i[0])
                            msg += '<td {}>{}</td>'.format(style, i[1])
                            msg += '<td {}>{}</td>'.format(style, i[2][j][0])
                            msg += '<td {}>{}</td>'.format(style, format(i[2][j][5][4], '.3f')) #CPL
                            msg += '<td {}>{}</td>'.format(style, format(i[2][j][5][5], '.3f')) #CPU
                            msg += '<td {}>{}</td>'.format(style, format(i[2][j][5][3], '.3f')) #CPK
                            msg += '</tr>'                          
                        else:
                            print('ASSY={} ST={} MEASURE={} CPK=0.0 CPL=0.0 CPU=0.0'.format(i[0], i[1], i[2][j][0]))
                        
                            msg += '<tr {}>'.format(style)
                            msg += '<td {}>{}</td>'.format(style, i[0])
                            msg += '<td {}>{}</td>'.format(style, i[1])
                            msg += '<td {}>{}</td>'.format(style, i[2][j][0])
                            msg += '<td {}>NaN</td>'.format(style) #CPL
                            msg += '<td {}>NaN</td>'.format(style) #CPU
                            msg += '<td {}>NaN</td>'.format(style) #CPK
                            msg += '</tr>'
                        style = style1


                msg += '</table>'
                subject += ' CPK'
            else:
                msg += '<p>missing the name of assembly line or not exist in database!<br>'
                msg += 'If not exist in database you can create it.<br>'
                msg += 'Curret files of assy lines : {}<p/>'.format(line_files)
            
                #email_outlk.send(["jan.graf@marelli.com"], 'CPK', msg, [])
            
            # --------------------------------------------------------------------------------------------------------------------------
            if PLT__:
                PLT__ = 0
                # ----- SPUST KONTROLU
                print('[+] Runing spc...')
                for a in final_data:
                    for b in range(len(a[2])):
                        #print('{} | {} | {}'.format(a[0], a[1], a[2][b])) # ex: MQB1 | ST20 | ['Camera_3_Flat_cable_Top', [0.905, 0.882,......
                        if len(a[2][b][1]) > 1:
                            
                            #spc(a[0], a[1], a[2][b]) # spc(assy, station, mdata)
                            assy = a[0]
                            station = a[1]
                            mdata = a[2][b]
                            name_measure = str(mdata[0])
                            name_measure = name_measure.upper() # NAZOV MERANIA NA VELKE PISMENA
                            status = [False, False, False, False, False, False] # 6x test
                            result = []
                            lim_min = mdata[3]
                            lim_max = mdata[4]
                            ucl = mdata[5][6]
                            lcl = mdata[5][7]
                            
                            # -----------------------------------------------------------------
                            # REVERSE pole hladaj patern od najaktualnejsich dat, takze od zadu
                            # -----------------------------------------------------------------
                            reverse_mdata = mdata[1].copy() # pole nameranych dat
                                
                            for i in range(len(reverse_mdata) // 2):
                                reverse_mdata[i], reverse_mdata[-1-i] = reverse_mdata[-1-i], reverse_mdata[i]
                            
                            # -------------------------------------------------------------------
                            # /* TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV */
                            # -------------------------------------------------------------------
                            t1 = []
                            for m in range(len(mdata[1])):
                                if mdata[1][m] > lim_max or mdata[1][m] < lim_min:
                                    result.append('TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV')
                                    t1.append((m, mdata[1][m]))
                                    status[0] = True
                   
                            # ---------------------------------------------------------------------
                            # /* TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole */
                            # ---------------------------------------------------------------------
                            t2 = []
                            up_down = ""
                            patern_0_1 = "01010101010101"
                            patern_1_0 = "10101010101010"
                            match1 = False
                            match2 = False
                            
                            # VYTVOR STRING z nameranych dat z postupnostou 0 alebo 1
                            for m in range(len(reverse_mdata)-1):
                                if reverse_mdata[m+1] > reverse_mdata[m]:
                                    up_down += "0"
                                else:
                                    up_down += "1"
                                    
                            if up_down[-1] == '0':
                                up_down += '1'
                            else:
                                up_down += '0'
                            
                            # NAJDI PATERNy vo vytvorenem stringu
                            match1 = re.search(patern_0_1, up_down) # EX: <re.Match object; span=(3462, 3476), match='01010101010101'>
                            match2 = re.search(patern_1_0, up_down)
                            
                            if match1 or match2: # ak sa nejaky patern nasiel tak test je pozitivny        
                                if match1 and match2:
                                    start_position = min(match1.start(), match2.start())
                                    end_position = min(match1.end(), match2.end())
                                elif match1:
                                    start_position = match1.start()
                                    end_position = match1.end()
                                elif match2:
                                    start_position = match2.start()
                                    end_position = match2.end()
 
                                t2.append(len(reverse_mdata)-1-end_position) # x start, plus odpocet pre prevod z reverz naspat
                                t2.append(len(reverse_mdata)-1-start_position) # x stop, plus odpocet pre prevod z reverz naspat             
                                t2.append(mdata[1][-end_position]) # y start axes
                                t2.append(mdata[1][-start_position]) # y end axes                    
                                result.append('TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole')
                                status[1] = True
                            
                            # --------------------------------------------------------
                            # /* TEST 3 : 6 po sebe iducich bodov klesa alebo stupa */
                            # --------------------------------------------------------
                            t3 = []
                            patern_6x0 = "000000"
                            patern_6x1 = "111111"
                            match1 = re.search(patern_6x0+'*0', up_down)
                            match2 = re.search(patern_6x1+'*1', up_down)
                            
                            if match1 or match2:
                                if match1 and match2:
                                    start_position = min(match1.start(), match2.start())
                                    end_position = min(match1.end(), match2.end())
                                elif match1:
                                    start_position = match1.start()
                                    end_position = match1.end()
                                elif match2:
                                    start_position = match2.start()
                                    end_position = match2.end()

                                t3.append(len(reverse_mdata)-1-end_position) # x start, plus odpocet pre prevod z reverz naspat
                                t3.append(len(reverse_mdata)-1-start_position) # x stop, plus odpocet pre prevod z reverz naspat             
                                t3.append(mdata[1][-end_position]) # y start axes
                                t3.append(mdata[1][-start_position]) # y end axes
                                result.append('TEST 3 : 6 po sebe iducich bodov klesa alebo stupa')
                                status[2] = True
                                
                            # ------------------------------------------------------------------
                            # /* TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL */
                            # ------------------------------------------------------------------
                            t4 = []
                            for m in range(len(mdata[1])):
                                if (mdata[1][m] > ucl and mdata[1][m] < lim_max) or (mdata[1][m] < lcl and mdata[1][m] > lim_min):# and mdata[1][m] < lim_max and mdata[1][m] > lim_min:
                                    result.append('TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL')
                                    t4.append((m, mdata[1][m]))
                                    status[3] = True
                                    
                            # -------------------------------------------------------
                            # /* TEST 5 : 6 bod po sebe iducich ma rovnaku hodnotu */
                            # -------------------------------------------------------
                            t5 = []
                            counter = 1
                            stoper = 6
                            for m in range(len(reverse_mdata)-1):
                                if reverse_mdata[m] == reverse_mdata[m+1]:
                                    counter = counter+1
                                    
                                    if counter >= stoper:
                                        result.append('TEST 5 : 6 bodov po sebe iducich ma rovnaku hodnotu')
                                        status[4] = True  
                                        t5.append((len(reverse_mdata)-1-(m-stoper+2),reverse_mdata[(m-stoper+2)], stoper-1)) # prevod z revez
                                        break
                                else:
                                    counter = 1                            
                            #----------------------------------------------------------------    
                            plot(assy, station, mdata ,result, t1, t2, t3, t4, t5, ai)
                                                        
                            
                            
                print('[*] Spc done!')                
                
        
        # ------------------------------------------------------------------------------------------------------------------------------
        if FTQ__ : # treba dokoncit.
            ai = 0
            FTQ__ = 0
            # ----- OPEN SQL connection
            conn_l, cursor_l = sql_db.connection_sql()
            
            #ftq_run_all = 1 # 0 = jedna stanica, 1 = cela linka, 2 = vsetko
            #ftq_run_line = 'MQB1'#'MQB1'
            #ftq_run_station = 'ST20'
            
            #w, StartTime_l, StopTime_l = week_last(2) # predchadajuci week
            print('{} - {}'.format(StartTime_l, StopTime_l))
            
            ftqdata = []
            for i in range(len(lines_array)):
        
                for j in range(len(lines_array[i])):
            
                    start_timer = perf_counter()
            
                    if (lines_array[i][j]['assyName'] == ftq_run_line and lines_array[i][j]['Station'] == ftq_run_station and 
                        ftq_run_all == 0) or (lines_array[i][j]['assyName'] == ftq_run_line and ftq_run_all == 1) or ftq_run_all == 2:
                        print('{} - {} - {} - {}'.format(lines_array[i][j]['assyName'], lines_array[i][j]['Station'], lines_array[i][j]['ID_Station'], lines_array[i][j]['Measure'] ))
                        #[assy, station, (OutputParts-fail), fail, ftq_bench, ftq_ole, ftq_ooe, fdata]
                        ftqdata.append(get_ftq(cursor_l, lines_array[i][j]['assyName'], lines_array[i][j]['Station'],lines_array[i][j]['ID_Station'], StartTime_l, StopTime_l)) # SQL
                        print(len(ftqdata))
                
                        end_timer = perf_counter()
                        print('[TIME] {}-{} : run_ftq_and_fails = {} s'.format(lines_array[i][j]['assyName'], lines_array[i][j]['Station'], format((end_timer - start_timer),'.2f')))            
            
            # ----- close sql connection
            cursor_l.close()
            conn_l.close()
                        
            style = style1
            
            msg += '<br>'
            msg += '<table {}>'.format(style3)
            msg += '<tr {}>'.format(style)
            msg += '<th {}> ASSEMBLY </th>'.format(style)
            msg += '<th {}> STATION </th>'.format(style)
            msg += '<th {}> Pass </th>'.format(style)
            msg += '<th {}> FTQ_bench </th>'.format(style)
            msg += '<th {}> FTQ_ole </th>'.format(style)
            msg += '<th {}> FTQ_ooe </th>'.format(style)
            msg += '<th {}> TIME </th>'.format(style)
            msg += '<th {}> DEBUG </th>'.format(style)
            msg += '</tr>'              
            
            print('{} - {}'.format(StartTime_l, StopTime_l)) 
            for i in ftqdata:
                print('ASSY={} ST={} Pass={} FTQ_bench={} FTQ_ole={} FTQ_ooe={} TIME={}'.format(i[0], i[1], i[2], format(i[4], '.2f'), format(i[5], '.2f'), format(i[6], '.2f'), format(i[8], '.2f'))) # [assy, station, (OutputParts-fail), fail, ftq_bench, ftq_ole, ftq_ooe, fdata]
                
                msg += '<tr {}>'.format(style)
                msg += '<td {}>{}</td>'.format(style, i[0])
                msg += '<td {}>{}</td>'.format(style, i[1])
                msg += '<td {}>{}</td>'.format(style, i[2]) #PASS
                msg += '<td {}>{}</td>'.format(style, format(i[4], '.3f')) #FTQ_bench
                msg += '<td {}>{}</td>'.format(style, format(i[5], '.3f')) #FTQ_ole
                msg += '<td {}>{}</td>'.format(style, format(i[6], '.3f')) #FTQ_ooe
                msg += '<td {}>{}</td>'.format(style, format(i[8], '.3f')) #TIME
                msg += '<td {}>{}</td>'.format(style, i[9]) #DEBUG
                msg += '</tr>'
                
            msg += '</table>'
            subject += ' FTQ'
            
            email_outlk.send(["jan.graf@marelli.com"], 'FTQ', msg, [])
                
        # ------------------------------------------------------------------------------------------------------------------------------  
        if INF__ :
            ai = 1
            INF__ = 0
            #CONNECT OT THE SQB
            
            #DISCONNET TO EH SQL
        # ------------------------------------------------------------------------------------------------------------------------------  
        if SKP__ :
            ai = 1
            SKP__ = 0
            
            current_path = os.getcwd()
            ofile = current_path + '\\skip1'
            
            if 'skip' in nlp_subject:
                
                f = open(ofile, "a")
                f.write("TEST1 SKIP FOR ALL OF THEM")
                f.close()            
            
            subject = 'Update TEST'
            msg = '<p>Hello {},<p/>'.format(str(data_email['sender'].split('.')[0].upper()))
            msg += '<p>[+] Test 1 is skip for all of them!<p/>'
            
            #DISCONNET TO EH SQL
            
        # ------------------------------------------------------------------------------------------------------------------------------
        if ADD__ :
            ADD__ = 0
            ai = 1
            
            current_path = os.getcwd()
            jfile = current_path + '\\address.json'
            
            print(data_email['subject'])
            
            #data_email_subject += ' 12662a4b78e19ac27361b005a6dbb3d7' # prida HASH na koniec aby sa pridaly linky do db ak uz nie su.
            #data_email_subject = data_email['subject']
            #nlp_subject, nlp_tags = nlu1.run(lines_array, data_email_subject)
            #print(nlp_tags)
            #print(nlp_subject)
            
            email_person = ''
            assy = ''
            
            subject = 'Update list'
            msg = '<p>Hello {},<p/>'.format(str(data_email['sender'].split('.')[0].upper()))
            
            # NAJDI EMAIL ADRESU
            for desu in nlp_subject: 
                if len(desu.split('@')) == 2 and len(desu) < 64:
                    r = desu.split('@')[1]
                    if len(r.split('.')) == 2:
                        email_person = desu
            
            # NAJDI LINKU
            for tag in nlp_tags: 
                if isinstance(tag, list):
                    if tag[0][9] == 11: # na pozicii 9 sa nachadza classification. EX:[(2256, 2256, 17597, 'mqb2', 'mqb2', 'podstatné', 1, 0.0, 0.0, 11.0, 0.0)]
                        assy = tag[0][4].upper() # na pozicii je string UTF8 lower case
            
            
            # AK NASIEL EMAIL A LINKU
            if email_person != '' and assy != '':
                if 'add' in nlp_subject:
                    email_outlk.add_address(jfile, assy, email_person)
                    send_to_address.append(email_person)
                    # POSLI EMAIL ABOUT MASA UZIVATELOVY.
                    msg += '<p>[+] Added user {} to the project {}!<p/>'.format(email_person, assy)
                    welcome = email_person
                elif 'del' in nlp_subject:   
                    email_outlk.del_address(jfile, assy, email_person)
                    msg += '<p>[+] Remove user {} from the project {}!<p/>'.format(email_person, assy)
                elif 'delete' in nlp_subject:   
                    email_outlk.del_address(jfile, assy, email_person)
                    msg += '<p>[+] Remove user {} from the project {}!<p/>'.format(email_person, assy)
                elif 'remove' in nlp_subject:   
                    email_outlk.del_address(jfile, assy, email_person)
                    msg += '<p>[+] Remove user {} from the project {}!<p/>'.format(email_person, assy)
            else:
                
                if email_person == '':
                    msg += '<p>missing the email of person!<p/>'
                elif assy == '':
                    msg += '<p>missing the name of assembly line or not exist in database!<br>'
                    msg += 'If not exist in database you can create it.<br>'
                    msg += 'Curret files of assy lines : {}<p/>'.format(line_files)
                    
            
        # SEND EMAIL
        if ai:
            email_outlk.send(send_to_address, subject, msg, [])
            
            if welcome != '':
                msg = '<h2>Hi {}</h2>'.format(str(welcome.split('.')[0].upper()))
                msg += '<p>welcome in <b>MASA</b> - Statistical process control (SPC) is a method of quality control which employs statistical methods to monitor and control a process.<p/>'
                msg += '<h3>SPC tests:</h3>'
                msg += '<p>'
                msg += 'Every {} seconds, data is loaded from the database and is tested for these tests: <br>'.format(str(uptime))
                msg += '/* TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV */<br>'
                msg += '/* TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole */<br>'
                msg += '/* TEST 3 : 6 po sebe iducich bodov klesa alebo stupa */<br>'
                msg += '/* TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL */<br>'
                msg += '/* TEST 5 : 6 bod po sebe iducich ma rovnaku hodnotu */<br>'
                msg += '/* TEST 6 : ziadny z 8 po sebe iducich bodov nelezi v pasme C */<br>'
                msg += '<br>'
                msg += 'The data sample size is default 50. Current is {}<br>'.format(str(amount_of_data))
                msg += '<b>We want to know every single piece. No losses and no filters!</b>'                
                email_outlk.send([welcome], 'Welcome', msg, [])
            
        
        fifth_end_timer = perf_counter()
        print('[+] fifth Done {}s | SPC runner = {} | Main count = {}\n'.format(format((fifth_end_timer - fifth_start_timer),'.2f'), spc_running, how_much))
        sleep(12) # while delay

    

def screen(version):
    
    r = 1
    
    if r == 1:
        print("")
        print("  _|      _|    _|_|      _|_|_|    _|_|    ")
        print("  _|_|  _|_|  _|    _|  _|        _|    _|  ")
        print("  _|  _|  _|  _|_|_|_|    _|_|    _|_|_|_|  ")
        print("  _|      _|  _|    _|        _|  _|    _|  ")
        print("  _|      _|  _|    _|  _|_|_|    _|    _| SPC ")
        print("")
        print(" --==[ {} ]==--".format(version))
        print("")
    elif r == 2:
        print("")
        print("  MM    MM   AAA    SSSSS    AAA    ")
        print("  MMM  MMM  AAAAA  SS       AAAAA   ")
        print("  MM MM MM AA   AA  SSSSS  AA   AA  ")
        print("  MM    MM AAAAAAA      SS AAAAAAA  ")
        print("  MM    MM AA   AA  SSSSS  AA   AA   SPC ")
        print("")
        print(" --==[ {} ]==--".format(version))
        print("")
        
#
# Funkcia nacita linky a stroje zo subora json.
# Vracia 3x premenu. Prve pole liniek v tvare: ['PORSCHE', 'MQB1'...
# Druhe pole strojov na linke v tvare [('SMT1', 'MQB1', 'SHI', '46E1SHI1'), ('MQB', 'MQB1', 'ST05', '46E1ST05')...
# Tretie data komplet nacitany json subor v tvare {'PORSCHE': [{'projectName': 'Porsche', 'nameStationPc': '08E1ST20', 'Station': 'ST20', 'Measure': ['Area1_position_longEdge',....]},{...
def load_line_file(lfile):

    if os.path.exists(lfile):

        try:
            with open(lfile, 'r') as f:
                data = json.load(f)
        except:
            print('[!] Error load file: {}'.format(lfile))
            sleep(3)
            data = []
    
    return data

#
#Funkcia vytovory zlozku ak neexistuje
def create_dir(dir_path):
    
    if not os.path.isdir(dir_path):
        try:
            os.mkdir(dir_path)
            print('[+] Dir created: {}.'.format(dir_path))
        except: 
            print('[-] Dir not created: {}!'.format(dir_path))

            
#
# Funkcia vytvory pole z nazvami suborov ktore maju koncovku .line/.LINE
# Ak nenajde ziaden subor .line tak vytvory prazdny.
#
def get_line_files():
    
    files = []
    ls = os.listdir(current_path)

    for l in ls:
        ext = l.split('.')
        if ext[-1] == 'line' or ext[-1] == 'LINE':
            files.append(l)
            
    if len(files) == 0:
        
        data_address =[
            {
                "assyName": "DNH3",
                "projectName": "DNH",
                "nameStationPc": "41E4ST10",
                "Station": "ST10",
                "ID_Station": 731,
                "Measure": [
                    "ScrewingTorque_1",
                    "ScrewingTorque_2",
                    "ScrewingTorque_3"
                ]
            },
            {
                "assyName": "DNH3",
                "projectName": "DNH",
                "nameStationPc": "41E4ST20",
                "Station": "ST20",
                "ID_Station": 735,
                "Measure": [
                    "Cam1_Angle",
                    "Cam2_Distance",
                    "Cam2_Angle",
                    "Cam3_Angle"
                ]
            }
        ]
        
        json_object = json.dumps(data_address, indent = 4) # Serializing json 
          
        # ----- Writing to json file
        try:
            with open('SAMPLE.line', "w") as outfile:
                outfile.write(json_object)
            print('[+] Create file: SAMPLE.line!')
            print('')
            print('[*] Now you can create data of line, first rename file SAMPLE.line. Ex: DNH1.line')
            print('    Next open the file in your favorite text editor and replace/add station data and measures.')
            print('')
            files = []
        except:
            print("[-] Failed create file: SAMPLE.line!")
            print("[-] I don't have permission to create file!")
            sys.exit(0)
            
    return files
      

#
# Funkcia vracia aktulany datum vo formate string(YYYY),string(MM),string(DD)
# ma jeden argument posun datumu spat, pre aktulny datum je argument cislo 0.
def datetime_format(day_offset):

    dt = datetime.datetime.now() - datetime.timedelta(days=int(day_offset))        # get prev datetime
    d = dt.day
    m = dt.month
    y = dt.year

    # DAY FORMAT 00
    if d < 10:
        d = "0" + str(d)
    # MON FORMAT 00
    if m < 10:
        m = "0" + str(m)

    return str(y), str(m), str(d) # YYYY, MM, DD


#
# Funkcia vrati cislo tyzdna, zaciatok, koniec datumu a casu v tvare 2022-01-10 00:00:00, 2022-01-16 23:59:59.913600
# Vstupny argument je integer pre ovset tyzdna do minulosti, 0 = aktualny tyzden
def week_last(week_offs):
    
    #1 = first_day 2022-01-03 00:00:00 - last_day 2022-01-09 23:59:59.913600
    #2 = first_day 2022-01-10 00:00:00 - last_day 2022-01-16 23:59:59.913600
    
    week = datetime.date.today().isocalendar()[1]
    week = week-week_offs
    year = datetime.date.today().isocalendar()[0]
    
    w = str(year) + '-W' + str(week) # change week here (-2 default)
    
    first_day = datetime.datetime.strptime(w + '-1', '%Y-W%W-%w')
    last_day = first_day + datetime.timedelta(days=6.999999)
    
    first_day = str(first_day)
    first_day = first_day[:16]
    last_day = str(last_day)
    last_day = last_day[:16]

    return week, first_day, last_day



#
# FTQ
# & Find fails
def get_ftq(cursor, assy, station, ID_Station, StartTime, StopTime):
    
    # ----- sql process data (FOR FTQ DATA)
    data = sql_db.get_process_data(cursor, ID_Station, StartTime, StopTime)
    array_id_process = []

    print('-----------------------------+')
    
    print('[DEBUG] type of data = {}'.format(type(data)))
    print('[DEBUG] length of data = {}'.format(len(data)))
    
    if len(data) == 0:
        return [assy, station, 0, 0, 0, 0, 0, [], 0.01, {}]
    
    pseudo = 0
    n2 = 0
    n3 = 0
    OutputParts = 0
    
    n1n = 0
    n2n = 0
    n3n = 0
    all_retests = 0
    
    fail = 0
    FirstPass = 0
    
    traceoff = 0
    
    duration = []
    
    
    for i in data:
        duration.append(i[7])

        if i[2]:
            pseudo = pseudo + 1
        if i[3]:
            n2 = n2 + 1
        if i[4]:
            n3 = n3 + 1
        if i[5]:
            OutputParts = OutputParts + 1
            
        if not i[2]:
            n1n = n1n + 1
        if not i[3]:
            n2n = n2n + 1
        if not i[4]:
            n3n = n3n + 1
        if not i[5]:
            all_retests = all_retests + 1
        
        if i[3] and i[5] and i[6] != 1: # REAL FAILS BUT HIDEN, TraceOff in header
            traceoff = traceoff + 1
            #print('[TraceOff] {}'.format(i))
            
        if i[3] and i[5] and i[6] == 1:
            fail = fail + 1
        if not i[2] and not i[3] and i[4]:
            FirstPass = FirstPass + 1
            
        if i[2] or i[3]:
        #    print('[_FAIL] {}'.format(i))
            array_id_process.append(i[0])
        #if i[8] != 1:
        #    print('[!FAIL] {}'.format(i))
            
    
    print('[DEBUG] traceoff={}'.format(traceoff))
    OutputParts = OutputParts - traceoff # BECAUSE traceoff
    
    print('[DEBUG] all_tests={}'.format(len(data)-traceoff))
    print('[DEBUG] pseudo={} {} {} OutputParts={}'.format(pseudo,n2,n3,OutputParts))
    print('[DEBUG] {} {} {} all_retests={}'.format(n1n,n2n,n3n,all_retests))
    print('[DEBUG] fail={} FirstPass={}'.format(fail, FirstPass))
    print('[DEBUG] pass={}'.format(OutputParts-fail))
    #ftq = (len(data)-all_retests-fail)/(len(data)-pass_retests)
    info_pcs = {'pass':(OutputParts-fail), 
                'fail':fail,
                'pseudo':pseudo,
                'OutputParts':OutputParts,
                'all_retests':all_retests,
                'FirstPass':FirstPass,
                'traceoff':traceoff,
                'all_tests':(len(data)-traceoff)
                }
    
    ftq_ole = (OutputParts)/(len(data))*100
    print('[FTQ OLE] = {}'.format(ftq_ole))
    
    try:
        ftq_bench = (FirstPass)/(OutputParts)*100
    except ZeroDivisionError:
        ftq_bench = 0
    print('[FTQ BENCH] = {}'.format(ftq_bench))
    
    #FTQ OOE = 1– ( celkový počet chýb / počet PASS kusov na výstupe) = 1 – (112+133) / (3565) = 0,93
    print('[DEBUG] VZOREC = 1-({})/({})'.format((pseudo+n2-fail),(OutputParts-fail)))
    try:
        ftq_ooe = ( 1-(pseudo+fail)/(OutputParts-fail) )*100 # SHITY
    except ZeroDivisionError:
        ftq_ooe = 0
    print('[FTQ OOE] = {}'.format(ftq_ooe))
    print('')
    fdata = sql_db.find_fails(cursor, array_id_process) # SQL
    
    if len(duration) > 0:
        duration_np = np.array(duration, dtype=np.float64)
    
        test_time = np.median(duration_np)
        #average = np.average(duration_np)        
    else:
        test_time = 0
    
    return [assy, station, (OutputParts-fail), fail, ftq_bench, ftq_ole, ftq_ooe, fdata, test_time, info_pcs]
    
    #print(array_id_process)
    #fdata = sql_db.find_fails(cursor, array_id_process)
    #print(fdata)
    #pie_plot(assy, station, fdata)
    
#
# CPK
# Globalna premenna amount_of_data, data_skip_dict
def get_spc_data(cursor, only_pass, NAME_assy, NAME_station, ID_Station, Top, measuresName, StartTime, StopTime):

    global data_skip_dict
    # ----- sql measures data
    start_timer = perf_counter()
    
    debug_get_spc_data = 1
    
    if debug_get_spc_data:
        f = open("debug_debug_get_spc_data_function.log", "a")    
    
    
    
    # TESTING
    # -----------------------------------------------------------------------------------------
    # ----- FILTER REFERENCE
    #
    # STIAHNE SA 2X TOLKO DAT A POTOM SA VYFILTRUJE KONKRETNE MERANIE PODLA POSLEDNEJ REFERENCIE
    # -----------------------------------------------------------------------------------------
    print('filter -------------++++++++++++')
    print(data_skip_dict)
    
    filter_ref = False
    array_of_filter = []
    
    try:
        d_s_d = data_skip_dict[NAME_assy] # ak najde nejake skipnute data pre danu linku
        for i in range(len(d_s_d[1])):
            data_filter_split = d_s_d[1][i].split('::f') #vytvor pole oddelene '::filter'
            if len(data_filter_split) > 1:
                assy_station = d_s_d[0][i].split('-')
                if len(assy_station) > 1:
                    if assy_station[0] == NAME_assy and assy_station[1] == NAME_station:
                        filter_ref = True
                        array_of_filter.append(assy_station[2]) # < ['DNH3'], ['ST20'], ['Cam2_Angle']
    except KeyError:
        pass
    
    print('[+] Filter ref: {}'.format(filter_ref))
    if filter_ref:
        Top = Top*2
        
    
    # TESTING
    # -----------------------------------------------------------------------------------------
    # ----- ZLUCENIE MERANI A PRIEMER
    #
    # STIAHNE SA x DAT A POTOM SA DATA UPRAVIA PODLA x PRIEMERU
    # #AVG3 = STIAHNE SA 3X TOLKO DAT. TRI PO SEBE MERANIA SA ZPRIEMERUJU A VZNIKNE JEDNO MERANIE
    # ----------------------------------------------------------------------------------------- 
    filter_avg = False
    avgNum = 1
    
    try:
        d_s_d = data_skip_dict[NAME_assy] # ak najde nejake skipnute data pre danu linku
        for i in range(len(d_s_d[1])):
            data_filter_split = d_s_d[1][i].split('::avg') #vytvor pole oddelene '::filter'
            if len(data_filter_split) > 1:
                assy_station = d_s_d[0][i].split('-')
                if len(assy_station) > 1:
                    if assy_station[0] == NAME_assy and assy_station[1] == NAME_station:
                        filter_avg = True
                        avgNum = int(data_filter_split[1])
                        
    except KeyError:
        pass    
    
    print('[+] Filter avg: {} | avgNum={}'.format(filter_avg,avgNum))
    
    #if filter_avg:
    #    Top = Top*avgNum
    #    print(Top)
    #    input('FILTER AVG>')
    
         

    if Top == 0:
        data = sql_db.get_measures_data(cursor, only_pass, ID_Station, measuresName, StartTime, StopTime)     #Top = 0 # disable TOP in SELECT
    else: # TOTO sa pouziva hlavne
        y,m,d = datetime_format(0) # aktualny den
        PresentTime = '{}-{}-{}'.format(y,m,d)
        print(PresentTime)
        try:
            data = sql_db.get_top_measures_data(cursor, ID_Station, measuresName, Top, PresentTime) # << BUG ak nie je datalog numericky ale boolovsky. musi byt cislo
        except pyodbc.Error:
            data = []
            print('[-] General network error. Check your network !')
            sleep(3)
        #if len(data) < Top: #Top
        #    print('[*] Lack of data: geting yesterday data')
        #    y,m,d = datetime_format(1) # vcerajsi den
        #    YesterdayTime = '{}-{}-{}'.format(y,m,d)        
        #    data = sql_db.get_top_measures_data(cursor, ID_Station, measuresName, Top, YesterdayTime)            
        
    end_timer = perf_counter()
    print('[TIME] DATA = {} s'.format(format((end_timer - start_timer),'.2f')))
    
    
    cpk_data = []
    
    for m in measuresName:
        #cpk_data.append(['Empty',[], [],-100,100, [], [], [], 0]) # cpk_data[ NAME_OF_MEASURE, ARRAY_OF_MEASURE_VALUE, ARRAY_OF_POSITION, LIMITA_MIN, LIMITA_MAX, ARRAY_OF_STATISTICS, ARRAY_OF_ID, ARRAY_OF_RESULT, LAST_DATETIME ]
        #cpk_data.append(['Empty',[], [],-100,100, [], [], [], 0, []]) # cpk_data[ NAME_OF_MEASURE, ARRAY_OF_MEASURE_VALUE, ARRAY_OF_POSITION, LIMITA_MIN, LIMITA_MAX, ARRAY_OF_STATISTICS, ARRAY_OF_ID, ARRAY_OF_RESULT, LAST_DATETIME, ARRAY_OF_REFERENCE ]
        cpk_data.append(['Empty',[], [],[],[], [], [], [], [], []]) # cpk_data[ NAME_OF_MEASURE, ARRAY_OF_MEASURE_VALUE, ARRAY_OF_POSITION, ARRAY_OF_LIMITA_MIN, ARRAY_OF_LIMITA_MAX, ARRAY_OF_STATISTICS, ARRAY_OF_ID, ARRAY_OF_RESULT, ARRAY_OF_LAST_DATETIME, ARRAY_OF_REFERENCE ]

    start_timer = perf_counter()
    
    
    # ----- Sortig value by measure name
    # SORT by measure ID for SQL TOP
    
    j = 0
    k = 0
    value = []
    position = []
    idcko = []
    results = []
    references = []
    lim_min = []
    lim_max =[]
    date_tag = []
    
    print('len(data) = {}'.format(len(data)))
    #print(data)
    #for i in data:
    #    print(i)
        
    for i in range(len(data)-1):
        
        if data[i][5] == data[i+1][5]: # ak nazov je roznaky z nasledujucim, ID merania je na [4]
            
            #if data[i][3] == True or only_pass == 1: # only pass
            value.append(data[i][6])
            position.append(data[i][2])
            idcko.append(data[i][9])
            results.append(data[i][3])
            references.append(data[i][10])
            lim_min.append(data[i][7])
            lim_max.append(data[i][8])
            date_tag.append(data[i][0])
            
            cpk_data[j][0] = data[i][5] #name_of_measure
            cpk_data[j][1] = value
            cpk_data[j][2] = position
            cpk_data[j][3] = lim_min #limit_min
            cpk_data[j][4] = lim_max #limit_max
            cpk_data[j][6] = idcko #ID
            cpk_data[j][7] = results # result
            cpk_data[j][8] = date_tag #last_datetime
            cpk_data[j][9] = references # reference of product
        else:
            #if data[i][3] == True or only_pass == 1: # only pass
            value.append(data[i][6])
            position.append(data[i][2])
            idcko.append(data[i][9])
            results.append(data[i][3])
            references.append(data[i][10])
            lim_min.append(data[i][7])
            lim_max.append(data[i][8])
            date_tag.append(data[i][0])
            
            cpk_data[j][0] = data[i][5] #name_of_measure
            cpk_data[j][1] = value
            cpk_data[j][2] = position
            cpk_data[j][3] = lim_min #limit_min
            cpk_data[j][4] = lim_max #limit_max
            cpk_data[j][6] = idcko #ID
            cpk_data[j][7] = results # result
            cpk_data[j][8] = date_tag #last_datetime
            cpk_data[j][9] = references # reference of product
            
            j = j + 1
            #print('cleaning')
            value = []
            position = []
            idcko = []
            results = []
            references = []
            lim_min = []
            lim_max = []
            date_tag = []
        
        if i == len(data)-2: # posledny v poly
            #print('poslednyyyyyyyyy')
            #if data[i][3] == True or only_pass == 1: # only pass
            value.append(data[i+1][6])
            position.append(data[i][2])
            idcko.append(data[i][9])
            results.append(data[i][3])
            references.append(data[i][10])
            lim_min.append(data[i][7])
            lim_max.append(data[i][8])
            date_tag.append(data[i][0])
            
            cpk_data[j][0] = data[i][5] #name_of_measure
            cpk_data[j][1] = value
            cpk_data[j][2] = position
            cpk_data[j][3] = lim_min #limit_min
            cpk_data[j][4] = lim_max #limit_max
            cpk_data[j][6] = idcko #ID
            cpk_data[j][7] = results # result
            cpk_data[j][8] = date_tag #last_datetime
            cpk_data[j][9] = references # reference of product
    
    
    # LOGGER
    if debug_get_spc_data:
        f.write('\n')
        f.write('data_skip_dict={}'.format(data_skip_dict))
        f.write('cpk_data ={}'.format(cpk_data))
        f.write('array_of_filter ={}'.format(array_of_filter))
    
    # ODFILTRUJ PODLA REFERENCIE
    if filter_ref:
        
        for c in range(len(cpk_data)):
            if len(cpk_data[c][0]) != 'Empty': #  ['Empty', [], [], [], [], [], [], [], [], []]
                
                if cpk_data[c][0] in array_of_filter: # << AK JE FILTER PRE MERANIE V ZOZNAME
                    
                    founded_references = {}
                    
                    # ZISTI referencie a pocet Ex: {'P2Q0': 100, ....}
                    for ref in cpk_data[c][9]:
                        if ref not in founded_references:
                            founded_references.update({ref:0})
                        
                        plus1 = founded_references[ref] +1
                        founded_references.update({ref:plus1})
                        
                    # PODMIENKY KEDY FILTROVAT:
                    # AK JE REFERENCIE VIAC AKO 1
                    # A AK SU ASPON 3 MERANIA
                    # AK POSLEDNE 3 MERANIA MAJU ROVNAKU REFERENCIU
                    print(len(cpk_data[c][9]))
                    print(cpk_data[c][9])
                    print(founded_references)
                    #input('FILT  ER>')
                    if len(founded_references.keys()) > 1 and len(cpk_data[c][9]) >= 3:
                        if cpk_data[c][9][-1] == cpk_data[c][9][-2] and  cpk_data[c][9][-2] == cpk_data[c][9][-3]:
                            selected_ref = cpk_data[c][9][-1]
                            print(selected_ref)
                            #input('FILTER>')
                            pass # tu sa upravia cpk_data podla referencie, ostanu data iba z jednej eferencie
                    
                        
                    #input("DEBUG FILTER> NAJDENA REFERENCIA ALE ESTE NIE PODLA NEJ ODFILTROVANA")
                    # UPRAVA cpk_data[], PREJDE CELE POLE A PODLA FILTRA PREJDE cpk_data[FILTER][9]
                    # VYTVORI NOVE cpk_data_f[]
                    
                
                    
                    
                
    
    # ZAMEN POLE LIMITOV A CASOVYCH DAT IBA Z POSLEDNEHO MERANIA, NAHRADI POLE JEDNOU HODNOTOU
    for c in range(len(cpk_data)):
        print(cpk_data[c][3])
        print(cpk_data[c][4])
        if len(cpk_data[c][3]) > 0 and len(cpk_data[c][4]) > 0:
            cpk_data[c][3] = cpk_data[c][3][-1]
            cpk_data[c][4] = cpk_data[c][4][-1]
        else:
            cpk_data[c][3] = -101
            cpk_data[c][4] = 101
            
        
        if len(cpk_data[c][8]) > 0:
            cpk_data[c][8] = cpk_data[c][8][-1]
        else:
            cpk_data[c][8] = 0
    
    # 
    # Ak je pouzity TOP in SQL, oreze pocet MIC, pre stanicu so 14 merani a datmi z poslednich 50 kusov vychadza Top 14*50=700
    # ale ak sa na stanici nepouzije jedno meranie alebo je skipnute tak Top vychadza 14*50=700 pretoze nevieme ci je meranie skipnute alebo sa nepouziva pred tym nez stiahneme data.
    # A spravne by malo potom byt 13*50=650
    # Je nutne po zoradeni zistit ci su data pre jednotlive meranie viac ako 50 a ak hej tak orazezat starsie merania.
    # Data su usporiadane od najstarsieho po najnovsie.[stare,....,nove]
    # cpk_data[c][1] = value[-50:]
    # cpk_data[c][2] = position[-50:]
    # cpk_data[c][6] = idcko[-50:]
    # cpk_data[c][7] = results[-50:]
    
    if Top != 0:
        for c in range(len(cpk_data)):
            cpk_data[c][1] = cpk_data[c][1][-amount_of_data:].copy() #value
            cpk_data[c][2] = cpk_data[c][2][-amount_of_data:].copy() #position
            cpk_data[c][6] = cpk_data[c][6][-amount_of_data:].copy() #idcko #ID
            cpk_data[c][7] = cpk_data[c][7][-amount_of_data:].copy() #results # result
        
            #print(len(cpk_data[c][1]))
            #print(len(cpk_data[c][2]))
            #print(len(cpk_data[c][6]))
            #print(len(cpk_data[c][7]))
        #sleep(2)
    
    # ----- STATISTICS
    # 
    # 1 = cp_k=0.7433092695331818 cp_l=0.7433092695331818 cp_u=0.8835973905612795
    # last = cp_k=0.8066350509503647 cp_l=1.17506960596945 cp_u=0.8066350509503647

    for i in range(len(cpk_data)):
        
        # ----- CPK DATA: vypocet iba z pasovych kusov (pozerat result pole)
        if Top == 0: # ak je TOP 0 tak sa beru data iba pass rovno z SQL
            value_pass = cpk_data[i][1]
        else:
            #value_pass = cpk_data[i][1]
            value_pass = []
            print('[*] sorting data for cpk, only pass...')
            for a in range(len(cpk_data[i][1])):
                #print(cpk_data[i][7][a])
                if cpk_data[i][7][a] == True:
                    value_pass.append(cpk_data[i][1][a])
            print('[+] Done.')
        
        if len(value_pass) > 0:
            print('[+] calculating STATISTICS... ')
            measures_np = np.array(value_pass, dtype=np.float64)
        
            std = np.std(measures_np, ddof=1) 
            median = np.median(measures_np)
            average = np.average(measures_np)
        
            # ----- CPK MATH
            limita_min = cpk_data[i][3]
            limita_max = cpk_data[i][4]
            cp_l = (average-limita_min)/(3*std)
            cp_u = (limita_max-average)/(3*std)
            cp_k = 0.00
        
            if cp_l > cp_u:
                cp_k = cp_u
            elif cp_l < cp_u:
                cp_k = cp_l
            
            # ----- SIGMA MATH
            ucl = average + (6*std)
            lcl = average - (6*std)
            if ucl > limita_max :
                ucl = limita_max # UCL = USL
            if lcl < limita_min :
                lcl = limita_min # LCL = LSL 
            
            # ----- ALL DATA IN ONE (STATISTICS)
            statistic = []
            statistic.append(std)
            statistic.append(median)
            statistic.append(average)
            statistic.append(cp_k)
            statistic.append(cp_l)
            statistic.append(cp_u)
            statistic.append(ucl)
            statistic.append(lcl)
            cpk_data[i][5] = statistic
        
            # ----- ALL DATA IN ONE (DATETIME) neviem co to je :-D
            #last_datetime = []
            #last_datetime # <<<<< :-D WTF
        
            print('cp_k={} cp_l={} cp_u={}'.format(cp_k, cp_l, cp_u))
            print('std={} median={} average={}'.format(std, median, average))
            print('len of data = {}'.format(len(measures_np)))
        else:
            # ----- ALL DATA IN ONE (STATISTICS)
            statistic = []
            statistic.append(0)
            statistic.append(0)
            statistic.append(0)
            statistic.append(0)
            statistic.append(0)
            statistic.append(0)
            statistic.append(0)
            statistic.append(0)
            cpk_data[i][5] = statistic            
            
        
    end_timer = perf_counter()
    print('[TIME] sorting cpk data = {} s'.format(format((end_timer - start_timer),'.2f')))
    
    #for hua in cpk_data:
    #    print(hua)
    #print('hua')
    #sleep(1)
    
    if debug_get_spc_data:
        f.close()    
    
    return cpk_data

#
# Vstup jedno meranie.
# Pouzita GLOBALNA premenna data_spc_prev
# Pouzita GLOBALNA premenna data_skip_dict
# Pouzita GLOBALNA premenna data_all_spc


def spc(assy, station, mdata):
 
    global data_all_spc
    global data_spc_prev
    global data_skip_dict
    global how_much
    
    path_img = ''
    skip = []
    
    debug_spc = 1
    
    if debug_spc:
        f = open("debug_spc_function.log", "a")    

    print('{} - {} - {}'.format(assy, station, mdata[0])) # (MQB1 - SHI - F1)
    
    #(datetime.datetime(2022, 7, 25, 15, 51, 29), '13XF610HAL7C', 1, True, 333158, 'Screw_Hight_RightDown', 0.036, -0.2, 0.2, 548201983, 'MEDIUM')
    #(datetime.datetime(2022, 7, 25, 13, 11, 13), '15H06H1B3M7C', 1, True, 11722935, 'Cam3_Foil_strap_result', 234.55, 130.0, 255.0, 548175129, 'P2Q0')
    #(datetime.datetime(2022, 7, 25, 11, 49, 58), '13TG6H02JE7C', 1, True, 308721, 'X74_Torque_Front_Right_Screw', 0.197, 0.0, 10.0, 548160939, 'X74')
    
    _meas = str(assy) + "-" + str(station) + "-" + str(mdata[0])
    print(_meas)
    print(data_skip_dict)
    
    
    try:
        d_s_d = data_skip_dict[assy] # ak najde nejake skipnute data pre danu linku
        for i in range(len(d_s_d[0])): # prejde zoznam nazvov ktore su skypnute ['MQB1-SHI-F0', 'MQB1-SHI-F1', 'MQB1-MOT-RPM_Assembly_Force_Cel1',.....]
            
            if _meas == d_s_d[0][i]:
                skip = []
                
                for znak in d_s_d[1][i].split('::')[0]: # ak je pouzity ::filter vyzera to nejak takto ['1', '']
                    skip.append(int(znak, 16)) # prevod zo hexa to decimal
                print(skip)
                
    except KeyError:
        pass
    
    # SKIP ALL TEST 1 FOR EVERETHING
    if os.path.exists('skip1'):
        if 1 not in skip:
            skip.append(1)
    
    name_measure = str(mdata[0])
    name_measure = name_measure.upper() # NAZOV MERANIA NA VELKE PISMENA
    status = [False, False, False, False, False, False] # 6x test
    result = []
    lim_min = mdata[3]
    lim_max = mdata[4]
    ucl = mdata[5][6]
    lcl = mdata[5][7]
    #sleep(3)    
    
    #--------------------------------------------------------------------
    # ----- Najde stanicu v slovniku pre porovnanie a ulozenie ID
    # ----- ULOZI do premenej data_path cestu v slovniku pre danu stanicu
    # -------------------------------------------------------------------
    for i in range(len(data_spc_prev)):
        #print(data_spc_prev[i])
        assy_data = data_spc_prev[i][0]
        st_data = data_spc_prev[i][1]
        data_path = -1
        if assy_data == assy and st_data == station:
            data_path = i
            break
            
    print('[DUBUG] POSITION={} PATH={}'.format(data_path, data_spc_prev[data_path]))
    
    print('lim_min={} lim_max={} ucl={} lcl={}'.format(lim_min,lim_max,ucl,lcl))
    
    # -----------------------------------------------------------------
    # REVERSE pole hladaj patern od najaktualnejsich dat, takze od zadu
    # -----------------------------------------------------------------
    reverse_mdata = mdata[1].copy() # pole nameranych dat
    reverse_id_data = mdata[6].copy() # pole id nameranych dat
    
    if len(reverse_mdata) != len(reverse_id_data):
        print('[-] Error : length of array reverse_mdata and reverse_id_data is not equal!')
        print(reverse_mdata)
        print(reverse_id_data)
        print('{} {}'.format(len(reverse_mdata), len(reverse_id_data)))
        input('    Press any key to continue...')
        
    for i in range(len(reverse_mdata) // 2):
        reverse_mdata[i], reverse_mdata[-1-i] = reverse_mdata[-1-i], reverse_mdata[i]
        reverse_id_data[i], reverse_id_data[-1-i] = reverse_id_data[-1-i], reverse_id_data[i]    
    
    # -------------------------------------------------------------------
    # /* TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV */
    # -------------------------------------------------------------------
    t1 = []
    tmp_id = []
    if 1 not in skip :
        for m in range(len(mdata[1])):
            if mdata[1][m] > lim_max or mdata[1][m] < lim_min:
                print('[-] TEST 1: {}'.format(mdata[1][m]))
                if mdata[6][m] not in data_spc_prev[data_path][2][name_measure]['TEST1']: # ak ID neexistuje v poly
                    print('[-] TEST 1: {} | ID: {} | EXIST_ID: {}'.format(mdata[1][m], mdata[6][m], data_spc_prev[data_path][2][name_measure]['TEST1']))
                    result.append('TEST 1 : 1 bod nachadzajuci sa mimo pola LSL USL MIMO LIMITOV')
                    t1.append((m, mdata[1][m]))
                    tmp_id.append( mdata[6][m] ) # ulozi ID po pola
                    status[0] = True
                
        if status[0]: # ulozi ak je test pozitivny
            if debug_spc:
                f.write('[{}] {} - counter={}\n'.format(datetime_format(0), _meas, how_much))
                f.write('\t[TEST1] NEW> {}\n'.format(tmp_id))
                f.write('\t[TEST1] TO> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST1']))         
        
            data_spc_prev[data_path][2][name_measure]['TEST1'].extend(tmp_id) # << EXTEND
            data_all_spc[data_path][2][name_measure]['TEST1'] = int(data_all_spc[data_path][2][name_measure]['TEST1'])+1 # counter

            
            if debug_spc:
                f.write('\t[TEST1] EXTENDED> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST1']))

    
    # ---------------------------------------------------------------------
    # /* TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole */
    # ---------------------------------------------------------------------
    t2 = []
    up_down = ""
    patern_0_1 = "01010101010101"
    patern_1_0 = "10101010101010"
    match1 = False
    match2 = False
    
    # VYTVOR STRING z nameranych dat z postupnostou 0 alebo 1
    #for m in range(len(reverse_mdata)-1):
    #    if reverse_mdata[m+1] > reverse_mdata[m]:
    #        up_down += "0"
    #    else:
    #        up_down += "1"
    #        
    #if up_down[-1] == '0':
    #    up_down += '1'
    #else:
    #    up_down += '0'
        
    
    
    # VYTVOR STRING z nameranych dat z postupnostou 0 alebo 1
    for m in range(len(reverse_mdata)-1):
        if reverse_mdata[m+1] > reverse_mdata[m]:
            up_down += "0"
        elif reverse_mdata[m+1] < reverse_mdata[m]:
            up_down += "1"
        else:
            up_down += "2"
    
    # NAJDI PATERNy vo vytvorenem stringu
    match1 = re.search(patern_0_1, up_down) # EX: <re.Match object; span=(3462, 3476), match='01010101010101'>
    match2 = re.search(patern_1_0, up_down)
    
    if 2 not in skip:
        if match1 or match2: # ak sa nejaky patern nasiel tak test je pozitivny        
            if match1 and match2:
                start_position = min(match1.start(), match2.start())
                end_position = min(match1.end(), match2.end())
            elif match1:
                start_position = match1.start()
                end_position = match1.end() #start_position = match1.start()
            elif match2:
                start_position = match2.start()
                end_position = match2.end()
            print('[-] TEST 2: {}'.format(up_down))
            

            # UPDATE: medzi bodmi z mnoziny pozitivneho testu nesmie presiahnut hodnotu (|limita min| + |limita max|) / 4
            test2_quarter = reverse_mdata[start_position:end_position]
            
            if (abs(min(test2_quarter))+abs(max(test2_quarter))) > ((abs(lim_min)+abs(lim_max))/4):
        
                if reverse_id_data[start_position] not in data_spc_prev[data_path][2][name_measure]['TEST2']:
                    print('[-] TEST 2: {}'.format(up_down))
            
                    # t2 na zobrazenie v grafe
                    t2.append(len(reverse_mdata)-1-end_position) # x start, plus odpocet pre prevod z reverz naspat
                    t2.append(len(reverse_mdata)-1-start_position) # x stop, plus odpocet pre prevod z reverz naspat             
                    t2.append(mdata[1][-end_position]) # y start axes
                    t2.append(mdata[1][-start_position]) # y end axes            
            
                    print('    DATA position {} - {}'.format(start_position, end_position))
                    print('    DATA from position {}'.format(reverse_mdata[start_position:end_position]))
                    print('    DATA = reverse_mdata = {}'.format(reverse_mdata))            
                    result.append('TEST 2 : 14 po sebe iducich bodov pravidelne kolise hore a dole')
                    status[1] = True
                
                    if debug_spc:
                        f.write('[{}] {} - counter={}\n'.format(datetime_format(0), _meas, how_much))
                        f.write('\t[TEST2] NEW> {}\n'.format([reverse_id_data[start_position]]))
                        f.write('\t[TEST2] TO> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST2']))
                    
                    data_spc_prev[data_path][2][name_measure]['TEST2'].extend( [reverse_id_data[start_position]] ) # ulozi iba jedno ID do pola.
                    data_all_spc[data_path][2][name_measure]['TEST2'] = int(data_all_spc[data_path][2][name_measure]['TEST2'])+1 # counter
                
                    if debug_spc:
                        f.write('\t[TEST2] EXTENDED> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST2']))                
    
    # --------------------------------------------------------
    # /* TEST 3 : 6 po sebe iducich bodov klesa alebo stupa */
    # --------------------------------------------------------
    t3 = []
    patern_6x0 = "000000"
    patern_6x1 = "111111"
    match1 = re.search(patern_6x0+'*0', up_down)
    match2 = re.search(patern_6x1+'*1', up_down)
    
    if 3 not in skip:
        if match1 or match2:
            if match1 and match2:
                start_position = min(match1.start(), match2.start())
                end_position = min(match1.end(), match2.end())
            elif match1:
                start_position = match1.start()
                end_position = match1.end()
            elif match2:
                start_position = match2.start()
                end_position = match2.end()
            print('[-] TEST 3: {}'.format(up_down))
            print('    {} not in {}'.format(reverse_id_data[start_position], data_spc_prev[data_path][2][name_measure]['TEST3']))
            
            
            print(reverse_mdata[start_position:end_position])
            input('debug >')
                        
            if reverse_id_data[start_position] not in data_spc_prev[data_path][2][name_measure]['TEST3']:
                print('    POSITIVE')
            
                t3.append(len(reverse_mdata)-1-end_position) # x start, plus odpocet pre prevod z reverz naspat
                t3.append(len(reverse_mdata)-1-start_position) # x stop, plus odpocet pre prevod z reverz naspat             
                t3.append(mdata[1][-end_position]) # y start axes
                t3.append(mdata[1][-start_position]) # y end axes
            
                print('    DATA position {} - {}'.format(start_position, end_position))
                print('    DATA from position {}'.format(reverse_mdata[start_position:end_position]))
                print('    DATA = reverse_mdata = {}'.format(reverse_mdata))
                result.append('TEST 3 : 6 po sebe iducich bodov klesa alebo stupa')
                status[2] = True
                
                if debug_spc:
                    f.write('[{}] {} - counter={}\n'.format(datetime_format(0), _meas, how_much))
                    f.write('\t[TEST3] NEW> {}\n'.format([reverse_id_data[start_position]]))
                    f.write('\t[TEST3] TO> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST3']))
                    
                data_spc_prev[data_path][2][name_measure]['TEST3'].extend( [reverse_id_data[start_position]] ) # ulozi iba jedno ID do pola.
                data_all_spc[data_path][2][name_measure]['TEST3'] = int(data_all_spc[data_path][2][name_measure]['TEST3'])+1 # counter
                
                if debug_spc:
                    f.write('\t[TEST3] EXTENDED> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST3']))                
    
    # ------------------------------------------------------------------
    # /* TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL */
    # ------------------------------------------------------------------
    t4 = []
    tmp_id = []
    if 4 not in skip:
        for m in range(len(mdata[1])):
            if (mdata[1][m] > ucl and mdata[1][m] < lim_max) or (mdata[1][m] < lcl and mdata[1][m] > lim_min):# and mdata[1][m] < lim_max and mdata[1][m] > lim_min:
            
                if mdata[6][m] not in data_spc_prev[data_path][2][name_measure]['TEST4']: # ak ID neexistuje v poly
                    print('[-] TEST 4: {}'.format(mdata[1][m]))
                    result.append('TEST 4 : 1 bod nachadzajuci sa mimo regulacneho pola UCL LCL')
                    t4.append((m, mdata[1][m]))
                    tmp_id.append( mdata[6][m] ) # ulozi ID po pola
                    status[3] = True
        if status[3]:
            if debug_spc:
                f.write('[{}] {} - counter={}\n'.format(datetime_format(0), _meas, how_much))
                f.write('\t[TEST4] NEW> {}\n'.format(tmp_id))
                f.write('\t[TEST4] TO> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST4']))
                
            data_spc_prev[data_path][2][name_measure]['TEST4'].extend(tmp_id)
            data_all_spc[data_path][2][name_measure]['TEST4'] = int(data_all_spc[data_path][2][name_measure]['TEST4'])+1 # counter
            
            if debug_spc:
                f.write('\t[TEST4] EXTENDED> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST4']))            
    
    # -------------------------------------------------------
    # /* TEST 5 : 6 bod po sebe iducich ma rovnaku hodnotu */
    # -------------------------------------------------------
    t5 = []
    counter = 1
    stoper = 6
    tmp_id = []
    if 5 not in skip:
        for m in range(len(reverse_mdata)-1):
            if reverse_mdata[m] == reverse_mdata[m+1]:
                counter = counter+1
            
                if counter >= stoper:
                    if reverse_id_data[m-stoper+2] not in data_spc_prev[data_path][2][name_measure]['TEST5']: # ak ID neexistuje v poly
                        print('[-] TEST 5: {}'.format(reverse_mdata))
                        print('    {} not in {}'.format(reverse_id_data[m-stoper+2], data_spc_prev[data_path][2][name_measure]['TEST5']))
                        result.append('TEST 5 : 6 bodov po sebe iducich ma rovnaku hodnotu')
                        status[4] = True
                        tmp_id.append(reverse_id_data[m-stoper+2])
                        t5.append((len(reverse_mdata)-1-(m-stoper+2),reverse_mdata[(m-stoper+2)], stoper-1)) # prevod z revez
                        
                        if debug_spc:
                            f.write('[{}] {} - counter={}\n'.format(datetime_format(0), _meas, how_much))
                            f.write('\t[TEST5] NEW> {}\n'.format([tmp_id[0]]))
                            f.write('\t[TEST5] TO> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST5']))                        
                        
                        data_spc_prev[data_path][2][name_measure]['TEST5'].extend( [tmp_id[0]] ) # ulozi iba prve najnovsie ID do pola.
                        data_all_spc[data_path][2][name_measure]['TEST5'] = int(data_all_spc[data_path][2][name_measure]['TEST5'])+1 # counter
                        
                        if debug_spc:
                            f.write('\t[TEST5] EXTENDED> {}\n'.format(data_spc_prev[data_path][2][name_measure]['TEST5']))                        
                    break
            else:
                counter = 1
        
    # ----------------------------------------------------------------
    # /* TEST 6 : ziadny z 8 po sebe iducich bodov nelezi v pasme C */
    # ----------------------------------------------------------------
    
    # ----- ULOZ pre nasledujuce porovnanie
    # ulozit datetime a ked sa bude zhodovat z aktualnym tak sa test zahodi.
    # ulozi sa pod typom 'dict' ako globalna premenna
    # ulozi sa pod objektom assy a station 
    # ulozi sa pod objektom nazov_merania = mdata ['Camera_3_Flat_cable_Top',
    # ex: {'MQB1-ST20-MENO_MERANIA': datetime(), ...}
    # slovnik sa vygeneruje pri spusteni programu
    # kazda linka bude mat svoj slovnik

    
    
    print(status)
    if status[0] or status[1] or status[2] or status[3] or status[4]:
        try:
            path_img = plot(assy, station, mdata ,result, t1, t2, t3, t4, t5, 0)
        except:
            email_outlk.send(["jan.graf@marelli.com"], 'BUG', '<p>Line 1789.<p/>', [])            
        
        if debug_spc:
            f.write('PLOT> plot({}, {}, MDATA ,{}, {}, {}, {}, {}, {}, {})\n\n'.format(assy, station, result, t1, t2, t3, t4, t5, 0))
        
    print(len(result))
    
    if debug_spc:
        f.close()    

    return result, path_img


def plot_show(final_data): # dokoncit ? TREBA TO?
    
    fig, axs = plt.subplots(len(mdata), 1,figsize=(1.6*len(mdata),3.2*len(mdata)))
    #fig = plt.figure(figsize=(6,3))
    fig.subplots_adjust(top=0.98) #0.85
    fig.subplots_adjust(bottom=0.02) #0.2
    fig.subplots_adjust(left=0.08) # 0.08
    fig.subplots_adjust(right=0.98) # 0.98
    
    # print('{} | {} | {}'.format(a[0], a[1], a[2][b]))
    
    title = ST
    img = current_path + '\\' + 'plot_' + title + '.png'
    
    for i in range(len(mdata)):
    
        # ----- create y (measure data)
        y1 = mdata[i][1]
        y1 = y1[-30:]
    
        # ----- create x
        x1 = []
        for j in range(1,len(y1)+1):
            x1.append(str(j))
        
        print('len x1 = {} | y1 = {}'.format(len(x1), len(y1)))
    
        axs[i].plot(x1, y1, 'o-', c='#00baff', linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
        axs[i].set_title(title)
        axs[i].yaxis.set_major_formatter(FormatStrFormatter('%.2f')) # Y AXIS = .2f
        axs[i].xaxis.grid(linestyle='-', linewidth=0.1) # X AXIS GRID
        axs[i].yaxis.grid(linestyle='-', linewidth=0.1) # Y AXIS GRID
        axs[i].set_xticklabels(x1, rotation=-30, fontsize=8) # X AXIS ROTATE TICK
        axs[i].set_xlim(-0.1, len(x1)+0.1) # X AXIS LIMIT
        
        lim_min = mdata[i][3]
        lim_max = mdata[i][4]
        lim_center = (lim_min+lim_max)/2
        ofs = ((lim_max - lim_min)/4)           # height out of range
        line = ofs/10                           # height of center line
        
        axs[i].set_yticks([lim_min-ofs,lim_min,((lim_min+lim_center)/2),lim_center,((lim_max+lim_center)/2),lim_max,lim_max+ofs])
        axs[i].axhspan(lim_center-line, lim_center+line, facecolor='#00ff00', alpha=0.3,label='center') # center green line
        axs[i].axhspan(lim_min-ofs, lim_min, facecolor='#ff0000', alpha=0.3, label="out") # out of range down
        axs[i].axhspan(lim_max, lim_max+ofs, facecolor='#ff0000', alpha=0.3) # out of range up     
        
    #plt.show()
    fig.savefig(img, format='png', quality=94, dpi=96) # 146kb jpg 90 160


# Volana z funkcie SPC iba ak neprejde cez test.
def plot(assy, station, mdata, result, t1, t2, t3, t4, t5, ai):
    
    #print('-'*64)
    #print(mdata)
    #input('mdata>')
    #for m in mdata:
    #    print(m)
    #sys.exit(0)
    
    
    fig, axs = plt.subplots(1, 1, figsize=(16,4))
    #fig = plt.figure(figsize=(6,3))
    fig.subplots_adjust(top=0.92) #0.85
    fig.subplots_adjust(bottom=0.08) #0.2
    fig.subplots_adjust(left=0.07) # 0.08
    fig.subplots_adjust(right=0.98) # 0.98    
    
    img_filter = mdata[0]
    img_filter = img_filter.replace(' ','_')
    #img_filter = img_filter.replace('&','_')
    #img_filter = img_filter.replace('(','_')
    #img_filter = img_filter.replace(')','_')
    #img_filter = img_filter.replace('=','_')          
    title = assy + '-' + station + '-' + img_filter
    
    img = current_path + '\\' + assy + '\\' + 'PLOT-' + title + '.png'
    
    if ai:
        img = current_path + '\\' + 'tmp_masa' + '\\' + 'PLOT-' + title + '.png'
    
    # ----- CREATE Y (measure data)
    y1 = mdata[1]
    y1 = y1[-amount_of_data:] #y1[-100:]
    
    # ----- CREATE X
    x1 = []
    for j in range(1,len(y1)+1):
        x1.append(str(j))
        
    # ----- CREATE FIXTURE POSITION
    f1 = mdata[2]
    f1 = f1[-amount_of_data:] #y1[-100:]
    
        
    # ----- COLORED point
    colored_position = True
    c_point = ['red', 'black', 'yellow', 'blue', 'green', 'orange', 'while']

    x_f = [[],[],[],[],[],[],[],[]]
    y_f = [[],[],[],[],[],[],[],[]]
    rateOfFixture = max(f1)
    
    if rateOfFixture > 1 and rateOfFixture <= 7 and colored_position:
        for r in range(len(f1)):                     # pole pozucii fixturi
            for q in range(1,rateOfFixture+1):      # bude hladat iba po pocet poziici fuxtur, ak pozicii je 3 tak 3x test if
                #print('{} == {}'.format(q, f1[r]))
                if q == f1[r]:
                    x_f[q-1].append(x1[r])
                    y_f[q-1].append(y1[r])
                    break
            
        
    print('len x1 = {} | y1 = {}'.format(len(x1), len(y1)))
    
    axs.plot(x1, y1, 'o-', c='#00baff', linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
    
    if rateOfFixture > 1 and rateOfFixture <= 7 and colored_position:
        #print('f1={}'.format(f1))
        #print(x_f)
        #print(y_f)
        axs.plot(x_f[0], y_f[0], 'o', c=c_point[0], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
        if rateOfFixture > 2:
            axs.plot(x_f[1], y_f[1], 'o', c=c_point[1], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
            if rateOfFixture > 3:
                axs.plot(x_f[2], y_f[2], 'o', c=c_point[2], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
                if rateOfFixture > 4:
                    axs.plot(x_f[3], y_f[3], 'o', c=c_point[3], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
                    if rateOfFixture > 5:
                        axs.plot(x_f[4], y_f[4], 'o', c=c_point[4], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
                        if rateOfFixture > 6:
                            axs.plot(x_f[5], y_f[5], 'o', c=c_point[5], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)
                            if rateOfFixture > 7:
                                axs.plot(x_f[6], y_f[6], 'o', c=c_point[6], linewidth=0.8, markeredgecolor = '#ffffff', markersize=4)                            
    
    axs.set_title(title)
    axs.yaxis.set_major_formatter(FormatStrFormatter('%.2f')) # Y AXIS = .2f
    axs.xaxis.grid(linestyle='-', linewidth=0.1) # X AXIS GRID
    axs.yaxis.grid(linestyle='-', linewidth=0.1) # Y AXIS GRID
    axs.set_xticklabels(x1, rotation=-30, fontsize=8) # X AXIS ROTATE TICK
    axs.set_xlim(-0.1, len(x1)+0.1) # X AXIS LIMIT
        
    lim_min = mdata[3]
    lim_max = mdata[4]

    ucl = mdata[5][6]
    lcl = mdata[5][7]
    
    #mdata[5]:
    #statistic.append(std)
    #statistic.append(median)
    #statistic.append(average)
    #statistic.append(cp_k)
    #statistic.append(cp_l)
    #statistic.append(cp_u)
    #statistic.append(ucl)
    #statistic.append(lcl)

    lim_center = (lim_min + lim_max)/2
    ofs = (lim_max - lim_min)/4             # height out of range
    line = ((lim_max - lim_min)/4)/16       # height of center line
    
    axs.set_yticks([lim_min-ofs,
                    lim_min,
                    (lim_min+lim_center)/2,
                    #lcl,
                    lim_center,
                    #ucl,
                    (lim_max+lim_center)/2,
                    lim_max,
                    lim_max+ofs],
                   minor=False)
    
    axs.text(0.5, lim_center-line, 'Target', color="#00ff00",alpha=0.5, fontsize=8) # Center
    axs.text(0.5, lim_min-(ofs/2)-line, 'LSL '+format(lim_min,'.2f')+' [Lower Specification Limit]', color="red",alpha=0.5, fontsize=8) # Lower Specification Limit
    axs.text(0.5, lim_max+(ofs/2)-line, 'USL '+format(lim_max,'.2f')+' [Upper Specification Limit]', color="red",alpha=0.5, fontsize=8) # Upper Specification Limit
    axs.text(0.5, lcl-line, 'LCL '+format(lcl,'.2f')+' [Lower Control Limit 6sigma]', color="white",alpha=0.5, fontsize=8) # Lower Control Limit 6sigma
    axs.text(0.5, ucl-line, 'UCL '+format(ucl,'.2f')+' [Upper Control Limit 6sigma]', color="white",alpha=0.5, fontsize=8) # Upper Control Limit 6sigma
    
    axs.axhspan((lim_center-line), (lim_center+line), facecolor='#00ff00', alpha=0.3,label='center') # center green line
    axs.axhspan(lim_min-ofs, lim_min, facecolor='#ff0000', alpha=0.3, label="out") # LIM MIN out of range down
    axs.axhspan(lim_max, lim_max+ofs, facecolor='#ff0000', alpha=0.3) # LIM MAX out of range up
    axs.axhspan(lim_min-line, lcl, facecolor='white', alpha=0.15) # LIM LCL
    axs.axhspan(ucl, lim_max+line, facecolor='white', alpha=0.15) # LIM UCL
    
    # ---- RESULT text in plot up
    axs.text(0.0, lim_max+ofs+line, str(result), color="white",alpha=0.8, fontsize=6) # result text
    
    # ---- DATETIME text in plot down right
    last_time_str = 'Last pcs:' + str(mdata[-2])
    axs.text(len(x1)-1, lim_min-ofs-(line*3), last_time_str, color="white",alpha=0.8, fontsize=6 , horizontalalignment='right') # datetime text
    
    # ---- STATISTIC text in plot down left
    statistics_info = 'Statistics: [ std=' + str(format(mdata[5][0], '.3f'))
    statistics_info += ' | med=' + str(format(mdata[5][1], '.3f'))
    statistics_info += ' | avg=' + str(format(mdata[5][2], '.3f'))
    statistics_info += ' | cpk=' + str(format(mdata[5][3], '.3f'))
    statistics_info += ' | cpl=' + str(format(mdata[5][4], '.3f'))
    statistics_info += ' | cpu=' + str(format(mdata[5][5], '.3f')) + ' ]'
    
    # ----- T5 points [(x1, value1, stoper)]
    if len(t5) > 0:
        print(t5)
        axs.axvline(t5[0][0]-t5[0][2]+0.1, color='blue', alpha=0.3, linestyle='--', label='TEST5')
        axs.text(t5[0][0], t5[0][1]+(line*4), '<< TEST5', color="blue", fontsize=6, horizontalalignment='right')
        axs.axvline(t5[0][0]+0.1, color='blue', alpha=0.3, linestyle='--', label='TEST5')
        
    
    # ----- T4 points [(x1, value1),(xnx, valuen), ...]
    if len(t4) > 0:
        print(t4)
        for t4_point in t4:
            axs.text(t4_point[0], t4_point[1]+(line*2), 'TEST4', color="white", fontsize=6)
            axs.axvline(t4_point[0], color='white', alpha=0.3, linestyle='--', label='TEST4')
    
    # ----- T3 points [x1, x2, y1, y2]
    if len(t3) == 4:
        print(t3)
        axs.text(t3[0], t3[2]+(line*2), 'TEST3 >>', color="orange", fontsize=6)
        #axs.text(t3[1], t3[3], '<T3', horizontalalignment='right', color="red", fontsize=6)
        #axs.axvspan(t3[0], t3[1], facecolor='orange', alpha=0.15)
        axs.axvline(t3[0], color='orange', alpha=0.3, linestyle='--', label='TEST3')
        axs.axvline(t3[1], color='orange', alpha=0.3, linestyle='--', label='TEST3')
        
    # ----- T2 points [x1, x2, y1, y2]
    if len(t2) == 4:
        print(t2)
        axs.text(t2[0], t2[2]+(line*2), 'TEST2 >>', color="yellow", fontsize=6)
        axs.axvline(t2[0], color='yellow', alpha=0.3, linestyle='--', label='TEST2')
        axs.axvline(t2[1], color='yellow', alpha=0.3, linestyle='--', label='TEST2')
    
    # ----- T1 points [(x1, value1),(xnx, valuen), ...]
    if len(t1) > 0:
        print(t1)
        for t1_point in t1:
            if t1_point[1] >= lim_center:
                axs.text(t1_point[0], lim_max+(ofs/2)-line+(line*3), 'TEST1 '+str(t1_point[1]), color="red", fontsize=6)
            else:
                axs.text(t1_point[0], lim_min-(ofs/2)-line-(line*3), 'TEST1 '+str(t1_point[1]), color="red", fontsize=6)
            axs.axvline(t1_point[0], color='red', alpha=0.3, linestyle='--', label='TEST1')        
        
    axs.text(0.0, lim_min-ofs-(line*3), statistics_info, color="white",alpha=0.8, fontsize=6) # statistics text
    
    axs.set_ylim(lim_min-ofs-ofs/4, lim_max+ofs+ofs/4) # Y LIMIT
        
    #plt.show()
    # ----- SAVE PLOT TO IMG
    # 6MB = 128img, 1536x384
    if ai:
        print('[+] save img: {}!'.format(img))
        fig.savefig(img, format='png', quality=99, dpi=96) # 146kb jpg 90 160
        #fig.cla()
        del fig
    else:
        print('[+] Save img: {}!'.format(img))
        fig.savefig(img, format='png', quality=99, dpi=96) # 146kb jpg 90 160
        #fig.cla()
        del fig
    #sleep(0.1)
    
    print('[gc] get_count={}\n'.format(gc.get_count()))
    gc.collect()
    print('[gc] get_count={}\n'.format(gc.get_count()))
    
    return img # path img = current_path + '\\' + assy + '\\' + 'PLOT-' + title + '.png'


# Show spc for everything
def plot_spc(data_all_spc):
    
   
    
    pass

def pie_plot(ftqdata):
    
    debug_pie_plot = 1
    
    if debug_pie_plot:
        f = open("debug_pie_plot_function.log", "a")
        f.write('ftqdata={}\n'.format(ftqdata))
        f.close()
    
    assy = ftqdata[0][0]
    img = current_path + '\\' + assy + '\\' + 'FAIL-' + assy + '.png'    

    # ----- VYTVOR POLE, SPOCITAJ DUPLICITY A VYPOCITAJ COUNTER
    array_fails = [] # [[ID, FAIL_NAME, COUNTER, ASSY, ST],...]
    for data in ftqdata:
        if len(data) > 7: # data musia mat dlzku 7 EX: ['DNH3', 'ST10', 3717, 23, 87.52, 87.13, 96.69, [(517629574, False, 0.202, -0.2, 0.2, 'Screw_4', 13401526),...]]
            fdata = data[7]
            
    
            for i in range(len(fdata)):
                count = 0
                jump = 0
                for f in range(len(array_fails)):
                    if array_fails[f][0] == fdata[i][6]:
                        jump = 1

                if jump == 0:
                    for j in range(len(fdata)):
                        if fdata[i][6] == fdata[j][6]:
                            count = count + 1
                    array_fails.append([fdata[i][6],fdata[i][5],count, data[0], data[1]])
    
    # ----- VYTVOR POLE STANIC, VYMAZ DUPLICITY
    array_st = []
    for i in range(len(array_fails)):
        jump = 0
        for j in range(len(array_st)):
            if array_fails[i][4] == array_st[j]:
                jump = 1
        if jump == 0:
            array_st.append(array_fails[i][4])
    
    # ----- VYTVOR POLE HODNOT A LABELOV, PRE VYKRESLENIE, V TVARE [ [POLE COUNTER PRE STANICU], [...]... ]
    # ----- ZISTI VELKOST NAJDLHSIE POLA A ULOZ HODNOTU
    array_count = [] # [[,...],[,...]...]
    array_label = [] # [[,...],[,...]...]
    len_count = 0
    len_count_tmp = 0
    for st in array_st:
        tmp_count = []
        tmp_label = []
        len_count_tmp = 0
        for i in range(len(array_fails)):
            if st == array_fails[i][4]:
                tmp_count.append(array_fails[i][2])
                len_count_tmp = len_count_tmp + 1
                label = str(array_fails[i][4]) + ' ' + str(array_fails[i][1]) + ' (' + str(array_fails[i][2]) + 'x)'
                tmp_label.append(label)
                
        array_count.append(tmp_count)
        array_label.append(tmp_label)
        if len_count_tmp > len_count:
            len_count = len_count_tmp
    
    
    # ----- POLIA V POLY ARRAY_COUNT MUSI MAT ROVNAKU DLZKU AKO NAJDLHSIE POLE, DOPLN NULY DO KRATSICH
    for i in range(len(array_count)):
        len_c = len_count - len(array_count[i])
        #print('{} {} +{}xx0'.format(len(array_count[i]), array_count[i], len_c))
        for j in range(len_c):
            array_count[i].append(0)
            array_label[i].append('')
    
    # ----- VYTVORY POLE FARIEB PRE STANICE ,OPAKUJUCE SA FARBY
    colors_plt = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Oranges, plt.cm.Purples, plt.cm.Greys, plt.cm.BuPu, plt.cm.PuRd, plt.cm.GnBu]
    
    colored_st = []
    r = 0
    for i in range(len(array_st)):
        
        colored_st.append(colors_plt[r](0.9))     
        r = r+1
        if r > len(colors_plt)-1:
            r = 0
            
    # ----- VYTVOR POLE LABELS PRE FAILY
    labels_fail = []
    for al in array_label:
        for l in al:
            labels_fail.append(l)
        
    # ----- VYTVOR PLOT
    #fig, ax = plt.subplots()
    fig, ax = plt.subplots(1, 1, figsize=(20,9))
    fig.subplots_adjust(top=0.97) #0.85
    fig.subplots_adjust(bottom=0.01) #0.2
    fig.subplots_adjust(left=0.01) # 0.08
    fig.subplots_adjust(right=0.99) # 0.98     
    ax.set(aspect="equal", title=assy)
    size = 0.3
    vals = np.array(array_count)
    
    #
    # ----- Z POLA LABEL FAIL NEUKAZUJE FAILI KTORE SU MENEJ AKO max_show_fail
    max_show_fail = 0
    labels_fail_final = []
    vals_flatten = vals.flatten()
    
    #print(vals) # Ex. [[1 2 3 n] [4 5 6 n] [7 8 9 n]]
    #print(vals_flatten) # Ex. [ 1 2 3 n 4 5 6 n 7 8 9 n]
    
    if len(vals_flatten) > 32:
        max_show_fail = 2 # zobrazi viac ako 2
    else:
        max_show_fail = 0 # zobrazi viac ako 0
        
    for i in range(len(vals_flatten)):
        if vals_flatten[i] > max_show_fail:
            labels_fail_final.append(labels_fail[i])
        else:
            labels_fail_final.append('')
    
    try:
        # ----- INER (STATIONS)
        wedgesIN, textsIN = ax.pie(vals.sum(axis=1),
                                            radius=1,
                                            startangle=90,
                                            colors=colored_st,
                                            labels=array_st,
                                            labeldistance=0.79,                                            
                                            #wedgeprops=dict(width=size, edgecolor='black')
                                            )
        plt.setp( wedgesIN, width=0.3, edgecolor='black')
        plt.setp( textsIN, size=8, color='white', weight="bold")
    
        # ----- OUTER (FAILS)
        wedgesOUT, textsOUT = ax.pie(vals.flatten(),
                                               radius=1+0.1,
                                               startangle=90,
                                               #autopct='%1.1f%%',
                                               #pctdistance=0.92,
                                               #wedgeprops=dict(width=size, edgecolor='black')
                                               labels=labels_fail_final,#labels_fail,
                                               labeldistance=1.05,                                               
                                               )
        plt.setp( wedgesOUT, width=0.1, edgecolor='black')
        plt.setp( textsOUT, size=7, color='white', weight="bold")   
    
        #plt.show()
        fig.savefig(img, format='png', quality=94, dpi=96) # 146kb jpg 90 160
    except:
        
        print('[-] Error in function pie_plot(ftqdata): assy={}, img={}, ftqdata={}'.format(assy, img, ftqdata))
        sleep(3)


# Uses pie_plot()
def run_ftq_and_fails(lines_array, failed_run_all, failed_run_line, failed_run_station, StartTime, StopTime):
    
    ftqdata = []
    for i in range(len(lines_array)):
        
        for j in range(len(lines_array[i])):
            
            start_timer = perf_counter()
            
            if (lines_array[i][j]['assyName'] == failed_run_line and lines_array[i][j]['Station'] == failed_run_station and 
                failed_run_all == 0) or (lines_array[i][j]['assyName'] == failed_run_line and failed_run_all == 1) or failed_run_all == 2:
                print('{} - {} - {} - {}'.format(lines_array[i][j]['assyName'], lines_array[i][j]['Station'], lines_array[i][j]['ID_Station'], lines_array[i][j]['Measure'] ))
                #[assy, station, (OutputParts-fail), fail, ftq_bench, ftq_ole, ftq_ooe, fdata]
                ftqdata.append(get_ftq(cursor, lines_array[i][j]['assyName'], lines_array[i][j]['Station'],lines_array[i][j]['ID_Station'], StartTime, StopTime)) # SQL
                print(len(ftqdata))
                
                end_timer = perf_counter()
                print('[TIME] {}-{} : run_ftq_and_fails = {} s'.format(lines_array[i][j]['assyName'], lines_array[i][j]['Station'], format((end_timer - start_timer),'.2f')))                
                
    # ----- PLOT FAILS
    if failed_run_all == 1: # Jedna assy linka
        pie_plot(ftqdata) # MATPLOTLIB

    elif failed_run_all == 2: # Viac assy liniek
        for assy in line_files:
            piedata = []
            for data in ftqdata:
                #print(''.format())
                assy_name = assy.split('.')
                if assy_name[0] == data[0]:
                    print(data)
                    piedata.append(data)

            pie_plot(piedata) # MATPLOTLIB    

# Globalna premenna amount_of_data
def run_spc(cursor, lines_array, only_pass, run_all, run_line, run_station, StartTime, StopTime):
    
    final_data = [] # [ASSY, STATION, [MDATA]]
    start_timer = perf_counter()
    for i in range(len(lines_array)):
        print('================================================================================================')
        
        for j in range(len(lines_array[i])):
            
            if (lines_array[i][j]['assyName'] == run_line and lines_array[i][j]['Station'] == run_station and 
                run_all == 0) or (lines_array[i][j]['assyName'] == run_line and run_all == 1) or run_all == 2:
                
                Top = amount_of_data*(len(lines_array[i][j]['Measure'])) # pocet kusov krat pocet merani.
                #Top = 0
                print('{} - {} - {} - {}'.format(lines_array[i][j]['assyName'], lines_array[i][j]['Station'], lines_array[i][j]['ID_Station'], lines_array[i][j]['Measure'] ))
                mdata = get_spc_data(cursor, only_pass, lines_array[i][j]['assyName'], lines_array[i][j]['Station'], lines_array[i][j]['ID_Station'], Top, lines_array[i][j]['Measure'], StartTime, StopTime) # SQL
                final_data.append([lines_array[i][j]['assyName'], lines_array[i][j]['Station'], mdata])
            
            
    end_timer = perf_counter()
    print('[TIME] get all data = {} s'.format(format((end_timer - start_timer),'.2f')))
    
    for i in final_data:
        print('')
        for j in range(len(i[2])):
            if len(i[2][j][5]) > 0:
                print('ASSY={} ST={} MEASURE={} CPK={} CPL={} CPU={}'.format(i[0], i[1], i[2][j][0], i[2][j][5][3], i[2][j][5][4], i[2][j][5][5])) # assy, st, measure, cpk, cpl, cpu
            else:
                print('ASSY={} ST={} MEASURE={} CPK=0.0 CPL=0.0 CPU=0.0'.format(i[0], i[1], i[2][j][0]))
    
    for i in data_spc_prev:
        print(i)
        
    # ----- SPUST KONTROLU
    print('[+] Runing spc...')
    imgs_to_sent_array = []     # pripravy pole ciest obrazov pre odoslanie pozitivnych testov
    for a in final_data:
        
        for b in range(len(a[2])):
            #print('{} | {} | {}'.format(a[0], a[1], a[2][b])) # ex: MQB1 | ST20 | ['Camera_3_Flat_cable_Top', [0.905, 0.882,......
            if len(a[2][b][1]) > 1:
                test_name, img_to_sent = spc(a[0], a[1], a[2][b]) # (assy, station, mdata)
                if img_to_sent != '':
                    imgs_to_sent_array.append(img_to_sent) # ulozi do pola cestu obrazka/testu 
                print('*'*200)
                print(imgs_to_sent_array)
                print('*'*200)
    print('[*] Spc done!')
    
    for i in data_spc_prev:
        print(i)
        
    send_email_positive_test(imgs_to_sent_array)
    
    #while True:
    #    input('Spustit?:')
    #    # ----- SPUST KONTROLU
    #    print('[+] Runing spc...')
    #    for a in final_data:
    #        for b in range(len(a[2])):
    #            #print('{} | {} | {}'.format(a[0], a[1], a[2][b])) # ex: MQB1 | ST20 | ['Camera_3_Flat_cable_Top', [0.905, 0.882,......
    #            if len(a[2][b][1]) > 0:
    #                spc(a[0], a[1], a[2][b])
    #    print('[*] Spc done!')
    
    #    for i in data_spc_prev:
    #        print(i)    
    
# Funkcia caka pole z cestami kde su ulozene obrazky
# V poly su vsetke linky a stroje
# Rozdeli pole podla linky a odosle data pre danu linku
def send_email_positive_test(imgs_to_sent_array):
    
    # ['d:\\Users\\f93918b\\Documents\\python\\MASA5core\\DNH2\\PLOT-DNH2-ST10-Screwing_Torque_Result_Left_Down.png',...]
    
    
    print('#'*200)
    for l in lines_array:                       # prejde zoznam podla linky.
        #print(l[0]['assyName'])
        buffer_img = []
        HTMLBody = ''
        for img in imgs_to_sent_array:          # prejde pole ulozenych obrazkov
            line_from_path = img.split('\\')    # vytvory pole zo stringu cesty

            if l[0]['assyName'] == line_from_path[-2]:      # porovna linku z cestou kde je nazov
                print('{} - {}'.format(line_from_path[-2], line_from_path))
                buffer_img.append(img)           # ulozi cestu do pola
                HTMLBody += '<img src="'+ line_from_path[-1] +'" alt="Images"><br>'
        if len(buffer_img) > 0:
            eaddresses = email_outlk.get_address(jfile)     # nacita adresu address.json
            try:
                email_to = eaddresses[l[0]['assyName']]       # pole vybranych emailov
            except:
                print('[-] Except in send_email_positive_test')
                HTMLBody += '<p>Error: Missing user for {}<p/>'.format(line_from_path[-2])
                HTMLBody += '<p>You can add a person to the list. Send me an email and write in the subject: ADD PERSON.NAME@MARELLI.COM TO THE {}<p/>'.format(line_from_path[-2])
                email_to = eaddresses['ROOT']
            
            HTMLBody += '<p>MASA5core<p/>'
            email_outlk.send(email_to, str(l[0]['assyName'] ), HTMLBody, buffer_img)
            
            
    print('#'*200)

#
# MAIN
#
if __name__ == "__main__":      
    
    # ----- SETTINGS MATPLOTLIB
    plt.rcParams.update({'figure.max_open_warning': 0})
    plt.style.use('dark_background') # Style for matplotlib
    mpl.use('Agg')
    
    # ----- SCREEN
    version = "Statistical Process Control core v5.0x16"
    screen(version)
    
    
    # ----- MAIN PATH
    current_path = os.getcwd()
    print('[*] Curret working directory {}'.format(current_path))
    
    # ----- MAIN SETTINGS
    amount_of_data = 50         # pocet dat pre spc
    uptime = int(2*60)          # in second
    time_for_report = '06:00'   # run_ftq_and_fails() datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 0 and datetime.datetime.now().day != prev_day
    
    # ----- DATE & TIME
    y,m,d = datetime_format(0)      # uloz aktualny datum
    print('    {}-{}-{}'.format(y,m,d))
    #week = datetime.date.today().isocalendar()[1]
    #print('    Week = {}'.format(week))
    
    #w, StartTime, StopTime = week_last(1)   # uloz predchadajuci week
    #w, StartTime, StopTime = week_last(0)   # uloz aktualny week
    #StartTime='2022-04-26 13:33'
    #StopTime='2022-04-26 23:59'
    #print('    week {} first_day {} - last_day {}'.format(w, StartTime, StopTime))   
    
    # ----- CHECK ADDRESS FILE
    jfile = current_path + '\\address.json'
    if not os.path.exists(jfile):
        count_input = 0
        print('')
        print('[!] Missing address file: {}'.format(jfile))
        print('    Create special user account used for administration.')
        ret = True
        while ret:
            root = input('Enter email: ')
            if len(root.split('@')) == 2 and len(root) < 64:
                r = root.split('@')[1]
                if len(r.split('.')) == 2:
                    ret = email_outlk.create_file_address(jfile, root) # EMAIL
            else:
                count_input = count_input+1
                print('[-] Wrong email address')
                if count_input > 3:
                    print('[*] Email address must be in the form: [Name]@[DomainName] Ex: Thomas.Anderson@matrix.sk')
                if count_input > 10:
                    print('[*] Interesting... Now wait as many seconds as there have been attempts...')
                    sleep(count_input)
    
    # ----- LOAD DATA from json file
    lines_array = []
    line_files = get_line_files()
    print('[+] List of lines: {}'.format(line_files))
    for lfile in line_files:
        line_data = load_line_file(lfile)
        if len(line_data) != 0:
            lines_array.append(line_data) # create array [[{}], [{}],...]c
            
    
            
    # ----- CREATE DICTIONARY for ID
    # ----- CREATE DATA for PREV DATA FOR SPC
    # ----- CREATE DATA for SPC STATISTIC
    # [ [ASSY,ST,{'MEASURE1' : [ID], 'MEASURE2' : [ID],...}], []... ]
    data_spc_prev = []
    data_all_spc = []
    # SKIP MEASURES [ [assy-station-measure, ...], [3, ...]]
    #data_skip = []
    skip_measure = []
    skip_num = []
    data_skip_dict = {}
    for i in range(len(lines_array)):
        
        skip_measure = []
        skip_num = []         
        for j in range(len(lines_array[i])):
            dict_measures = []
            dict_measures.append( lines_array[i][j]['assyName'] ) # ulozi meno linky
            dict_measures.append( lines_array[i][j]['Station'] ) # ulozi meno stanice
            measures = []
            measures_st = lines_array[i][j]['Measure'] # ulozi nazov merania, moze obsahovat skip cez "::" [m1, m2, m3::skip1, m4,...]
            count_zero = 0
                       
            for meas in measures_st:
                measures_split = meas.split('::skip') #vytvor pole oddelene '::skip'
                if len(measures_split) > 1: # ak je v poli viac prvkov lebo split 
                    measures.append(measures_split[0])
                    assy_st_meas = str(lines_array[i][j]['assyName']) +'-'+ str(lines_array[i][j]['Station']) +'-'+ str(measures_split[0])
                    skip_measure.append(assy_st_meas)
                    skip_num.append(str(measures_split[1]))
                    
                    data_skip_dict.update({lines_array[i][j]['assyName']:[skip_measure, skip_num]})
                    #print(data_skip_dict)                    
                    
                    lines_array[i][j]['Measure'][count_zero] = measures_split[0] # <<< WARNING IN TESTING |CLEANING| prepise zoznam bez ::skip
                elif len(measures_split) == 1:
                    measures.append(measures_split[0])
                count_zero += 1
                    
            d = {}
            d2 = {}
            
            # NAZOV MERANIA NA VELKE PISMENA
            for m in measures:
                d[m.upper()] = {'TEST1':[], 'TEST2':[], 'TEST3':[], 'TEST4':[], 'TEST5':[], 'TEST6':[]} # vytvori pre meranie prazdny zoznam
                d2[m.upper()] = {'TEST1':0, 'TEST2':0, 'TEST3':0, 'TEST4':0, 'TEST5':0, 'TEST6':0} # Vytvori counter pre spc ploting
            
            d2_dict_measures = dict_measures.copy()
            d2_dict_measures.append(d2)
            dict_measures.append(d)
            data_spc_prev.append(dict_measures)
            data_all_spc.append(d2_dict_measures)

    
    # ----- CREATE EMPTY TEMPLATE FOR DAYLY RESTART
    emtpy_data_all_spc = data_all_spc.copy()
    #data_skip.append(skip_measure)
    #data_skip.append(skip_num)
    #print(lines_array)
    #print(data_skip) #[['MQB1-SHI-F2', 'MQB1-ST60-Screwing_Torque_Result_3', 'MQB1-ST60-Screwing_Torque_Result_4'], [3A, 1, 15]]
    
    print('[*] Doctionary of skiping: {}'.format(data_skip_dict))
    input('\nRUN? > SEE 1201, 1173')
    
    
    # ----- CHECK ASSY IN DB IF IS NEW THEN ADD TO DB
    # CHECK LINES_ARRAY, IF IS CHANGED UPGRADE DB
    nlu1.run(lines_array, '12662a4b78e19ac27361b005a6dbb3d7')
            
    
    # ----- inicializacia data_path=-1 # ak nenajde stanicu ostava -1, ak sa pouzije [-1] vrati posledne data 'END', osetrenie nedojde k preteceniu                            
    data_spc_prev.append(['END', 'END', {'END': {'TEST1':[], 'TEST2':[], 'TEST3':[], 'TEST4':[], 'TEST5':[], 'TEST6':[]}}]) 
    
    # ----- vypne program ak nenajde ziadne data ohladne liniek
    if len(lines_array) == 0:
        print('[*] No data of lines! Check files with .line')
        sys.exit(404)
        
    # ----- skontoluje/vytvory zlosku pre linky 
    for l in lines_array:
        print(l[0]['assyName'])
        dir_path = current_path + '\\' + str(l[0]['assyName'])
        create_dir(dir_path) # Vytvori zlosku pre linku
    dir_path = current_path + '\\tmp_masa'
    create_dir(dir_path) # Vytvori zlosku TMP
    
    

    how_much = 0
    spc_running = 1 # iba info pre thread t1
    # ----- THREADING
    # Theading pre komunikaciu - email
    t1 = threading.Thread(target=fifth, args=("Thread-fifth", lines_array, jfile, 2))
    t1.start()
    print(t1.is_alive())
    
    #sleep(100000) # <<<<<<<<<<<<<<<<<
    
    sequnce_time_data = []
    
    t2 = threading.Thread(target=main, args=("Thread-main", lines_array, jfile, 2))
    t2.start()
    print(t2.is_alive())
    
    
    while True:
        
        print('')
        print('\t+----------------+')
        print('\t| Thread t1 {} |'.format(t1.is_alive()))
        print('\t| Thread t2 {} |'.format(t2.is_alive()))
        print('\t+----------------+')
        print('')
        
        if not t1.is_alive() or not t2.is_alive():
            all_addresses = email_outlk.get_address(jfile)     # nacita adresu address.json
            email_outlk.send(all_addresses['ROOT'], 'WARNING', '<p>Threading is gone!<p/>', [])
            if not t2.is_alive():
                t2.start()
                sleep(10)
            
        sleep(60)
        
    print('[EOL]')

    
    
def shceme():
    
    #main()
    #
    #  while()
    #
    #    1.run_spc(lines_array, only_pass, run_all, run_line, run_station, StartTime, StopTime)
    #
    #      1.1.get_spc_data(SQL)
    #
    #        1.1.1 SQL.get_top_measures_data(ID_st, measuresName, Top, PresentTime) ALEBO SQL.get_measures_data(only_pass, ID_st, measuresName, StartTime, StopTime)
    #
    #         DATA Z SQL:
    #         cpk_data[j][0] = data[i][5] #name_of_measure
    #         cpk_data[j][1] = value
    #         cpk_data[j][2] = position
    #         cpk_data[j][3] = data[i][7] #limit_min
    #         cpk_data[j][4] = data[i][8] #limit_max
    #         5ty PRVOK REZERVOVANY PRE STATISTIKY  
    #         cpk_data[j][6] = idcko #ID
    #         cpk_data[j][7] = results # result
    #         cpk_data[j][8] = data[i][0] #last_datetime
    #         cpk_data[j][9] = references # reference of product
    #
    #         VYPOCET STATISTIK, LIMITY ULOZENE Z POSLEDNEHO MERANIA, VYPOCET IBA Z PASSOVYCH KUSOV:
    #         cp_l = (average-limita_min)/(3*std)
    #         cp_u = (limita_max-average)/(3*std)
    #         ucl = average + (6*std) SIGMA
    #         lcl = average - (6*std) SIGMA
    #
    #         CELE SA TO ZABALI DO POLA:
    #         statistic[0] = std # <<< 1/(N-1)
    #         statistic[1] = median
    #         statistic[2] = average
    #         statistic[3] = cp_k
    #         statistic[4] = cp_l
    #         statistic[5] = cp_u
    #         statistic[6] = ucl
    #         statistic[7] = lcl
    #
    #         ULOZI STATISTIKY K DATA Z SQL:
    #         cpk_data[i][5] = statistic    
    #
    #      1.2.spc(assy, station, SQLdata)
    #       AK NIE JE SKIPNUTY TEST PRE DANE MERANIE
    #       1.2.1.plot(assy, station, mdata, result, t1, t2, t3, t4, t5, ai)
    #
    #      1.3.send_email_positive_test(imgs_to_sent_array)
    pass