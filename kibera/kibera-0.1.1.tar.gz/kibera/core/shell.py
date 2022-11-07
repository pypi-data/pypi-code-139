def start_shell(**ns):
    import IPython

    IPython.start_ipython(colors="neutral", argv=[], user_ns=ns)
