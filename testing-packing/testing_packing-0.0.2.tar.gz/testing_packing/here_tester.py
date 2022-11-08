def hello():
    return "Hello"

class HZN:
    def __init__(self) -> None:
        self.name = 'Han Zaw Nyein'
    
    def __repr__(self) -> str:
        return self.name

HELLO = hello()
hzn = HZN()

if __name__ == "__main__":
    print("*"*10)
    print(hello())