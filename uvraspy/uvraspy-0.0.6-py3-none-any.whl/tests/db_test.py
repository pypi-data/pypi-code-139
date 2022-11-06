import pytest
import os
from datetime import datetime

# import database.dbmanager as DB
DB = pytest.importorskip("database.dbmanager")
# wipe db and alert files


def db_init():
    try:
        os.remove("db")
        os.remove("alert")
    except:
        pass  # file doesn't exist
    return DB.DBManager("db", "alert")


def test_db_init():
    db = db_init()
    assert db is not None
    assert db.db is not None
    assert db.alert is not None
    assert db.db_length == 0  # empty file
    assert db.alert_length == 0  # empty file


def test_add_data_point():
    db = db_init()
    db.addDataPoint(DB.DataPoint(datetime.timestamp(datetime.now()), 0, 0, 0, 0))
    assert db.db_length == 1
    assert db.alert_length == 0
    db.addDataPoint(DB.DataPoint(datetime.timestamp(datetime.now()), 0, 0, 0, 0))
    assert db.db_length == 2

    for i in range(100):
        db.addDataPoint(DB.DataPoint(datetime.timestamp(datetime.now()), 0, 0, 0, 0))
    assert db.db_length == 102


def test_retrieve_data():
    db = db_init()
    for i in range(100):
        d = i % 10
        db.addDataPoint(DB.DataPoint(i, d * 2, d * 3, d * 4, d * 5))
    assert db.db_length == 100
    assert len(db.retrieveData(None, None)) == 100
    assert len(db.retrieveData(0, 100)) == 100
    assert len(db.retrieveData(0, 50)) == 51
    assert len(db.retrieveData(50, 100)) == 50
    assert len(db.retrieveData(50, 51)) == 2
    assert len(db.retrieveData(50, 50)) == 1
    assert len(db.retrieveData(50, 500)) == 50
    assert len(db.retrieveData(100, 99)) == 0
    assert len(db.retrieveData(1000, 100)) == 0
    assert len(db.retrieveData(100, 1000)) == 0

    data = db.retrieveData(0, 100)
    for i in range(100):
        d = i % 10
        assert data[i].timestamp == i
        assert data[i].temperature == d * 2
        assert data[i].humidity == d * 3
        assert data[i].pressure == d * 4
        assert data[i].Ultraviolet == d * 5


def test_add_alert_entry():
    db = db_init()
    db.addAlertEntry(DB.Alert(datetime.timestamp(datetime.now()), "random alert"))
    assert db.db_length == 0
    assert db.alert_length == 1
    db.addAlertEntry(DB.Alert(datetime.timestamp(datetime.now()), "random second alert"))
    assert db.alert_length == 2

    for i in range(100):
        db.addAlertEntry(DB.Alert(datetime.timestamp(datetime.now()), "random alert " + str(i)))
    assert db.alert_length == 102


def test_retrieve_alerts():
    db = db_init()
    for i in range(100):
        db.addAlertEntry(DB.Alert(i, "random alert " + str(i)))
    assert db.alert_length == 100
    assert len(db.retrieveAlerts(None, None)) == 100
    assert len(db.retrieveAlerts(0, 100)) == 100
    assert len(db.retrieveAlerts(0, 50)) == 51
    assert len(db.retrieveAlerts(50, 100)) == 50
    assert len(db.retrieveAlerts(50, 51)) == 2
    assert len(db.retrieveAlerts(50, 50)) == 1
    assert len(db.retrieveAlerts(50, 500)) == 50
    assert len(db.retrieveAlerts(100, 99)) == 0
    assert len(db.retrieveAlerts(1000, 100)) == 0
    assert len(db.retrieveAlerts(100, 1000)) == 0

    data = db.retrieveAlerts(0, 100)
    for i in range(100):
        assert data[i].timestamp == i
        assert data[i].warning == "random alert " + str(i)


def test_stress():
    db_len = 100000
    db_retreive = 20000
    db = DB.DBManager("dbdummy", "alert")
    if db.db_length < db_len:
        for i in range(db_len):
            db.addDataPoint(DB.DataPoint(i, i * 2, i * 3, i * 4, i % 12))

    print("now timing")

    btime = datetime.timestamp(datetime.now())
    data = db.retrieveData(None, None, db_retreive)
    etime = datetime.timestamp(datetime.now())
    for d in data:
        ts = d.timestamp
        assert d.temperature == (ts * 2) & 0xffff
        assert d.humidity == (ts * 3) & 0xffff
        assert d.pressure == (ts * 4) & 0xffff
        if ts % 12 != d.Ultraviolet:
            print("UV mismatch")
            print("ts: {} uv: {} d.uv: {} tmp: {}".format(ts, ts % 12, d.Ultraviolet, d.temperature))
        assert d.Ultraviolet == ts % 12

    print("Time to retrieve " + str(db_retreive) + " data points: " + str(etime - btime) + " seconds")


def test_normalize():
    db_len = 100000
    db = DB.DBManager("dbnorm", "alert")
    if db.db_length < db_len - 1000:
        # remove all data points
        db.db.truncate(0)
        db.db_length = 0
        now = int(round(datetime.timestamp(datetime.now())))

        for i in range(db_len):
            d = i % 10
            db.addDataPoint(DB.DataPoint(now + (i - db_len) * 60 * 60, d * 2, d * 3, d * 4, d * 5))

    # copy dbnorm to a temp file
    os.system("cp dbnorm dbnormtemp")
    db2 = DB.DBManager("dbnormtemp", "alert")

    print("now timing")

    btime = datetime.timestamp(datetime.now())
    # normalize
    db2.normalize()
    etime = datetime.timestamp(datetime.now())
    print("Time to normalize " + str(db_len) + " data points: " + str(etime - btime) + " seconds")
    print("db length: " + str(db2.db_length))


# # multi-threading
#             # split the data into 4 chunks
#             # and read them in parallel
#             
#             def decrypt_chunk(data, start, end, ret, i):
#                 ret[i].append([DataPoint.fromEncoded(i) for i in data[start:end]])
# 
#             threads = []
#             returns = [[], [], [], []]
#             for i in range(4):
#                 threads.append(
#                     threading.Thread(
#                         target=decrypt_chunk,
#                         args=(
#                             data_ls,  # data
#                             i * (len(data) // 4),  # start
#                             (i + 1) * (len(data) // 4),  # end
#                             returns,  # return
#                             i
#                         )
#                     )
#                 )
#                 threads[i].start()
#             sleep(1)
#             for i in range(4):
#                 threads[i].join()
#                 full_data += returns[i][0]