from threading import Timer

TOKEN = "5608746480:AAESSuAzhT4-tyKHmpQGlT1MAFcxz8ffppU"



welcome_morning = """Доброе утро!
Добро пожаловать в <b>Alone Dayz</b>!
<em>Вам предстоитт пройти <b>огромное путешествие</b>, чтобы стать выдающимся воином среди всех!
<b>Выбирай классы, фарми лес, сражайся с боссами!</b>
Все это тебя ждет в <b>Alone Dayz</b>! Начни играть прямо сейчас!
Пиши /help и узнавай подробности о игре!</em>"""



welcome_day = """Добрый день!
Добро пожаловать в <b>Alone Dayz</b>!
<em>Вам предстоитт пройти <b>огромное путешествие</b>, чтобы стать выдающимся воином среди всех!
<b>Выбирай классы, фарми лес, сражайся с боссами!</b>
Все это тебя ждет в <b>Alone Dayz</b>! Начни играть прямо сейчас!
Пиши /help и узнавай подробности о игре!</em>"""


welcome_dinner = """Добрый вечер!
Добро пожаловать в <b>Alone Dayz</b>!
<em>Вам предстоитт пройти <b>огромное путешествие</b>, чтобы стать выдающимся воином среди всех!
<b>Выбирай классы, фарми лес, сражайся с боссами!</b>
Все это тебя ждет в <b>Alone Dayz</b>! Начни играть прямо сейчас!
Пиши /help и узнавай подробности о игре!</em>"""

welcome_night = """Доброй ночи!
Добро пожаловать в <b>Alone Dayz</b>!
<em>Вам предстоитт пройти <b>огромное путешествие</b>, чтобы стать выдающимся воином среди всех!
<b>Выбирай классы, фарми лес, сражайся с боссами!</b>
Все это тебя ждет в <b>Alone Dayz</b>! Начни играть прямо сейчас!
Пиши /help и узнавай подробности о игре!</em>"""



help = """
<em><b>Alone Dayz</b> - бот-игра в стиле RPG
Здесь доступно 3 класса:
<b>1. Светлые Эльфы</b>
<b>2. Темные Эльфы</b>
<b>3. Рыцари</b>
У каждого класса есть свои привелегии
(PS: подробнее о каждом классе вы узнаете при выборе персонажа)
    Команды для дальнейшего развития:
        /game - <b>начало игры</b>
        /farm - <b>начать фарм опыта</b>
        /buy - <b>открыть магазин предметов</b></em>
        /profile - <b>Показывает вашу статистику</b>
        """

vibor_classa = """
Как вы уже знаете в <b>Alone Dayz</b> есть 3 класса:
<b>Светлый Эльф:</b>
<em><b>1.</b>увеличивает скорость фарма на 40
<b>2.</b>с шансом 5% может получит 2х опыт за фарм
<b>3.</b>Начальная мана увеличена на 5 единиц </em>
<b>Темный Эльф:</b>
<em><b>1.</b>скорость фарма увеличина на 60
<b>2.</b>с шансом 15% может увеличить урон на 25%
<b>3.</b>начальная мана уменьшена на 10 единиц</em>
<b>Рыцарь:</b>
<b>1.</b><em>скорость фарма увеличина на 70
<b>2.</b>изначально мана уменьшена на 15 единиц
<b>3.</b>с шансом 10% увеличивает получаемый опыт на 50%</em>"""


vibor_weapon = """
<em>Отлично! Вы выбрали класс <b>{}</b>!
Теперь Вам предстоит <b>выбор оружия</b>, для вашего героя!
<b>Мечник</b> - Герой ближнего боя, дает +10 к скорости фарма
<b>Лучник</b> - Герой дальнего боя, дает +20 к скорости фарма, но уменьшает ману на 5
<b>Маг</b> - Герой использующий магию, увеличивает ману героя на 30</em>
"""



start_farm = """
<em>Отлично! Вы выбрали <b>{}</b>!
Ваш путь воина в <b>Alone Dayz</b> начался!
<b>Начинайте фарм командой /farm
Покупайте новые шмотки командой /buy
Сражение с боссом происходит каждый понедельник!</b>
За сражение вы можете получить особые награды(P.S: если победите😂)
Удачи! Да прибудет с тобой сила!</em>"""

XP_ADD = """Добавлено: {}XP
Всего: {}/{}XP"""

GOLD_ADD = """Добавлено золота: <b>{}</b>"""

white_elf = "white_elf"
dark_elf = "dark_elf"
knights = "knights"

PROFILE ="""Ваш класс: <b>{}</b>
Ваше оружее: <b>{}</b>
Ваш уровень: <b>{}</b>
Ваше золото: <b>{}</b>"""


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

