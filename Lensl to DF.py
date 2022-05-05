# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 08:45:02 2022

@author: edvar
"""
import pandas as pd
import jsonlines
import json
#import multiprocessing
'''do not recomend recreating the the dataframes from base data, as process arranging the date into edge list
within dataframes are very time consuming'''
path_or_buf = 'D:/OneDrive/Python/Master/Patent test/Export_test.jsonl'
path_FCV = 'D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/FCV-Export-Lens.jsonl'
path_Json = 'D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/FCV-Export-Lens.jsonl'
def JsonLRead(path):
    List_of_patent_dictionaries = []
    with jsonlines.open(path) as reader:
        for obj in reader:
            List_of_patent_dictionaries.append(obj)
    reader.close()
    return List_of_patent_dictionaries
Lidar_test_list = JsonLRead(path_or_buf)
List_of_patent_dictionaries = JsonLRead(path_FCV)
def Unpack_ITI(list_of_dicts):
    Inv_Inv_edges = pd.DataFrame(columns=['Inventor_I', 'Inventor_J','Inventor_I_R', 'Inventor_J_R', 'Patent_J+NR'])
   
    for Dict in list_of_dicts:
        Patent_biblo =  Dict['biblio']
        jur = Patent_biblo['application_reference']['jurisdiction']
        doc_number = Patent_biblo['application_reference']['doc_number']
        #applicants =  Patent_biblo['parties']['applicants']
        if 'inventors' in Patent_biblo['parties']:
            inventors = Patent_biblo['parties']['inventors']
            if 'residence' and 'extracted_name'  in (inventors[0]):
                for inv_i in inventors:
                    for inv_j in inventors:
                        if 'residence' and 'extracted_name' in inv_i and inv_j:
                            if inv_i != inv_j:
                                index = Inv_Inv_edges.shape[0]
                                if 'residence' in inv_i:
                                    if 'residence' in inv_j:
                                        Inv_Inv_edges.at[index, 'Inventor_I'] = inv_i['extracted_name']['value']
                                        Inv_Inv_edges.at[index, 'Inventor_J'] = inv_j['extracted_name']['value']    
                                        Inv_Inv_edges.at[index, 'Inventor_I_R'] = inv_i['residence']
                                        Inv_Inv_edges.at[index, 'Inventor_J_R'] = inv_j['residence']
                                        Inv_Inv_edges.at[index, 'Patent_J+NR'] = jur+' '+doc_number
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                        else: 
                            pass
            else:
                pass
        else:
            pass
        '''for inv_i in inventors:
            for inv_j in inventors:
                index = Inv_Inv_edges.shape[0]
                Inv_Inv_edges.at[index, 'Inventor_I'] = inv_i['extracted_name']['value']
                Inv_Inv_edges.at[index, 'Inventor_J'] = inv_j['extracted_name']['value']
                if 'residence' in inv_i:
                    Inv_Inv_edges.at[index, 'Inventor_I_R'] = inv_i['residence']
                else: 
                    pass
                if 'residence' in inv_j: 
                    Inv_Inv_edges.at[index, 'Inventor_J_R'] = inv_j['residence']
                else: 
                    pass
                Inv_Inv_edges.at[index, 'Patent_J+NR'] = jur+' '+doc_number'''
    return Inv_Inv_edges
test = Unpack_ITI(List_of_patent_dictionaries)   
IxI_edge = test 
          
def Unpack_ITA(list_of_dicts):
    Inv_Ap_eges = pd.DataFrame(columns=['Inventor', 'Applicant','Inventor_R', 'Applicant_R', 'Patent_J+NR'])
    for Dict in list_of_dicts:
        Patent_biblo =  Dict['biblio']
        jur = Patent_biblo['application_reference']['jurisdiction']
        doc_number = Patent_biblo['application_reference']['doc_number']
        if 'applicants' in Patent_biblo['parties']:
            if 'inventors' in Patent_biblo['parties']:
                
                applicants =  Patent_biblo['parties']['applicants']
                inventors = Patent_biblo['parties']['inventors']
                for ap in applicants:
                    for inv in inventors:
                        if 'residence' in inv:
                            
                            index = Inv_Ap_eges.shape[0]
                            Inv_Ap_eges.at[index, 'Inventor'] = inv['extracted_name']['value']
                            Inv_Ap_eges.at[index, 'Applicant'] = ap['extracted_name']['value']
                            Inv_Ap_eges.at[index, 'Inventor_R'] = inv['residence']
                            if 'residence' in ap:
                                Inv_Ap_eges.at[index, 'Applicant_R'] = ap['residence']
                            else:
                                Inv_Ap_eges.at[index, 'Applicant_R'] = 'TBD'
                            Inv_Ap_eges.at[index, 'Patent_J+NR'] = jur+' '+doc_number
                    else:
                        pass
            else:
                pass
        else:
            pass
    return Inv_Ap_eges
IXA_edge = Unpack_ITA(List_of_patent_dictionaries)
'''def Unpack_Node_A(list_of_dicts):
    Nodes_app = pd.DataFrame(columns=['Actor', 'Residency'])
    for Dict in list_of_dicts:
        Patent_biblo =  Dict['biblio']
        #jur = Patent_biblo['application_reference']
        #doc_number = Patent_biblo['application_reference']
        applicants =  Patent_biblo['parties']['applicants']
        #inventors = Patent_biblo['parties']['inventors']
        for app in applicants:
            index = Nodes_app.shape[0]
            Nodes_app.at[index, 'Actor'] = app['extracted_name']['value']
            Nodes_app.at[index, 'Residency'] = app['residence']


def Unpack_Node_I(list_of_dicts):
    Nodes_inv = pd.DataFrame(columns=['Actor', 'Residency'])
    for Dict in list_of_dicts:
        Patent_biblo =  Dict['biblio']
        #jur = Patent_biblo['application_reference']
        #doc_number = Patent_biblo['application_reference']
        #applicants =  Patent_biblo['parties']['applicants']
        inventors = Patent_biblo['parties']['inventors']
        for inv in inventors:
            index = Nodes_inv.shape[0]
            Nodes_inv.at[index, 'Actor'] = inv['extracted_name']['value']
            Nodes_inv.at[index, 'Residency'] = inv['residence']
    return
'''
#to save the structured data set
IXA_edge.to_excel('IXA_edge_MP.xlsx')
IxI_edge.to_excel('IXI_edge_MP.xlsx')


def ITAR(IXA_DF): #searches for Residency from other patents or from inventor side
    T_index = IXA_DF.shape[0]
    for i in range(T_index):
        if IXA_DF.at[i,'Applicant_R'] == 'TBD':
            Ap = IXA_DF.at[i, 'Applicant']
            for j in range(T_index): 
                if IXA_DF.at[j,'Inventor'] == Ap:
                    IXA_DF.at[i,'Applicant_R'] = IXA_DF.at[j,'Inventor_R']
                elif IXA_DF.at[j,'Applicant'] == Ap:
                    if IXA_DF.at[j,'Applicant_R'] != 'TBD':
                        IXA_DF.at[i, 'Applicant_R'] = IXA_DF.at[j,'Applicant_R']
    return IXA_DF
IXA_Cedge = ITAR(IXA_edge)
IXA_Cedge.to_excel('IXA_Cedge_MP.xlsx')


IXA_CedgeR = pd.read_excel('IXA_Cedge_MP.xlsx')
IxI_edgeR = pd.read_excel('IXI_edge_MP.xlsx')
IXA_OG = pd.read_excel('IXA_edge_MP.xlsx')


#df[df[''] == 'TBD']        

IXA_Test = IXA_CedgeR[IXA_CedgeR['Applicant_R'] == 'TBD']
def ITAR02(IXA_DF): #More efficent version of ITAR - but current version will only look at the inventor side - use for second round
    IXA_DF_out = IXA_DF
    #AIR = []
    for i in IXA_DF[IXA_DF['Applicant_R'] == 'TBD'].index:
        for j in IXA_DF[IXA_DF['Applicant_R'] == 'TBD'].index:
            if IXA_DF.loc[i,'Applicant'].strip('.').replace('. ',' ').replace(', ',' ').strip(' ') == IXA_DF.loc[j,'Inventor']:
                IXA_DF_out.at[i, 'Applicant_R'] = IXA_DF.loc[j, 'Inventor_R']
                #AIR.append([IXA_DF.loc[j, 'Inventor_R']])
    return IXA_DF_out
def TBD_Values(Df):
    TBD = Df[Df['Applicant_R']=='TBD']
    return TBD 
IXA_CedgeR2S = ITAR02(IXA_CedgeR)
'''
IXA_TBD_R2S = TBD_Values(IXA_CedgeR2S)
for i in IXA_CedgeR[IXA_CedgeR['Applicant_R'] == 'TBD'].index:
    for j in IXA_CedgeR[IXA_CedgeR['Applicant_R'] == 'TBD'].index:
        if IXA_CedgeR['Applicant'][i] == IXA_CedgeR['Inventor'][j]+'.':
            print('go')
'''
List_Manual_clean = { #will only correct Applicant_R - will not correct typos or missmatches between inventor and applicant names due to signs such as ,.:; as it will not make much of a difference
    "O'BRIEN JOHN F.":['US',"O'BRIEN JOHN F"], #[R, Change to Inventor, Change to Applicant]
    'GOMEZ RODOLFO A.M.':['AU','GOMEZ RODOLFO A M'],
    'BRUCK ROLF' : ['DE','','BRUECK ROLF'], # Assume that 'BRUCK ROLF' and 'BRUECK ROLF' is the same person and that there is a type somewhere
    'AEROVIRONMENT INC A CALIFORNIA' : ['US'], # In the name
    'NISSAN TECHNICAL CT N A INC':['US'], #North american Technical center beloning Nissan https://virginiadb.com/company/F1574997/nissan-technical-center-north-america-inc.html
    'SEARETE LLC':['US'], #https://www.lens.org/lens/patent/191-983-161-609-279/frontpage?l=en
    'NG CASEY Y.K.':['US','NG CASEY Y K'], # NG CASEY Y K == NG CASEY Y.K. where not included in the strips and replace functions used in ITAR02
    'SCHNECK MICHAEL M.':['US','SCHNECK MICHAEL M'], #SCHNECK MICHAEL M == SCHNECK MICHAEL M. 
    'PARISE; RONALD J.':['US','PARISE RONALD J'], # PARISE RONALD J == PARISE; RONALD J.
    'BURNS; DAVID JOHNSTON':['GB','BURNS DAVID JOHNSTON'], #BURNS DAVID JOHNSTON == BURNS; DAVID JOHNSTON
    'DEWEY SCOTT B.':['US','DEWEY SCOTT B'], #'DEWEY SCOTT B' == 'DEWEY SCOTT B.'
    'VAN-DRENTHAM-SUSMAN HECTOR FILIPUS ALEXANDER':['GB','VAN-DRENTHAM-SUSMAN HECTOR FIL'], # VAN-DRENTHAM-SUSMAN HECTOR FIL == VAN-DRENTHAM-SUSMAN HECTOR FILIPUS ALEXANDER
    'AGAR DAVID W.':['DE','AGAR DAVID W'], # AGAR DAVID W. == AGAR DAVID W 
    'COLORADO SCHOOL OF MINES':['US'], # Name of applicant
    'OLEAGORDIA AGUIRRE INIGO JAVIE':['ES','','OLEAGORDIA AGUIRRE INIGO JAVIER'], # OLEAGORDIA AGUIRRE INIGO JAVIE == OLEAGORDIA AGUIRRE INIGO JAVIER - probably a typo
    'SCHOULTZ; ROGER A.':['US','SCHOULTZ; ROGER A'], #SCHOULTZ; ROGER A. = SCHOULTZ; ROGER A
    'NIELSON; JAY P.':['US','NIELSON; JAY P'], # NIELSON; JAY P. == NIELSON; JAY P
    'DODGE; CLEVELAND E.':['US','DODGE CLEVELAND E'],
    'WENZEL JOACHIM':['DE','WENZEL JOACHIM DIPL ING'],
    'KONIECZNY JORG-ROMAN':['DE','', 'KONIECZNY JOERG-ROMAN'],
    'NI; XUAN Z.':['US','NI XUAN Z'],
    'BECHTEL BWXT IDAHO LLC':['US'], # State name included in name
    'KAGATANI TAKEO':['JP'], #Only one applicant and only one Inventor probably only a typo
    'KAGATANI; TAKEO':['JP','','KAGATANI TAKEO'],
    'CLINGERMAN BRUCE J.':['US','CLINGERMAN BRUCE J'],
    'CRANE SAMUEL N.':['US','CRANE SAMUEL N'],
    'MARGIOTT PAUL R.':['US','MARGIOTT PAUL R'],
    'SIMMONS, JR.; TIMOTHY C.':['US','SIMMONS JR TIMOTHY C'],
    'HARRIS DONALD B.':['US','HARRIS DONALD B'],
    'MEACHAM G.B. KIRBY':['US', 'MEACHAM G B KIRBY'],
    'GRIEVE M. JAMES':['US','GRIEVE M JAMES'],
    'WEBSTER BRUCE A.':['US','WEBSTER BRUCE A'],
    'YOUNG ROSA T.':['US','YOUNG ROSA T'],
    'C MAR HOLDINGS LTD':['GB'], #https://find-and-update.company-information.service.gov.uk/company/02974834
    'SANDERSON, JR WILLIAM':['US','SANDERSON JR WILLIAM'],
    'STUART ANDREW T.B.':['CA','STUART ANDREW T B'],
    'LAWRENCE LIVERNORE NAT SECURIT':['US'], #https://www.llnsllc.com/
    'HARRINGTON MICHAEL D.':['US','HARRINGTON MICHAEL D'],
    'SWANSON KYLE D.':['US','SWANSON KYLE D'],
    'ROGERS STEPHEN P.':['US','ROGERS STEPHEN P'],
    'NASHBURN RICHARD F.':['US','NASHBURN RICHARD F'],
    'THIJSSEN JOHANNES H.J.':['US','THIJSSEN JOHANNES H J'],
    "O'HARA JEANETTE E.":['US',"O'HARA JEANETTE E"],
    'FARIS SADEG M.':['US','FARIS SADEG M'],
    'MOTSENBOCKER MARVIN A.':['US','MOTSENBOCKER MARVIN A'],
    'ERDLE ERICH K.':['DE','ERDLE ERICH K'],
    'HOLMES CHARLES M.':['US','HOLMES CHARLES M'],
    'GABRIEL JEAN-CHRISTOPHE P.':['US','GABRIEL JEAN-CHRISTOPHE P'],
    'YANG JEFFERSON Y.':['US','YANG JEFFERSON Y'],
    'BLUNK RICHARD H.':['US','BLUNK RICHARD H'],
    'GUANGDONG HYDROGEN ENERGY SCIENCE AND TE':['CN'], #Institute name indicates residency
    'HARPER MATTHEW ALBERT MACLENNAN':['CA','HARPER MATTHEW ALBERT MACLENNA'],
    'SHABANA MOHSEN D.':['US','SHABANA MOHSEN D'],
    'VOSS HENRY H.':['CA','VOSS HENRY H'],
    'JENSEN; MAURICE W.': ['US','JENSEN MAURICE W'],
    'NELSON PATRICIA J.':['US','NELSON PATRICIA J']
    }
''' 
Note for later, Large parts of the dict above could have been generated automaticly, 
the strings in Inventor and Applicant had been tokenized (splitt into its respective parts,
splitting at ' ' and removed all probmematic signs [,.;:]), for repeat automate this process and limit data entry to typos and large firms
'''
# A list of dictionaries that contains the corrections to Applicant residency, based on either data allredy avaible in IXA_CedgeR2S or on web searcher of company names

def Incorperate_Cleaning_Dic_IXA(Dic, DF):
    for i in DF[DF['Applicant_R']=='TBD'].index:
        if len(Dic[DF.loc[i,'Applicant']]) == 1: #Instituional and Corparate Applicant only - residency is changed
            DF.at[i,'Applicant_R'] = Dic[DF.loc[i,'Applicant']][0] 
        elif len(Dic[DF.loc[i,'Applicant']]) == 2: # Ensure homogenity in spell of the Inventors as when they are written up as in addition to specefing Applicant residency
            Inven = Dic[DF.loc[i,'Applicant']][1]
            DF.at[i,'Applicant_R'] = Dic[DF.loc[i,'Applicant']][0]
            for j in DF[DF['Inventor'] == Inven].index:
                DF.at[j, 'Inventor'] = DF.loc[i,'Applicant']
        elif len(Dic[DF.loc[i,'Applicant']]) == 3:
            DF.at[i,'Applicant_R'] = Dic[DF.loc[i,'Applicant']][0]
            DF.at[i,'Applicant'] = Dic[DF.loc[i,'Applicant']][2]
    return DF
IXA_CedgeR3 = Incorperate_Cleaning_Dic_IXA(List_Manual_clean, IXA_CedgeR2S)
IXA_CedgeR3.to_csv('IXA_cleaned.csv')

def Incorperate_Cleaning_Dic_IXI (Dic, DF): #is meant to sync IXI up with the changes made to IXA
    for i in Dic.keys():
        if len(Dic[i]) == 2:
            Inv_cor = Dic[i][1]
            for j in DF[DF['Inventor_I'] == Inv_cor].index:
                DF.at[j, 'Inventor_I'] = str(i)
            for j in DF[DF['Inventor_J'] == Inv_cor].index:
                DF.at[j, 'Inventor_J'] = str(i) 
    return DF
IxI_edgeR2 = Incorperate_Cleaning_Dic_IXI(List_Manual_clean, IxI_edgeR)

IxI_edgeR2.to_csv('IxI_cleaned.csv')
IxI_cleaned = pd.read_csv('IxI_cleaned.csv')
IxA_cleaned = pd.read_csv('IXA_cleaned.csv')
'''Now that the edge lists has been fully built and cleand to only contain usable data,
we must add new columns to indicate whether the edge was limited with the national boards or external,
in addition to a Node list and Dataframe that for the nations in order to calculate the nationaliation index based on
the data we have on internal and external edges'''

#Prep for gephi
IxI_cleaned = IxI_cleaned.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
IxA_cleaned = IxA_cleaned.drop(columns=['Unnamed: 0','Unnamed: 0.1'])
'''create a function that will remove casesin which Inventor I == Inventor J '''

#prep for UCI
IxI_cleaned.rename(columns= {'Inventor_I':'Source','Inventor_J':'Target'}).drop(columns = ['Inventor_I_R', 'Inventor_J_R','Patent_J+NR']).to_excel('IXI_FUCI.xlsx')
IxA_cleaned.rename(columns={'Inventor':'Source','Applicant':'Target'}).drop(columns = ['Inventor_R', 'Applicant_R', 'Patent_J+NR']).set_index('Source').to_csv('IXA_FUCI.csv')


def Creat_AXA(AxI): #considerd to include AXA but the generation process takes too much time and strictly not needed
    AxA = pd.DataFrame()
    for i in set(AxI['Patent_J+NR']):
        Patent_sub = AxI[AxI['Patent_J+NR'] == i]
        for j in Patent_sub.index: # sets Applicant I
            for k in Patent_sub.index: # sets applicant J 
                NIV = AxA.shape[0] #New index value
                if Patent_sub.loc[k,'Applicant'] != Patent_sub.loc[j, 'Applicant']:
                    AxA.at[NIV, 'Applicant_I'] = Patent_sub.loc[j,'Applicant']
                    AxA.at[NIV, 'Applicant_J'] = Patent_sub.loc[k,'Applicant']
                    AxA.at[NIV, 'Applicant_IR'] = Patent_sub.loc[j,'Applicant_R']
                    AxA.at[NIV, 'Applicant_JR'] = i
    return AxA
AXA = Creat_AXA(IxA_cleaned)
def Remove_Equal_node_edge(IXI): #where not used
    drop_row_list = IXI[IXI['Inventor_I'] == IXI['Inventor_J']].index
    for i in drop_row_list:
        IXI.drop(index= i)
    return IXI

IXI_FGephi =IxI_cleaned
IxI_cleaned.rename(columns= {'Inventor_I':'Source','Inventor_J':'Target'}).set_index('Source').to_csv('IXI_FGephi.csv')
IxI_cleaned.rename(columns= {'Inventor_I':'Source','Inventor_J':'Target'}).to_excel('IXI_FGephi.xlsx')

IxA_cleaned.rename(columns={'Inventor':'Source','Applicant':'Target'}).set_index('Source').to_csv('IXA_FGephi.csv')

#_______________________________________
def Link_classification_IXA(DF):
    for i in DF.index:
        if DF.loc[i,'Inventor_R'] == DF.loc[i,'Applicant_R']:
            DF.at[i,'IL'] = 1
            DF.at[i, 'EL'] = 0
        elif DF.loc[i,'Inventor_R'] != DF.loc[i, 'Applicant_R']:
            DF.at[i,'IL'] = 0
            DF.at[i, 'EL'] = 1
            
    return DF

def Link_classification_IXI(DF):
    for i in DF.index:
        if DF.loc[i,'Inventor_I_R'] == DF.loc[i,'Inventor_J_R']:
            DF.at[i,'IL'] = 1
            DF.at[i, 'EL'] = 0
        elif DF.loc[i,'Inventor_I_R'] != DF.loc[i, 'Inventor_J_R']:
            DF.at[i,'IL'] = 0
            DF.at[i, 'EL'] = 1
            
    return DF
IxI_cleanedwL = Link_classification_IXI(IxI_cleaned)
IxA_cleanedwL = Link_classification_IXA(IxA_cleaned)
IxA_cleanedwL = IxA_cleaned
IxA_cleanedwL.to_csv('IxA_cleanedwL.csv')
IxI_cleanedwL.to_csv('IxI_cleanedwL.csv')


IxI_cleanedwL = pd.read_csv('IxI_cleanedwL.csv')
IxA_cleanedwL = pd.read_csv('IxA_cleanedwL.csv')
IxI_cleanedwL = IxI_cleanedwL.drop(columns='Unnamed: 0')
IxA_cleanedwL = IxA_cleanedwL.drop(columns='Unnamed: 0')

def Edge_to_Node(IXA):
    Nodes = pd.DataFrame(columns = ['Actor', 'Country'])
    for i in ['Inventor','Applicant']:
        for j in IXA.index:
            I = Nodes.shape[0]
            post_fix = '_R'
            Con = i + post_fix
            Nodes.at[I,'Actor'] = IXA.loc[j,i]
            Nodes.at[I,'Country'] = IXA.loc[j,Con]
    return Nodes.drop_duplicates(subset = ['Actor']) # replace with at set_index with drop = True
Nodes_df = Edge_to_Node(IxA_cleaned)
Nodes_df = Nodes_df.set_index('Actor')
Nodes_df.to_csv('Nodes_part1.csv')
Nodes = pd.read_csv('Nodes_part1.csv')
Nodes.rename(columns = {'Actor':'Id'}).set_index('Id').to_csv('Nodes_gephi.csv')

def Nation_DF_construction(IXA, IXI, Node):
    Countries = pd.DataFrame(Node['Country'])
    Countries = Countries.drop_duplicates(subset='Country')
    for i in Countries.index: 
        Sub_IXA = IXA[(IXA['Inventor_R'] == Countries.loc[i,'Country']) | (IXA['Applicant_R'] == Countries.loc[i,'Country'])] 
        Sub_IXI = IXI[IXI['Inventor_I'] == Countries.loc[i,'Country']] #change such that only Inventor I is considerd  
        for j in ['IL', 'EL']:
            Countries.at[i, j+' Sum'] = Sub_IXA[j].sum() + Sub_IXI[j].sum()
    Countries['Sum L'] = Countries['IL Sum'] + Countries['EL Sum']
    Countries['Nationalization index'] = (Countries['IL Sum']-Countries['EL Sum'])/(Countries['IL Sum'] + Countries['EL Sum'])
    #Nation_df = pd.DataFrame(columns = ['Country','NI'])
    
    return Countries.reset_index()
Nc_df = Nation_DF_construction(IxA_cleanedwL, IxI_cleanedwL, Nodes) 
NGTIS = Nc_df['Nationalization index'].mean()

def clique_i_j(IxA, IxI, List_of_set):
    return

def finder_2_clan(IxA, IxI, Nodes):
    # = {}
    df = pd.DataFrame(columns= ['I','J','Through', 'GD'])
    for node in Nodes['Actor'].values:
        #temp = {}
        print(node) #only included to make sure that function are running - can be seen as progress bar - could alternativly print (index_value/index.max)*100 to get an actual progress bar
        GD = 1
        IxA_sub =  IxA[IxA['Inventor'] == node]
        IxI_sub =  IxI[IxI['Inventor_I'] == node]
        IXI_J_set = set(IxI_sub['Inventor_J'].values)
        IxA_A_set = set(IxA_sub['Applicant'].values) # set up a program that will determin everything with a certain geostatic N reach of the intial node, take the intersect of these sets for all nod sets 
        for k in IxA_A_set.union(IXI_J_set):
            index_size = df.shape[0]
            df.at[index_size,'I'] = node
            df.at[index_size,'J'] = k
            df.at[index_size,'Through'] = 0
            df.at[index_size,'GD'] = GD
            IxA_sub_k =  IxA[IxA['Inventor'] == k]
            IxI_sub_k =  IxI[IxI['Inventor_I'] == k]
            for l in set(IxI_sub_k['Inventor_J'].values).union(set(IxA_sub_k['Applicant'].values)):
                GD = 2
                index_size = df.shape[0]
                df.at[index_size,'I'] = node
                df.at[index_size,'J'] = l
                df.at[index_size,'Through'] = k
                df.at[index_size,'GD'] = GD
    return df


'''def finder_3_clan(IxA, IxI, Nodes): # expanded verson will consider 3clan case - too computanaly heavy to be of any real us as it takes to much time
    # is too time consuming in its current format will drop in favor of a modular subsystem identifaction and classification built into GEPHI
    df = pd.DataFrame(columns= ['I','J','Through', 'GD'])
    for node in Nodes['Actor'].values:
        #temp = {}
        print(node,'has started processing ',(((Nodes[Nodes['Actor'] == node].index)/Nodes.index[-1])*100)[0],'%' ) #only included to make sure that function are running - can be seen as progress bar 
        GD = 1
        IxA_sub =  IxA[IxA['Inventor'] == node]
        IxI_sub =  IxI[IxI['Inventor_I'] == node]
        IXI_J_set = set(IxI_sub['Inventor_J'].values)
        IxA_A_set = set(IxA_sub['Applicant'].values) # set up a program that will determin everything with a certain geostatic N reach of the intial node, take the intersect of these sets for all nod sets 
        for k in IxA_A_set.union(IXI_J_set):
            index_size = df.shape[0]
            df.at[index_size,'I'] = node
            df.at[index_size,'J'] = k
            df.at[index_size,'Through'] = 0
            df.at[index_size,'GD'] = GD
            IxA_sub_k =  IxA[IxA['Inventor'] == k]
            IxI_sub_k =  IxI[IxI['Inventor_I'] == k]
            for l in set(IxI_sub_k['Inventor_J'].values).union(set(IxA_sub_k['Applicant'].values)):
                GD2 = 2
                index_size = df.shape[0]
                df.at[index_size,'I'] = node
                df.at[index_size,'J'] = l
                df.at[index_size,'Through'] = k
                df.at[index_size,'GD'] = GD2
                IxA_sub_l =  IxA[IxA['Inventor'] == l]
                IxI_sub_l =  IxI[IxI['Inventor_I'] == l]
                for m in set(IxI_sub_l['Inventor_J'].values).union(set(IxA_sub_l['Applicant'].values)):
                    GD3 = 3
                    index_size = df.shape[0]
                    df.at[index_size,'I'] = node
                    df.at[index_size,'J'] = m
                    df.at[index_size,'Through'] = l +', ' + k
                    df.at[index_size,'GD'] = GD3
    return df
'''
clan_finder_data = finder_2_clan(IxA_cleanedwL, IxI_cleanedwL, Nodes)
clan_finder_data.to_csv('Clan_input.csv')  
#Input_3clan = finder_3_clan(IxA_cleanedwL, IxI_cleanedwL, Nodes)      
def Find_sort_clan(data, Node):
    output_list = {}
    for node in set(data['I'].values):
        temp_val = []
        temp_names = []
        print('proccesing with ', node, ' as starting point')
        sub = data[data['I'] == node].sort_values('GD', ascending = True)
        node_GD2_set = set(sub['J'].values)
        if len(node_GD2_set) > 3: # will not consider set with less than 3 values
            for pot_clan in node_GD2_set:
                PC_set = set(data[data['I'] == pot_clan].sort_values('GD', ascending = True)['J'].values)
                if len(temp_val) == 0 & len(temp_names) == 0:
                    temp_val.append(node_GD2_set)
                    temp_names.append(node)
                    temp_val.append(PC_set)
                    temp_names.append(pot_clan)
                elif pot_clan in temp_val[0].intersection(*temp_val):
                    temp_val.append(PC_set)
                    temp_names.append(pot_clan)
                else: pass
            tempD_n = {}
            tempD_n['Nodes in clan'] = temp_names
            tempD_v = {}
            tempD_v['Reach set of Nodes in clan'] = temp_val
            # = temp_names[0][0] 
        output_list[node+' start'] = tempD_n, tempD_v
    return output_list
clan2 = Find_sort_clan(clan_finder_data)
#def cluster_name_genrator(names, Nodes):
  #  output = ''
  #  country_codes = []
    

with open('2clan_data.json','w') as outfile:
    json.dump(clan2, outfile)
with jsonlines.open('output.jsonl', mode='w') as writer:
    writer.write(...)
    
def mark_nodes_with_clan(nodes,clan_dic):
    for n in nodes.index:
        nodes.at[n, 'Clan'] = ''
    for key in clan2.keys():
        for actor in clan_dic[key][0]['Nodes in clan']:
            nodes.at[nodes[nodes['Actor'] == actor].index, 'Clan'] = nodes.loc[[nodes[nodes['Actor'] == actor].index, 'Clan']] + key.replace('start',' start')
    return nodes
nodesWc = mark_nodes_with_clan(Nodes, clan2)
nodesWc.to_csv('Nodes + dummy_clan.csv')
def drop_clan(dic): #remove duplicts
    drop_list = []
    for keyi in dic:
        for keyj in dic:
            if keyi != keyj:
                if dic[keyi][0]['Nodes in clan'] == dic[keyj][0]['Nodes in clan']:
                    if keyj  not in drop_list:
                        drop_list.append(keyj)
    for k in drop_list:
        dic.pop(k)
    return dic 
trimmed_clan = drop_clan(clan2)


def list_of_clans(dummy, Nodes):
    for clan in dummy.columns[2:]:
        for 