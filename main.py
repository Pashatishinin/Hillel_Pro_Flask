from flask import Flask, render_template, url_for, request
import urllib
from random import randint
import csv
from flask_csv import send_csv

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run()


@app.route("/requirements/")
def requirements():
    req = open("requirements.txt")
    return render_template('requirements.html', requirements_string=f'{url_for}')


@app.route("/generate-users/")
@app.route("/generate-users/", methods=['GET'])
def generate_users():
    user_all_dict = []

    def randomizer():
        # Список имен
        name_list = ["Aleksandr", "Sasha", "Alexey", "Alyosha", "Albert", "Alik", "Anatoly", "Andrey", "Anton",
                     "Antosha", "Arkadiy", "Artem", "Artur", "Arkhip", "Afanasii", "Boris", "Bronislav", "Vadim",
                     "Valentin", "Valya", "Valeriy", "Vasily", "Viktor", "Vitaly", "Vladimir", "Vladislav", "Vsevolod",
                     "Vyacheslav"]
        # Радномайзер числа для списка имен
        ran_name_number = randint(0, len(name_list) - 1)
        # Имя из списка под рандомный номером
        random_first_name = name_list[ran_name_number]
        # Cписок почтовых ящиков
        mail_list = ["gmail.com", "yahoo.com", "urk.net"]
        # Радномайзер числа для списка почтовых ящиков
        ran_mail_number = randint(0, len(mail_list) - 1)
        # Почтовый ящик из списка под рандомный номером
        random_mailbox = mail_list[ran_mail_number]
        random_name = ''
        # Генератор имени для почтового ящика, который генерируется только из букв имени
        for _ in range(7):
            ran_mail_name_number = randint(0, len(random_first_name) - 1)
            random_name += random_first_name.lower()[ran_mail_name_number]

        mail_post = random_name + "@" + random_mailbox
        users_dict = {"User Name": random_first_name, "Email": mail_post}

        return users_dict

    #Парсим
    args = request.args
    new_dict = dict(args)

    if new_dict.get('count'):
        for _ in range(int(new_dict.get('count'))):
            user_all_dict.append(randomizer())
        number = int(new_dict.get('count'))
    else:
        user_all_dict.append(randomizer())
        number = 1

    with open("generate_users.txt", 'w') as file:
        file.write(str(user_all_dict))

    req = open("generate_users.txt")
    return render_template('generate_users.html', generate_users_string=req.read(), number=number)


@app.route("/mean/")
def mean():
    with open('hw.csv', "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        h = 0.0
        w = 0.0
        for row in reader:
            h += float(row.get(' "Height(Inches)"'))
            w += float(row.get(' "Weight(Pounds)"'))
            count += 1
        print(h, w, count)
        middle_height = h/count
        middle_weight = w/count
    return render_template('mean.html', height=middle_height, weight=middle_weight)







