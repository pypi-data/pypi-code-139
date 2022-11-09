import sys

import crybaby


def unhandled_exception():
    raise Exception("Unhandled exception")


def handled_exception():
    try:
        raise Exception("Handled exception")
    except Exception as e:
        crybaby.catch(e)
        print(e)
        pass


# unhandled exception
if __name__ == "__main__":
    # test channel: C049CPX8PK9
    # none channel: C02J2G8J0AD
    crybaby.setup(
        slack_token="xoxb-2587256136151-2992810866883-jeItqYtief32SL5KBeFbHekf", slack_channel_id="C049CPX8PK9"
    )
    # print(slack_client.post_message("test msg"))
    # division_by_zero = 1 / 0
    handled_exception()
    # unhandled_exception()
