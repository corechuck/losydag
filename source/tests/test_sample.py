import pytest
from ..LosydagGenerator import LosydagGenerator

def inc(x):
    return x + 1

def test_setup_work():
    assert inc(4) == 5


@pytest.fixture(scope="session")
def realized_case():
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    generator = LosydagGenerator("http://corechuck.com/modeling/dependent_onto")
    realized_case = generator.realize("RealizationCase.Check1")
    return realized_case


def test_generated_data_have_all_needed_tables(realized_case):
    assert len(realized_case) == 4

    
def test_that_equal_external_dependency_are_equal(realized_case):
    assert realized_case['Table.Ref_01'][0]['Col0_id'] == (
        realized_case['Table.Test3'][0]['Col2_property1_number']
    )


"""
test that generated data has:
    id has format
    two entries in Table.Test2 
    two entries ids have different autoincrements
    Column.Test1.Col3_text has tree or rock not 
    All sets of Table.Test2 not have in Column.Test2.Col3_text "London" and "Tokio" and "Paris
    Realization.Test2.first_colors Column.Test2.Col3_text has 


Other generation of just Table2. where Test.Col3_text have "London" and "Tokio" and "Paris 
    it needs better conversion from Min_Req to Realization def. Move Req_Min to be subclass of RealizationDef


"""