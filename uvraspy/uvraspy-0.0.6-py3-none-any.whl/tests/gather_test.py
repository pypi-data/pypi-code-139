import pytest
from time import sleep
gather = pytest.importorskip("gather.gather")
from database.dbmanager import DBManager

dbm = DBManager("db", "alert")

g = gather.Gather(dbm)

def test_get_sensors():
    for i in range(10):
        t = g._temp()
        h = g._humid()
        p = g._pressure()
        u = g._uv()
        assert t >= -20 and t <= 60
        assert h >= 0 and h <= 100
        assert p >= 900 and p <= 1100
        assert u >= 0 and u <= 12
        sleep(0.1)


def test_threading():
    # start the gatherer
    g.start_gather()
    sleep(5)
    
    # get the data
    t = g.getTemp()
    h = g.getHumid()
    p = g.getPressure()
    u = g.getUV()
    assert t >= -20 and t <= 60
    assert h >= 0 and h <= 100
    assert p >= 900 and p <= 1100
    assert u >= 0 and u <= 12
    
    # stop the gatherer
    g.running = False
    g.thread.join()
