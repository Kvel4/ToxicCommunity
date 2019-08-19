import telebot
import downloader
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.utils import shuffle
import numpy as np

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@train.geekclass.ru:7777'}

bot = telebot.TeleBot('972699153:AAFYR9xj5DnGcwLGmoXxNhk0xj2DI7aCYQ0')

train = pd.read_csv("labeled.csv")
train = shuffle(train, random_state=45)
ans = train['toxic']
train = train.drop(["toxic"], axis=1)
idf_vectorizer = TfidfVectorizer()
train = idf_vectorizer.fit_transform(train.values.reshape(-1))
lr = LogisticRegression().fit(train, ans)


def toxic(comment_list):
    saved = comment_list
    comment_list = pd.DataFrame(comment_list)

    x_test = comment_list
    x_test = idf_vectorizer.transform(x_test.values.reshape(-1))

    y_test = lr.predict_proba(x_test)

    y_test = np.array([el[1] for el in y_test])
    rating = y_test.argsort()[::-1]

    #for el in rating[:10]:
    #    print(saved[el])

    return [sum(y_test) / len(y_test), [saved[el] for el in rating[:10]]]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет отправь мне тэг группы в вк https://vk.com/(это поле)groupname(это поле) '
                                      'и я скажу тебе уровень ее токсичности')


@bot.message_handler(content_types=['text'])
def get_group(message):
    try:
        prob = toxic(downloader.save_comment(message.text))
        bot.send_message(message.chat.id, prob[0])
        bot.send_message(message.chat.id, f'Топ 10 токсичных сообщений:\n'
                                          f'{prob[1][0]}\n'
                                          f'{prob[1][1]}\n'
                                          f'{prob[1][2]}\n'
                                          f'{prob[1][3]}\n'
                                          f'{prob[1][4]}\n'
                                          f'{prob[1][5]}\n'
                                          f'{prob[1][6]}\n'
                                          f'{prob[1][7]}\n'
                                          f'{prob[1][8]}\n'
                                          f'{prob[1][9]}\n')
    except:
        bot.send_message(message.chat.id, 'Такой группы не существует, попробуйте еще раз')


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=10000)
