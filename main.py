from Breakthrough import Breakthrough
from Api import Api

if __name__ == '__main__':
    a = Api()
    a.login()
    b = Breakthrough(a)
    b.breakthrough()