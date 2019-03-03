# Flask team recaps collection

Basic web app that allows to collect recaps for the tournaments held by rating.chgk.info 
(Russian-language quiz-like offline game "What? Where? When?"). 
Form uses Flask-WTF and Rating API search functionality to spend less time and paper collecting team recaps.    

Functionality description in Russian below. Beware of the ugly coding practices.

# Сбор составов на "Что? Где? Когда?"

Форма сбора составов для упрощения жизни представителям, загружающим составы команд на rating.chgk.info, 
и капитанам команд, копирующим одного игрока за другим на каждый турнир.

Функционал:

* Поиск команды по ID с автоматическим вводом базового состава
* Поиск игрока по ID (точный) или ФИО (предлагает варианты при множественном совпадении)
* Сбор дат рождения игроков и дополнительной информации о командах (вуз)
* Сохранение составов в формате сайте рейтинга (правильный порядок полей через точку с запятой)
* Отображение списка отправленных составов

Что пока не сделано, но будет: 

* Сохранение всех отправленных составов в СР-1251 для прямой загрузки на сайт рейтинга
* Красивый поиск, а не как сейчас

Писать можно в Issues или телеграм @papkov