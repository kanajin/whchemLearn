import fucker

if __name__ == '__main__':
    usr = input('输入账号')
    pwd = input('输入密码')
    f = fucker.Fucker(usr, pwd)
    f.login()
    f.breakthrough()