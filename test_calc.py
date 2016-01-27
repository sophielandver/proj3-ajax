"""
Nose tests for app.py
"""
from app import OpenDuration
from app import CloseDuration

def test_firstControle():
    """
    special case#1
    the open duration for a controle at a distance of 0 is 00:00 and 
    the close duration for a controle at a distance of 0 is 01:00.
    """
    assert OpenDuration(0, 200) == [0, 0]
    assert OpenDuration(0, 600) == [0, 0]
    assert CloseDuration(0,200) == [1, 0]
    assert CloseDuration(0,1000) == [1, 0]

def test_endControle():
    """
    special case #2
    when given a controle distance >= brevet_distance, the open duration is calculated 
    using the brevet_distance instead of the controle distance and the close duration 
    is preset as follows: 13:30 for 200 KM, 20:00 for 300 KM, 27:00 for 400 KM, 
    40:00 for 600 KM, and 75:00 for 1000 KM. 
    """
    assert OpenDuration(205, 200) == OpenDuration(200, 200) == [5,53]
    assert CloseDuration(200, 200) == CloseDuration(205, 200) == [13, 30]
    assert OpenDuration(600, 600) == OpenDuration(610, 600) == [18,48]
    assert CloseDuration(600,600) == CloseDuration(600,600) == [40, 0]


def test_endPoints():
    """
    This is a test to check that I interpreted the table given in the ACP directions
    correctly; i.e. control distances are split up as such: 0...200, 201...400, 401...600, 
    and 601...1000. 
    """
    assert OpenDuration(199, 400) == [5, 51]
    assert OpenDuration(200, 400) == [5, 53]
    assert OpenDuration(201, 400) == [5, 55]
    assert OpenDuration(199, 200) == [5, 51]
    assert OpenDuration(200, 200) == [5, 53]
    assert OpenDuration(201, 200) == [5, 53]
    assert OpenDuration(399, 600) == [12, 6]
    assert OpenDuration(400, 600) == [12, 8]
    assert OpenDuration(403, 600) == [12, 14]
    assert OpenDuration(599, 1000) == [18, 46]
    assert OpenDuration(600, 1000) == [18, 48]
    assert OpenDuration(605, 1000) == [18, 59]

def test_otherCases():
    """
    Some more test cases. 
    """
    assert OpenDuration(0, 1000) == [0,0]
    assert OpenDuration(100, 1000) == [2, 56]
    assert OpenDuration(200, 1000) == [5, 53]
    assert OpenDuration(214, 1000) == [6, 19]
    assert OpenDuration(317, 1000) == [9, 32]
    assert OpenDuration(500, 1000) == [15, 28]
    assert OpenDuration(600, 1000) == [18, 48]
    assert OpenDuration(800, 1000) == [25, 57]
    assert OpenDuration(999, 1000) == [33, 3]
    assert OpenDuration(1000, 1000) == [33, 5]
    assert OpenDuration(1005, 1000) == [33, 5]
    
    assert CloseDuration(0, 1000) == [1, 0]
    assert CloseDuration(100, 1000) == [6, 40]
    assert CloseDuration(200, 1000) == [13, 20]
    assert CloseDuration(214, 1000) == [14, 16]
    assert CloseDuration(317, 1000) == [21, 8]
    assert CloseDuration(500, 1000) == [33, 20]
    assert CloseDuration(600, 1000) == [40, 0]
    assert CloseDuration(800, 1000) == [57, 30]
    assert CloseDuration(999, 1000) == [74, 55]
    assert CloseDuration(1000, 1000) == [75, 0]
    assert CloseDuration(1005, 1000) == [75, 0]
    
    

    
