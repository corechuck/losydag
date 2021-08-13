# Losydag

Logic driven synthetic data generator:

There are features inside that data set like autoincrement that works, or deriving which tables have to be generated like Table.Ref1 (curently just single depth) and others

Example output (without dependencies):
```
(base) C:\work\Import_onto_project> cd c:\work\Import_onto_project && cmd /C "set "PYTHONIOENCODING=UTF-8" && set "PYTHONUNBUFFERED=1" && C:\ProgramData\Miniconda3\python.exe c:\Users\rkorczak\.vscode\extensions\ms-python.python-2020.6.91350\pythonFiles\ptvsd_launcher.py --default --client --host localhost --port 64330 C:\work\Import_onto_project\source\MainSandRun.py "
INFO: Running Ontology
* Owlready2 * Running HermiT...
    java -Xmx2000M -cp C:\ProgramData\Miniconda3\lib\site-packages\owlready2\hermit;C:\ProgramData\Miniconda3\lib\site-packages\owlready2\hermit\HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///C:/Users/rkorczak/AppData/Local/Temp/tmpkn_ymvq4 -Y
* Owlready2 * HermiT took 5.28425407409668 seconds
* Owlready * (NB: only changes on entities loaded in Python are shown, other changes are done but not listed)
INFO: Reasoned with pellet.
# Realization case:
INFO: Referenced tables: {dependent_onto.Table.Test2, dependent_onto.Table.Test1, dependent_onto.Table.Ref_01}
* Owlready2 * Running HermiT...
    java -Xmx2000M -cp C:\ProgramData\Miniconda3\lib\site-packages\owlready2\hermit;C:\ProgramData\Miniconda3\lib\site-packages\owlready2\hermit\HermiT.jar org.semanticweb.HermiT.cli.CommandLine -c -O -D -I file:///C:/Users/rkorczak/AppData/Local/Temp/tmplbbbx7j2 -Y
* Owlready2 * HermiT took 5.37617039680481 seconds
* Owlready * Adding relation dependent_onto.Min.Table_ref1_temp_27579 is_constraining_tables dependent_onto.Table.Ref_01
* Owlready * (NB: only changes on entities loaded in Python are shown, other changes are done but not listed)
INFO: Result based on: RealizationCase.Check1
INFO: Evaluating Realization.Test1.first:
INFO: Realizing : Realization.Test1.first
INFO: Evaluating Realization.Test2.first_colors:
INFO: Realizing : Realization.Test2.first_colors
INFO: Evaluating Realization.Test2.second_directions:
INFO: Realizing : Realization.Test2.second_directions
INFO: Evaluating Realization.Test3.first:
INFO: Not ready : Realization.Test3.first
INFO: Evaluating Min.Table_ref1_temp_27579:
INFO: Realizing : Min.Table_ref1_temp_27579
INFO: Evaluating Realization.Test1.first:
INFO: Already realized : Realization.Test1.first
INFO: Evaluating Realization.Test2.first_colors:
INFO: Already realized : Realization.Test2.first_colors
INFO: Evaluating Realization.Test2.second_directions:
INFO: Already realized : Realization.Test2.second_directions
INFO: Evaluating Realization.Test3.first:
INFO: Realizing : Realization.Test3.first
INFO: Evaluating Min.Table_ref1_temp_27579:
INFO: Already realized : Min.Table_ref1_temp_27579
{ 'Table.Ref_01': [{'Col0_id': '1444', 'Col1_range': '-55858'}],
  'Table.Test1': [ { 'Col0_id': 'temp_673_1',
                     'Col1_n': '14',
                     'Col2_d': '1988-06-30',
                     'Col3_text': 'Tree',
                     'Col4_not_constrained': None}],
  'Table.Test2': [ { 'Col0_id': 'tab2_1_0014',
                     'Col1_n': '555',
                     'Col2_d': '2019-07-08',
                     'Col3_text': 'black',
                     'Col4_formatted': 'black',
                     'Col5_external_dep': 'temp_673_1'},
                   { 'Col0_id': 'tab2_2_7540',
                     'Col1_n': '444',
                     'Col2_d': '2013-03-07',
                     'Col3_text': 'towards',
                     'Col4_formatted': 'towards',
                     'Col5_external_dep': 'temp_673_1'}],
  'Table.Test3': [ { 'Col0_id': '5035579',
                     'Col1_tbl2_reference': 'tab2_1_0014',
                     'Col2_property1_number': '1444'}]}
----------------------------
{ 'Table.Ref_01': [{'Col0_id': '1284', 'Col1_range': '-35694'}],
  'Table.Test1': [ { 'Col0_id': 'temp_45Q_2',
                     'Col1_n': '14',
                     'Col2_d': '1988-06-30',
                     'Col3_text': 'Rock',
                     'Col4_not_constrained': None}],
  'Table.Test2': [ { 'Col0_id': 'tab2_3_7182',
                     'Col1_n': '333',
                     'Col2_d': '2019-07-08',
                     'Col3_text': 'black',
                     'Col4_formatted': 'black',
                     'Col5_external_dep': 'temp_45Q_2'},
                   { 'Col0_id': 'tab2_4_3039',
                     'Col1_n': '333',
                     'Col2_d': '2017-05-29',
                     'Col3_text': 'down',
                     'Col4_formatted': 'down',
                     'Col5_external_dep': 'temp_45Q_2'}],
  'Table.Test3': [ { 'Col0_id': '235038700',
                     'Col1_tbl2_reference': 'tab2_3_7182',
                     'Col2_property1_number': '1284'}]}
----------------------------
{ 'Table.Ref_01': [{'Col0_id': '1035', 'Col1_range': '-37958'}],
  'Table.Test1': [ { 'Col0_id': 'temp_Oj7_3',
                     'Col1_n': '14',
                     'Col2_d': '1986-03-18',
                     'Col3_text': 'Rock',
                     'Col4_not_constrained': None}],
  'Table.Test2': [ { 'Col0_id': 'tab2_5_5642',
                     'Col1_n': '333',
                     'Col2_d': '2013-03-07',
                     'Col3_text': 'red',
                     'Col4_formatted': 'red',
                     'Col5_external_dep': 'temp_Oj7_3'},
                   { 'Col0_id': 'tab2_6_6164',
                     'Col1_n': '555',
                     'Col2_d': '2017-05-29',
                     'Col3_text': 'towards',
                     'Col4_formatted': 'towards',
                     'Col5_external_dep': 'temp_Oj7_3'}],
  'Table.Test3': [ { 'Col0_id': '9663',
                     'Col1_tbl2_reference': 'tab2_5_5642',
                     'Col2_property1_number': '1035'}]}
----------------------------
{ 'Table.Ref_01': [{'Col0_id': '1419', 'Col1_range': '-43763'}],
  'Table.Test1': [ { 'Col0_id': 'temp_JST_4',
                     'Col1_n': '14',
                     'Col2_d': '1986-03-18',
                     'Col3_text': 'Tree',
                     'Col4_not_constrained': None}],
  'Table.Test2': [ { 'Col0_id': 'tab2_7_9831',
                     'Col1_n': '444',
                     'Col2_d': '2019-07-08',
                     'Col3_text': 'orange',
                     'Col4_formatted': 'orange',
                     'Col5_external_dep': 'temp_JST_4'},
                   { 'Col0_id': 'tab2_8_1293',
                     'Col1_n': '444',
                     'Col2_d': '2013-03-07',
                     'Col3_text': 'up',
                     'Col4_formatted': 'up',
                     'Col5_external_dep': 'temp_JST_4'}],
  'Table.Test3': [ { 'Col0_id': '52856',
                     'Col1_tbl2_reference': 'tab2_7_9831',
                     'Col2_property1_number': '1419'}]}
----------------------------
{ 'Table.Ref_01': [{'Col0_id': '1297', 'Col1_range': '-30338'}],
  'Table.Test1': [ { 'Col0_id': 'temp_ZeV_5',
                     'Col1_n': '32',
                     'Col2_d': '1986-03-18',
                     'Col3_text': 'Rock',
                     'Col4_not_constrained': None}],
  'Table.Test2': [ { 'Col0_id': 'tab2_9_1342',
                     'Col1_n': '444',
                     'Col2_d': '2019-07-08',
                     'Col3_text': 'blue',
                     'Col4_formatted': 'blue',
                     'Col5_external_dep': 'temp_ZeV_5'},
                   { 'Col0_id': 'tab2_10_4442',
                     'Col1_n': '444',
                     'Col2_d': '2013-03-07',
                     'Col3_text': 'down',
                     'Col4_formatted': 'down',
                     'Col5_external_dep': 'temp_ZeV_5'}],
  'Table.Test3': [ { 'Col0_id': '93802',
                     'Col1_tbl2_reference': 'tab2_9_1342',
                     'Col2_property1_number': '1297'}]}
```
