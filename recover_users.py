from apps.accounts.serializer import UserSerializer
import datetime


def recover():
    with open('u.txt', 'r') as f:
        for line in f.readlines():
            line = line[:-1]
            splitted = line.split("\t")
            # print(splitted)
            print("name ", splitted[1], splitted[2])
            print("email ", splitted[3])
            print("date ", splitted[4])
            print("uni ", splitted[5])
            print("=============================================")
            data = {
                "email": splitted[3],
                "password1": 'security_branch',
                "password2": 'security_branch',
                "profile": {
                    'firstname_fa': splitted[1],
                    'firstname_en': '_',
                    'lastname_fa': splitted[2],
                    'lastname_en': '_',
                    'birth_date': datetime.datetime.strptime(splitted[4], '%Y-%m-%d'),
                    'university': splitted[5]
                }
            }
            user = UserSerializer(data=data)
            user.save()
            user.instance.is_active = True
            user.instance.save()
