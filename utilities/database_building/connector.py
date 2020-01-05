
from dao_test import connector

def main():
    c = connector()
    print(c.get_rooms())
    c.close_conn()


if __name__ == '__main__':
    main()
