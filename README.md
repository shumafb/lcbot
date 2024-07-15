*Фишт* \- OSINT\-бот, предназначенный для оперативного поиска информации в различных сервисах  
  
*🤖СТЭК*  
  
Python, aiogram, asyncio, beautifulsoup4, playwright, requests  
  
*🧩МОДУЛИ*  
  
*🦊 numvox* \- внешний сервис определения оператора и региона российского номера  
*☎ kodysu* \- внешний сервис определения оператора и региона номера  
*📦 mysmsbox* \- внешний сервис определения СПАМ\-номеров  
    
*📮 Модем* \- собственный сервис отправки PING\-смс  
└ ⏰ таймер \- функция для отложенной\|быстрой отправки  
*📫 SMSC* \- внешний сервис отправки PING\-смс  
└ ⏰ таймер \- функция для отложенной\|быстрой отправки  
  
*🆔 imeicheck* \- внешний сервис для определения модели телефона  
*🆑 taCList* \- собственный сервис для определения модели телефона  
*🖼 QuickIMAGE* \- внешний сервис поиска изображения по модели телефона  
  
*👤 saveru* \- собственный сервис для поиска по ФИО на базе saverudata  
*🧊 QuickOSINT* \- собственный сервис для поиска по ФИО  
  
*📡 Яндекс Локатор* \- внешний сервис определения координат БС  
  
*🔍ЗАПРОСЫ*  
  
📱 Абонентский номер \[🦊 ☎ 📦\]  
├ 📝 9998887766 \- пример  
├ ℹ️ Номер любой страны  
├ ℹ️ Доп поиск по базам данных  
├ 📫 SMSC \- Ping через SMSC  
├ 📮 Модем \- Ping через собственный модем  
├ 🟢 WhatsApp \- переход в WhatsApp  
├ 🔵 Telegram \- переход в Telegram  
└ 🔴 Yandex \- переход в Яндекс  
  
⏰ Таймер \| Быстрый Ping \[📮 📫\]  
├ 📝 9998887766 [смсц \| smsc \| s \| с \| смс \| sms]  
└ 📝 9998887766 [модем \| м \| можем \| modem \| m]  
  
🆔 IMEI \[🆔 🆑 🖼\]:  
├ 📝 352354112234567 \- пример  
├ 🟣 IMEIinfo \- переход на IMEIinfo  
└ 🔴 Yandex \- переход в Яндекс  
  
👨‍💼 ФИО \[👤 🧊\]  
├ 📝 *Иванов* Иван Иванович \- пример  
└ ℹ️ Фамилия \- обязательно, имя, отчество \- уточняющие фильтры  
  
📡 Базовая станция \[📡\]  
├ 📝 2 2321 7123 \- пример  
├ ℹ️ MNC: 1 \- МТС \| 2 \- Мегафон \|  
└ ℹ️ MNC: 20 \- ТЕЛЕ2 \| 99 \- Билайн  
  
*🤖КОМАНДЫ*  
  
/help \- помощь по командам  
/balance \- проверить баланс  
/modules \- проверить статус сервисов  
/id \- получить Telegram ID  
