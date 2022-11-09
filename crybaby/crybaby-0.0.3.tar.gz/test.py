import crybaby


def unhandled_exception():
    raise Exception("Unhandled exception")


def handled_exception():
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)


if __name__ == "__main__":
    crybaby.setup(
        slack_token="xoxb-sample-slack-token", slack_channel_id="SLACKCHANNELID"
    )
    handled_exception()
    unhandled_exception()