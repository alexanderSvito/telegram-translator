import re
import telebot
import requests
import config


YANDEX_API = "https://translate.yandex.net/api/v1.5/tr.json/translate"
bot = telebot.TeleBot(config.TOKEN)


def command(regex):
    compiled = re.compile(regex)
    def outer(func):
        def inner(message):
            arguments = compiled.match(message.text).groupdict()
            return func(message, arguments)

        return inner
    return outer


@bot.message_handler(commands=['t', 'translate'])
@command(r"^(?P<command>/t(ranslate)?)\s(?P<from_lang>\w{2})\-(?P<to_lang>\w{2})\s(?P<text>.+$)")
def handle_command(message, args):
    text = args['text']
    params = {
        "key": config.YANDEX_TRANSLATE_KEY,
        "text": text,
        "lang": f"{args['from_lang']}-{args['to_lang']}"
    }
    response = requests.get(YANDEX_API, params=params)
    if response.ok:
        data = response.json()
        bot.send_message(
            message.chat.id, data['text'][0]
        )
    else:
        bot.send_message(
            message.chat.id, "Error"
        )


@bot.message_handler(content_types=['text'])
def handle_answer(message):
    print(message.text)
    bot.send_message(
        message.chat.id, message.text
    )



if __name__ == '__main__':
    bot.polling(none_stop=True)
