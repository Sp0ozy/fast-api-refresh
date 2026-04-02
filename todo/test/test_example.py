import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2
    
def test_is_instance():
    assert isinstance(1, int)
    assert not isinstance(1, str)    
    
def test_boolean():
    valid = True
    assert valid is True
    assert ('hello'=='world') is  False
    
def test_type():
    assert type(1) == int
    assert type('hello' is str)
    
def test_greater_and_less_then():
    assert 2 > 1
    assert 1 < 2
    assert not 1 > 2
    assert not 2 < 1

def test_list():
    num_list = [1, 2, 3]
    any_list = [False, False]
    assert len(num_list) == 3
    assert num_list[0] == 1
    assert 1 in num_list
    assert 4 not in num_list
    assert all(any_list) is False
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
    

@pytest.fixture    
def default_student():
    return Student('John', 'Doe', 'Computer Science', 2)

def test_person_initialization(default_student):
    assert default_student.first_name == 'John'
    assert default_student.last_name == 'Doe'
    assert default_student.major == 'Computer Science'
    assert default_student.years == 2