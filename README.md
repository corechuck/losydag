# Losydag

Logic driven synthetic data generator:

It is an engine which reads modelled database structure in ontology and parse a generation request sentence (GRS) (sql-like query) to generate data sets and break down of given logical sentence.
```
USES 'http://corechuck.com/modeling/dependent_onto'
GENERATE all cases
FOR Table.Test1 as realization_1
FOR Table.Test1 as realization_2
WHERE
    realization_1.Col1_n IN ('0.222', '0.111', '0.333')
    AND (
        realization_2.Col3_text IN ('aaa', 'bbb', 'ccc')
        OR realization_2.Col4_not_constrained MATCH 'Ref_\d\d\d'
    )
```

It allows commands like: 
```
    EXAMPLE_POSITIVE_CASES = "example positive cases"
    EXAMPLE_NEGATIVE_CASES = "example negative cases"
    POSITIVE_CASES = "positive cases"
    NEGATIVE_CASES = "negative cases"
    ALL_CASES = "all cases"
    EXAMPLE_ALL_CASES = "examples of all cases"
    EXAMPLE = "example"
```
Other queries that are worked on are in source/tests/query_language/test_queries/

There are features inside that data set like autoincrement that works, or deriving which tables have to be generated like Table.Ref1 (currently just single depth) and others

Example part of output (currently not showing directly which are positive and which are negative cases):
```
(base) C:\ProgramData\Miniconda3\python.exe C:/work/Import_onto_project/source/parse_and_process_query.py --onto-location resources/development/ --query-path source/tests/query_language/test_queries/query1_and.grs

(.. here is more logs what engine does ...)

INFO: Presenting excerpt from what datasets represent:
{ 'G1': { 'case_name': 'Positive_case__main_query__merged_with__1st_positive_case_of_query_group_from_line_7',
          'meta': 'No change main_query; Negated all, but chosen constraint_from_line_8 from OR group query_group_from_line_7 for positive case'},
  'G2': { 'case_name': 'Positive_case__main_query__merged_with__2nd_positive_case_of_query_group_from_line_7',
          'meta': 'No change main_query; Negated all, but chosen constraint_from_line_9 from OR group query_group_from_line_7 for positive case'},
  'G3': { 'case_name': 'Negative_case__M_0__1st_negative_case_of_main_query__1st_positive_case_of_query_group_from_line_7',
          'meta': 'Negating constraint_from_line_6 in group main_query; Negated all, but chosen constraint_from_line_8 from OR group '
                  'query_group_from_line_7 for positive case'},
  'G4': { 'case_name': 'Negative_case__M_0__1st_negative_case_of_main_query__2nd_positive_case_of_query_group_from_line_7',
          'meta': 'Negating constraint_from_line_6 in group main_query; Negated all, but chosen constraint_from_line_9 from OR group '
                  'query_group_from_line_7 for positive case'},
  'G5': { 'case_name': 'Negative_case__3rd_negative_case_of_main_query__merged_with__negative_OR_case_query_group_from_line_7',
          'meta': 'Negating query_group_from_line_7 in group main_query; Negated all constraints and child groups from query_group_from_line_7'}}
INFO: Presenting generated data:
{ 'G1': [ { 'Table.Test1': [ {'Col0_id': 'temp_0.333_1', 'Col1_n': '0.333', 'Col2_d': '1988-06-30', 'Col3_text': 'foo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_32_2', 'Col1_n': '32', 'Col2_d': '1986-03-18', 'Col3_text': 'bbb', 'Col4_not_constrained': None}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_0.111_3', 'Col1_n': '0.111', 'Col2_d': '1986-03-18', 'Col3_text': 'moo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_4', 'Col1_n': '14', 'Col2_d': '1988-06-30', 'Col3_text': 'aaa', 'Col4_not_constrained': None}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_0.222_5', 'Col1_n': '0.222', 'Col2_d': '1988-06-30', 'Col3_text': 'boo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_32_6', 'Col1_n': '32', 'Col2_d': '1988-06-30', 'Col3_text': 'ccc', 'Col4_not_constrained': None}]}],
  'G2': [ { 'Table.Test1': [ {'Col0_id': 'temp_0.111_7', 'Col1_n': '0.111', 'Col2_d': '1988-06-30', 'Col3_text': 'boo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_32_8', 'Col1_n': '32', 'Col2_d': '1988-06-30', 'Col3_text': 'boo', 'Col4_not_constrained': 'Ref_681'}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_0.333_9', 'Col1_n': '0.333', 'Col2_d': '1988-06-30', 'Col3_text': 'moo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_10', 'Col1_n': '14', 'Col2_d': '1986-03-18', 'Col3_text': 'foo', 'Col4_not_constrained': 'Ref_432'}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_0.222_11', 'Col1_n': '0.222', 'Col2_d': '1988-06-30', 'Col3_text': 'foo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_32_12', 'Col1_n': '32', 'Col2_d': '1988-06-30', 'Col3_text': 'foo', 'Col4_not_constrained': 'Ref_134'}]}],
  'G3': [ { 'Table.Test1': [ {'Col0_id': 'temp_32_13', 'Col1_n': '32', 'Col2_d': '1988-06-30', 'Col3_text': 'boo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_14', 'Col1_n': '14', 'Col2_d': '1988-06-30', 'Col3_text': 'bbb', 'Col4_not_constrained': None}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_32_15', 'Col1_n': '32', 'Col2_d': '1988-06-30', 'Col3_text': 'foo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_32_16', 'Col1_n': '32', 'Col2_d': '1988-06-30', 'Col3_text': 'ccc', 'Col4_not_constrained': None}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_14_17', 'Col1_n': '14', 'Col2_d': '1988-06-30', 'Col3_text': 'boo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_18', 'Col1_n': '14', 'Col2_d': '1986-03-18', 'Col3_text': 'aaa', 'Col4_not_constrained': None}]}],
  'G4': [ { 'Table.Test1': [ {'Col0_id': 'temp_32_19', 'Col1_n': '32', 'Col2_d': '1986-03-18', 'Col3_text': 'moo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_20', 'Col1_n': '14', 'Col2_d': '1986-03-18', 'Col3_text': 'moo', 'Col4_not_constrained': 'Ref_510'}]}],
  'G5': [ { 'Table.Test1': [ {'Col0_id': 'temp_0.111_21', 'Col1_n': '0.111', 'Col2_d': '1988-06-30', 'Col3_text': 'foo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_32_22', 'Col1_n': '32', 'Col2_d': '1986-03-18', 'Col3_text': 'moo', 'Col4_not_constrained': None}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_0.222_23', 'Col1_n': '0.222', 'Col2_d': '1986-03-18', 'Col3_text': 'boo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_24', 'Col1_n': '14', 'Col2_d': '1986-03-18', 'Col3_text': 'foo', 'Col4_not_constrained': None}]},
          { 'Table.Test1': [ {'Col0_id': 'temp_0.333_25', 'Col1_n': '0.333', 'Col2_d': '1986-03-18', 'Col3_text': 'moo', 'Col4_not_constrained': None},
                             {'Col0_id': 'temp_14_26', 'Col1_n': '14', 'Col2_d': '1986-03-18', 'Col3_text': 'moo', 'Col4_not_constrained': None}]}]}


```
