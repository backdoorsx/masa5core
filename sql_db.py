import pyodbc
import sys

import datetime

def connection_sql():

    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.129.38.47;DATABASE=testing;UID=TestingRO;PWD=tst#Pwd34ro_9')
        cursor = conn.cursor()
        
        return conn, cursor
    except:
        print('[-] Cannot open database requested by the login. The login failed.')
        sys.exit(0)


def show_database_schema(cursor):
    
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES")
    row = cursor.fetchall()
    for r in row:
        print(r)
        
    #('testing', 'dbo', 'EWO_Process', 'BASE TABLE')
    #('testing', 'dbo', '__PACKGEN_Watchdog', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_BlueTag', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Activity', 'BASE TABLE')
    #('testing', 'dbo', '__PACKGEN_Watchdog_history', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Buffer', 'BASE TABLE')
    #('testing', 'dbo', 'Flow', 'BASE TABLE')
    #('testing', 'dbo', 'eEWO_X_Bench', 'BASE TABLE')
    #('testing', 'dbo', 'EWO_Process_Plan', 'BASE TABLE')
    #('testing', 'dbo', 'sysdiagrams', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Done', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_JobProjectLock', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Filter', 'BASE TABLE')
    #('testing', 'dbo', '__PtN_Service_Wdg', 'BASE TABLE')
    #('testing', 'dbo', '__ADC_Watchdog_history', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Job', 'BASE TABLE')
    #('testing', 'dbo', 'PM_check', 'BASE TABLE')
    #('testing', 'dbo', 'ProcessPictures', 'BASE TABLE')
    #('testing', 'dbo', 'TRACE_AllProcessViewBD', 'VIEW')
    #('testing', 'dbo', 'TRACE_AllProcessViewMeastable', 'VIEW')
    #('testing', 'dbo', 'Process_history', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_PN', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Producing', 'BASE TABLE')
    #('testing', 'dbo', '_ID_ShiftBase', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Production', 'BASE TABLE')
    #('testing', 'dbo', 'PM_CheckItem', 'BASE TABLE')
    #('testing', 'dbo', '_ID_area', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Profil', 'BASE TABLE')
    #('testing', 'dbo', 'PM_Checklist_standard', 'BASE TABLE')
    #('testing', 'dbo', 'AllAOIDeclaration2', 'VIEW')
    #('testing', 'dbo', 'ProdInfo_Project', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Sequence', 'BASE TABLE')
    #('testing', 'dbo', 'PM_Checklist_specific', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_WIP_Stock', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Stopped', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Filter_B', 'BASE TABLE')
    #('testing', 'dbo', '___Configuration', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Tag', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_NIP_Group', 'BASE TABLE')
    #('testing', 'dbo', '_bench_settings', 'BASE TABLE')
    #('testing', 'dbo', '_measurementsKey', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_List', 'BASE TABLE')
    #('testing', 'dbo', 'Translate_ID_Lang', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_NIP', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_Reference_T', 'BASE TABLE')
    #('testing', 'dbo', 'Translate_Ref', 'BASE TABLE')
    #('testing', 'dbo', '___Process_0', 'BASE TABLE')
    #('testing', 'dbo', 'EWO_ACTIONtracking', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory', 'BASE TABLE')
    #('testing', 'dbo', 'Process', 'BASE TABLE')
    #('testing', 'dbo', '__MM_Supervisor_Wdg', 'BASE TABLE')
    #('testing', 'dbo', 'MeasTable_2022', 'BASE TABLE')
    #('testing', 'dbo', 'AllMeasTables', 'VIEW')
    #('testing', 'dbo', 'WAREHOUSE', 'BASE TABLE')
    #('testing', 'dbo', 'AllMeasView', 'VIEW')
    #('testing', 'dbo', 'AllProcessView', 'VIEW')
    #('testing', 'dbo', 'AllProcessViewNoMeas', 'VIEW')
    #('testing', 'dbo', 'STAT_BenchDaily', 'BASE TABLE')
    #('testing', 'dbo', 'AllProcessViewUniq', 'VIEW')
    #('testing', 'dbo', 'FS_Links', 'BASE TABLE')
    #('testing', 'dbo', 'TRACE_AllProcessView', 'VIEW')
    #('testing', 'dbo', 'FS_CheckToFollow', 'BASE TABLE')
    #('testing', 'dbo', 'EWO_ACTIONcategory', 'BASE TABLE')
    #('testing', 'dbo', 'AllMeasTables_backup', 'VIEW')
    #('testing', 'dbo', 'ProdInfo_Inventory_SAP_FN', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_Diff_Type', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_Diff', 'BASE TABLE')
    #('testing', 'dbo', 'FS_MeasGroup', 'BASE TABLE')
    #('testing', 'dbo', '___IT_timeExec', 'BASE TABLE')
    #('testing', 'dbo', 'BMW_SW', 'BASE TABLE')
    #('testing', 'dbo', 'Flow_backup', 'BASE TABLE')
    #('testing', 'dbo', 'ParentChild', 'BASE TABLE')
    #('testing', 'dbo', 'MeasTable', 'BASE TABLE')
    #('testing', 'dbo', 'EWOcategory', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_Project', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_RADNOK', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_DEK_Console', 'BASE TABLE')
    #('testing', 'dbo', 'LastProcessResults_no use', 'VIEW') 
    #('testing', 'dbo', 'BMW_SWdescr', 'BASE TABLE')
    #('testing', 'dbo', 'RealFailMeasurementPareto', 'VIEW')
    #('testing', 'dbo', 'ProdInfo_Inventory_Stock', 'BASE TABLE')
    #('testing', 'dbo', 'ProcesPK', 'BASE TABLE')
    #('testing', 'dbo', 'FailMeasurementData_no use', 'VIEW')
    #('testing', 'dbo', '_bench', 'BASE TABLE')
    #('testing', 'dbo', 'FailMeasurementPareto_no use', 'VIEW')
    #('testing', 'dbo', 'ProdInfo_Inventory_Stock_Params', 'BASE TABLE')
    #('testing', 'dbo', 'Translate_ID_Text', 'BASE TABLE')
    #('testing', 'dbo', '_line', 'BASE TABLE')
    #('testing', 'dbo', '_benchType', 'BASE TABLE')
    #('testing', 'dbo', '_production', 'BASE TABLE')
    #('testing', 'dbo', 'FlowFailNoRtst', 'BASE TABLE')
    #('testing', 'dbo', '_cycle', 'BASE TABLE')
    #('testing', 'dbo', 'DATA_IO_Declaration', 'BASE TABLE')
    #('testing', 'dbo', '_result', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_ReworkDeviation', 'BASE TABLE')
    #('testing', 'dbo', 'AllAOIDeclaration', 'VIEW')
    #('testing', 'dbo', 'ProdInfo_AOIDeclaration_Reverz', 'BASE TABLE')
    #('testing', 'dbo', 'DATA_IO_Actions', 'BASE TABLE')
    #('testing', 'dbo', 'AllProcessViewUniqReference', 'VIEW')
    #('testing', 'dbo', 'SampleList', 'BASE TABLE')
    #('testing', 'dbo', 'DATA_IO_ActionLog', 'BASE TABLE')
    #('testing', 'dbo', '__ADC_Watchdog', 'BASE TABLE')
    #('testing', 'dbo', '__ADC_Updates', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_ICTDeclaration', 'BASE TABLE')
    #('testing', 'dbo', 'USER', 'BASE TABLE')
    #('testing', 'dbo', '_benchPictureFolders', 'BASE TABLE')
    #('testing', 'dbo', '_USER_JobPosition', 'BASE TABLE')
    #('testing', 'dbo', '_measurements', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_SAP_MVT', 'BASE TABLE')
    #('testing', 'dbo', '_bench_logs', 'BASE TABLE')
    #('testing', 'dbo', '_department', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_AOIDeclaration_Machine', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_AOIDeclaration_Type', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_ReworkPlanTypes', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_SAP_Inv_Stock', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_Inventory_SAP', 'BASE TABLE')
    #('testing', 'dbo', 'PM', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_AOIDeclaration', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_ReworkPlan', 'BASE TABLE')
    #('testing', 'dbo', 'SW_ID', 'BASE TABLE')
    #('testing', 'dbo', 'ValorFeeder', 'BASE TABLE')
    #('testing', 'dbo', 'SW_wdg', 'BASE TABLE')
    #('testing', 'dbo', 'ProdInfo_AOIDeclaration_Notes', 'BASE TABLE')
    #('testing', 'dbo', 'EWO', 'BASE TABLE')
    #('testing', 'dbo', 'EWO_ACTION', 'BASE TABLE')
    #('testing', 'dbo', '_product', 'BASE TABLE')


def find_assy(cursor):

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='_line'")
    lines = cursor.fetchall()
    print(lines)

    cursor.execute("SELECT * FROM _line")
    lines = cursor.fetchall()

    print(lines)
    print("\n +++++++++++++++++++++++++++++++++ \n")

    return lines



def find_stations(cursor, ID_assy):

    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='_bench'")
    stations = cursor.fetchall()
    print(stations)

    ID_STATIONS = str(ID_assy)
    inject = "SELECT * FROM _bench WHERE ID_line='{}'".format(ID_STATIONS)
    stations = cursor.execute(inject)
    stations = cursor.fetchall()
    for s in stations:
        print(s)

    return stations


def find_measures(cursor, ID_st):

    y = int(datetime.datetime.now().year)
    if y > 9999 or y < 2021:
        print(''.format(y))
        y = 2022
    
    inject = "SELECT distinct t3.meas_name, t3.ID_measurement FROM testing.dbo.process t1 WITH(NOLOCK) "
    inject +="left join testing.dbo.MeasTable t2 WITH(NOLOCK) on t1.ID = t2.ID_process "
    inject +="left join testing.dbo._measurements t3 WITH(NOLOCK) on t2.ID_measurement = t3.ID_measurement "
    inject +="WHERE ID_bench={} AND t1.StartTime > '{}-01-01'".format(int(ID_st), str(y))
            
    print('[SQL] {}'.format(inject))
    cursor.execute(inject)
    measures = cursor.fetchall()
    
    return measures


def show_schema(cursor): #DEBUGING

    #cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='MeasTable'")
    # [('ID_item', ), ('ID_process', ), ('ID_measurement', ), ('Value', ), ('ValueStr', ), ('LimitMin', ), ('LimitMax', ), ('result', ), ('LimitStr', )]

    #cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='_measurements'")
    # [('ID_measurement', ), ('meas_name', ), ('units', ), ('optional', ), ('ID_FS_measGroup', )]
    
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='_measurements'")
    row = cursor.fetchall()
    for r in row:
        print(r)
        
    #inject = "SELECT * FROM testing.dbo._product WITH(NOLOCK) "
    #inject +="WHERE ID_product={}".format(int(82989))    
    
    pass

# ID_st=815 mic='XYZ30+11RFXY'
def get_mic_plus_lcd(cursor, ID_st, mic): # DEBUGING
    inject = "SELECT t1.StartTime, t1.NIP_code, t2.ID_measurement, t3.meas_name, t2.ValueStr, t1.ID FROM testing.dbo.process t1 WITH(NOLOCK) "
    inject +="LEFT JOIN testing.dbo.MeasTable t2 WITH(NOLOCK) ON t1.ID = t2.ID_process "
    inject +="LEFT JOIN testing.dbo._measurements t3 WITH(NOLOCK) ON t2.ID_measurement = t3.ID_measurement "
    inject +="WHERE ID_bench={} ".format(int(ID_st))
    inject +="AND t1.NIP_code='{}' ".format(mic)
    inject +="AND t2.ID_measurement IN ("
    inject +="SELECT ID_measurement FROM testing.dbo._measurements WITH(NOLOCK) WHERE meas_name in ("
    inject += "'LCD_CODE'"
    inject +=")) ORDER BY t1.StartTime DESC"
    
    print(inject)
    cursor.execute(inject)
    data = cursor.fetchall()
    print(len(data))
    
    for i in data:
        print(i)
    

def get_top_measures_data(cursor, ID_st, measuresName, Top, PresentTime):
    
    # [('ID', ), ('NIP_code', ), ('ID_bench', ), ('Num_position', ), ('ID_product', ), ('ID_cycle', ), 
    #  ('StartTime', ), ('Duration', ), ('ID_result', ), ('ReportPath', ), ('ID_User', ), ('pseudo_Fail', ), 
    #  ('real_Fail', ), ('first_data', ), ('last_data', ), ('parrentID', )]

    inject = "SELECT TOP {} t1.StartTime, t1.NIP_code, t1.Num_position, t2.result, t2.ID_measurement, t3.meas_name, t2.Value, t2.LimitMin, t2.LimitMax, t1.ID, t0.optional_1 FROM testing.dbo.process t1 WITH(NOLOCK) ".format(Top)
    inject +="LEFT JOIN testing.dbo._product t0 WITH(NOLOCK) ON t1.ID_product = t0.ID_product "
    inject +="LEFT JOIN testing.dbo.MeasTable t2 WITH(NOLOCK) ON t1.ID = t2.ID_process "
    inject +="LEFT JOIN testing.dbo._measurements t3 WITH(NOLOCK) ON t2.ID_measurement = t3.ID_measurement "
    inject +="WHERE ID_bench={} ".format(int(ID_st))
    inject +="AND t1.StartTime > '{}' ".format(PresentTime)
    #inject +="AND NOT t2.Value=None "
    inject +="AND t2.ID_measurement IN ("
    inject +="SELECT ID_measurement FROM testing.dbo._measurements WITH(NOLOCK) WHERE meas_name in ("
    
    for m in measuresName:
        inject += "'{}',".format(str(m))
        
    inject = inject[:-1]
    inject +=")) ORDER BY t1.StartTime DESC, t1.NIP_code" #NAJNOVSIE DATA, PODLA NIP
    #inject +=")) ORDER BY t2.ID_measurement, t1.StartTime"

    print(inject)
    cursor.execute(inject) 
    data = cursor.fetchall()
    print(len(data))
    
    # revers array of data last will by newer
    for i in range(len(data) // 2):
        data[i], data[-1 - i] = data[-1 - i], data[i]    
    # sorted by ID_measurement
    data = sorted(data, key=lambda x: x[4], reverse=False)
    return data

def find_fails(cursor, array_id_process):
    
    if len(array_id_process) > 0:
        inject = "SELECT t1.ID_process, t1.result, t1.Value, t1.LimitMin, t1.LimitMax, t2.meas_name, t2.ID_measurement FROM testing.dbo.MeasTable t1 WITH(NOLOCK) "
        inject += "LEFT JOIN testing.dbo._measurements t2 WITH(NOLOCK) ON t1.ID_measurement = t2.ID_measurement "
        inject += "WHERE t1.result='False'"
        inject += "AND t1.ID_process IN ("
        for i in array_id_process:
            inject += "{},".format(str(i))
        
        inject = inject[:-1]
        inject +=")"

        print(inject)
        cursor.execute(inject)
        fdata = cursor.fetchall()
    else:
        fdata = []
        
    return fdata    
    

def get_measures_data(cursor, only_pass, ID_st, measuresName, StartTime, StopTime):
    
    # [('ID', ), ('NIP_code', ), ('ID_bench', ), ('Num_position', ), ('ID_product', ), ('ID_cycle', ), 
    #  ('StartTime', ), ('Duration', ), ('ID_result', ), ('ReportPath', ), ('ID_User', ), ('pseudo_Fail', ), 
    #  ('real_Fail', ), ('first_data', ), ('last_data', ), ('parrentID', )]

    inject = "SELECT t1.StartTime, t1.NIP_code, t1.Num_position, t2.result, t2.ID_measurement, t3.meas_name, t2.Value, t2.LimitMin, t2.LimitMax, t1.ID, t0.optional_1 FROM testing.dbo.process t1 WITH(NOLOCK) "
    inject +="LEFT JOIN testing.dbo._product t0 WITH(NOLOCK) ON t1.ID_product = t0.ID_product " # line in testing
    inject +="LEFT JOIN testing.dbo.MeasTable t2 WITH(NOLOCK) ON t1.ID = t2.ID_process "
    inject +="LEFT JOIN testing.dbo._measurements t3 WITH(NOLOCK) ON t2.ID_measurement = t3.ID_measurement "
    inject +="WHERE ID_bench={} ".format(int(ID_st))
    inject +="AND t1.StartTime > '{}' ".format(StartTime)
    inject +="AND t1.StartTime < '{}' ".format(StopTime)
    
    if only_pass == 'False' or only_pass == 'True':
        inject +="AND t2.result='{}' ".format(only_pass) # 'False'/'True'/''
        
    inject +="AND t2.ID_measurement IN ("
    inject +="SELECT ID_measurement FROM testing.dbo._measurements WITH(NOLOCK) WHERE meas_name in ("
    
    for m in measuresName:
        inject += "'{}',".format(str(m))
        
    inject = inject[:-1]
    inject +=")) ORDER BY t3.meas_name, t1.StartTime" #t2.ID_measurement

    print(inject)
    cursor.execute(inject)
    data = cursor.fetchall()
    print(len(data))
    return data
    
    
def get_process_data(cursor, ID_st, StartTime, StopTime):
    # get data in process table ('pseudo_Fail', ), ('real_Fail', ), ('first_data', ), ('last_data', ),
    
    inject = "SELECT ID,NIP_code,pseudo_Fail,real_Fail,first_data,last_data,ID_cycle,Duration,ID_result FROM testing.dbo.Process WITH(NOLOCK) "
    inject +="WHERE ID_bench={} AND StartTime > '{}' AND StartTime < '{}'".format(int(ID_st), StartTime, StopTime)
    
    print(inject)
    cursor.execute(inject)
    data = cursor.fetchall()
    
    return data


def get_continuity_MIC(cursor): #DEBUGING
    # get data in process table ('pseudo_Fail', ), ('real_Fail', ), ('first_data', ), ('last_data', ),
    
    inject = "SELECT TOP 10 * FROM testing.dbo.MeasTable t1 WITH(NOLOCK) "# WHERE meas_name = 'LCD_CODE' "
    inject +="WHERE t1.ID_measurement = 14507332"
    #inject +="AND t1.StartTime > '{}' ".format('2022-04-30 23:59')
    #inject +="LEFT JOIN testing.dbo.MeasTable t2 WITH(NOLOCK) ON t1.ID = t2.ID_process "
    #inject +="LEFT JOIN testing.dbo._measurements t3 WITH(NOLOCK) ON t2.ID_measurement = t3.ID_measurement "
    #inject +="AND t2.ID_measurement IN ("
    #inject +="SELECT ID_measurement FROM testing.dbo._measurements WITH(NOLOCK) WHERE meas_name in ("
    #inject += "'{}'))".format(str('PowerMIC_readed'))
    
    
    print(inject)
    cursor.execute(inject)
    data = cursor.fetchall()
    
    return data


# bond je nazov pre program ktory robi korelacie medzi jednotlivimi meraniami
def bond_data(cursor,BOND_ID_st, BOND_ID_measurement): #DEBUGING treba?
    inject = "SELECT TOP 10 * FROM testing.dbo.MeasTable t1 WITH(NOLOCK) "# WHERE meas_name = 'LCD_CODE' "
    inject +="WHERE ID_bench={} AND t1.ID_measurement = {}".format(int(BOND_ID_st), BOND_ID_measurement)
    pass


# najdi dostupmne merania
# vstup do funkcie bude nazov projektu a nazov stanice
# Fukcia vrati zoznam merani.
def ai_find_id(): #DEBUGING
    conn, cursor = connection_sql()

    find_assy(cursor) # tag=1
    find_stations(cursor, ID_assy) #tag=2
    find_measures(cursor, ID_st) #tag=3
    
    cursor.close()
    conn.close()    
    
    
test = 0

if test > 0:
    conn, cursor = connection_sql()
    measuresName = []
    measuresName.append('F0')
    #measuresName.append('A_position_hight')
    #measuresName.append('A_position_width')
    #measuresName.append('A_position_gap')
    
    #StartTime_l = '2022-04-26 08:00'
    #StopTime_l = '2022-04-26 23:59'    
    #data = get_measures_data(cursor, 'True', 814, measuresName , '2022-04-26 08:00', '2022-04-26 23:59')
    # (530337266, '0W0005232227', 814, 2, 82989, 1, datetime.datetime(2022, 4, 26, 9, 1, 18), 137, 2, 'ELS\\2022\\04\\Porsche\\ST30\\220426\\08E1ST30\\0W0005232227_220426_090118.txt', 1, False, True, True, True, None)

    #data = get_process_data(cursor, 814, '2022-04-26 08:00', '2022-04-30 23:59')
    
    #data = get_top_measures_data(cursor, 598, measuresName, 1000, '2022-05-17 08:00')
    
    #data = get_continuity_MIC(cursor)
    #for d in data:
    #    #if 'LCD_CODE' in d[1].upper():
    #    print(d)
    
    #show_schema(cursor)
    
    ID_assy = find_assy(cursor)
    for a in ID_assy:
        print(a)
    
    find_stations(cursor, 75)
    #find_measures(cursor, ID_st)
    
    #ID_st=815
    #mic='XYZ30+11RFXY'
    #get_mic_plus_lcd(cursor, ID_st, mic)

    cursor.close()
    conn.close()
