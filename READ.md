# Проект №2
## 1. Установка
1. скачайте проект, установите недостающие модули
```
pip install flask
pip indtall requests
```
2. Затем создайте файл .env, в который нужно вставить api с сайта https://developer.accuweather.com/
```
ACCUWEATHER_TOKEN=Тут APi
```
3. Запустите файл app.py и перейдите по адресу, который появится в консоли
## 2. О самом проекте
Проект был создан в образовательных целях. Описание проекта находится в файле Project12R.ipynb.
## 3. Обрабатка ошибок
#### Пользователь имеет 5 полей для ввода:
##### Обязательные: 
- Начальный город
- Конечный город
##### Необязательные(пожелание пользователя):
- Температура
- Влажность
- Скорость ветра
- Осадков нету, потому что в тз сказано брать в %, а в сете мм
#### На необязательных полях поставлен ``type=="number"``, благодаря этому мы можем избежать некорректного ввода
Реализована функция ```check_bad_weather() ```, которая проверяет соответствия погодных условий с предпочтениям
Логика функции построена таким образом, чтобы избежать ошибка в связи с отсутствием каких-либо параметров
#### Ошибки, которые могут произойти (get_weather())
1. Ошибка Not found - города не существует. В этом случае происходит redirect на главную страницу для ввода снова
2. Ошибка API - некорректный API, лимит исчерпан и т.д.. При появлении такой происходит redirect на error.html
  
