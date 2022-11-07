from evdspy.EVDSlocal.index_requests.datagroups import get_datagroups_df


def test_get_datagroups_df(capsys):
    with capsys.disabled():
        *coming, last = get_datagroups_df('csv', None, True)
        print(coming)
        print(last)
        print(last())
