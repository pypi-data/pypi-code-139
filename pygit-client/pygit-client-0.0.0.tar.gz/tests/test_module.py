import git

def test_version():
    assert len(git.__version__) > 0
