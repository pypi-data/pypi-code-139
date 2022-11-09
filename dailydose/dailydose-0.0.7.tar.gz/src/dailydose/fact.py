import os
import json
import random


def get(count=1, include_details=True):
    '''
    Returns a fun fact from The Fact Site (thefactsite.com)
    '''

    # Get absolute data path
    data_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "./data/fun_fact.json")

    # Read fun facts data
    fun_facts = json.load(open(data_path, "r", encoding="utf-8"))

    # Sample `count` number of data
    random_fun_facts = random.sample(fun_facts, count)

    # Keep only heading if `include_details=False`
    if not include_details:
        random_fun_facts = [{"heading": fact["heading"]}
                            for fact in random_fun_facts]

    return random_fun_facts


if __name__ == "__main__":
    fact = get()
    print(fact[0]['heading'])
    print("\n"+fact[0]['content'])
