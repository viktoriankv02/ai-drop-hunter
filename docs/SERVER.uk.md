# Hunter на постійному Linux-сервері

Стан: підготовлені конфігурації та перевірені Python-механізми. Справжнє розгортання на Linux/ARM, HTTPS домену, перезавантаження сервера й швидкість Qwen ще не перевірені. Сервер у хмарі не створено.

## Архітектура

Android PWA → HTTPS Caddy :443 → захищений gateway 127.0.0.1:4320 → Hunter 127.0.0.1:4318 → SQLite та Ollama 127.0.0.1:11434.

Весь аналіз і щоденний планувальник працюватимуть на сервері. ПК можна буде вимикати. Для телефона потрібен інтернет. Інсталяція PWA не означає наявності моделі на телефоні.

Код і Python-середовище: /opt/hunter. Постійна база, пам’ять агентів, сесії, inference-lock і резервні копії: /var/lib/hunter. Конфігурація: /etc/hunter.env. Запускається тільки один процес backend, щоб не дублювати планувальник. Telegram-бот і браузерний імпорт із ПК не з’являються автоматично внаслідок перенесення.

## Перед створенням сервера

Перевірити власний безкоштовний ліміт, доступність ARM-інстансу, диск і тариф у консолі провайдера. Цей документ не створює платних ресурсів.

Потрібні Ubuntu або інший Linux із systemd, SSH, Python із venv, Caddy, Ollama та DNS-ім’я, яке веде на сервер. Орієнтир для невеликої Qwen: 8–16 ГБ RAM і 60–80 ГБ диска; швидкість CPU оцінюється окремо. На Windows тести пройдено з Python 3.14; сумісність конкретних Linux-пакетів слід перевірити під час встановлення.

Встановлення Caddy: https://caddyserver.com/docs/install
Ollama для Linux/ARM64: https://docs.ollama.com/linux
HTTPS і DNS: https://caddyserver.com/docs/automatic-https

На зовнішньому firewall: 80/443 для Caddy, SSH лише для власника. 4318, 4320 та 11434 не відкривати в інтернет. Застосунок і Ollama залишаються на loopback. Секрети, бази, профілі браузера й модель не входять до публічного репозиторію.

## Підготовка ОС та коду

Команди нижче — для майбутнього сервера; на ПК їх не запускали.

    sudo useradd --system --home-dir /var/lib/hunter --create-home --shell /usr/sbin/nologin hunter
    sudo install -d -m 0755 /opt/hunter
    sudo install -d -o hunter -g hunter -m 0700 /var/lib/hunter

Передати перевірену поточну версію вихідного коду до /opt/hunter. Поточні зміни ще не опубліковані в GitHub: звичайний clone може їх не містити. Не переносити Windows .venv, .env, data, .git, стару drop_hunter.db або профілі браузера разом із кодом. Дослідження research/ потрібні для історичних матеріалів застосунку.

Створити Linux venv і перевірити залежності:

    cd /opt/hunter
    sudo python3 -m venv .venv
    sudo .venv/bin/python -m pip install -r requirements-dev.txt
    sudo .venv/bin/python -m pytest tests -q
    sudo install -o root -g hunter -m 0640 deploy/linux/hunter.env.example /etc/hunter.env

Відредагувати /etc/hunter.env на сервері. Ключ CryptoRank вводиться локально, якщо потрібен; його відсутність не означає доступності всіх сторінок через API. Зберегти HUNTER_DB=/var/lib/hunter/workspace.sqlite.

Встановити Ollama з офіційного джерела, перевірити loopback-адресу й отримати модель:

    ollama pull qwen3:4b-instruct
    curl --fail http://127.0.0.1:11434/api/tags

Без моделі вебінтерфейс може працювати, але локальний ШІ-аналіз недоступний.

## Копіювання даних із ПК

Онлайн-копія створюється через SQLite backup API, а не копіювання одного .sqlite без WAL:

    .venv/Scripts/python.exe scripts/server_admin.py backup --directory data/backups/server-migration

У каталозі копії є workspace.sqlite та manifest.json із SHA256. До бази входять проєкти, завдання, звіти, джерела, налаштування та пам’ять агентів. Окремі сесії телефона, .env, API-ключі із .env, Ollama-моделі й зовнішні файли не копіюються. База містить приватну інформацію користувача — передавати через SSH, не публічним посиланням.

Під час остаточного переходу зупинити локальні агенти й зробити фінальну копію, щоб ПК і сервер не розійшлися в даних. Перенести каталог копії через SCP/SFTP у /var/lib/hunter/import і надати його користувачу hunter.

На сервері, поки служби зупинені:

    sudo -u hunter /opt/hunter/.venv/bin/python /opt/hunter/scripts/server_admin.py verify-backup /var/lib/hunter/import/BUNDLE
    sudo -u hunter /opt/hunter/.venv/bin/python /opt/hunter/scripts/server_admin.py restore /var/lib/hunter/import/BUNDLE --destination /var/lib/hunter/workspace.sqlite

BUNDLE замінити назвою реальної папки. Відновлення навмисно відмовляється перезаписати наявну базу або її WAL-файли.

## Захищена адреса й перший вхід

Замінити hunter.example.com у deploy/linux/Caddyfile.example реальним доменом і додати цей сайт до конфігурації Caddy, не перезаписуючи інші сайти. DNS має вести на IP цього сервера. Проксі спрямований тільки на gateway :4320.

    sudo -u hunter /opt/hunter/.venv/bin/python /opt/hunter/scripts/server_admin.py --database /var/lib/hunter/workspace.sqlite origin https://hunter.example.com
    sudo cp /opt/hunter/deploy/linux/hunter.service /etc/systemd/system/
    sudo cp /opt/hunter/deploy/linux/hunter-gateway.service /etc/systemd/system/
    sudo cp /opt/hunter/deploy/linux/hunter-backup.service /etc/systemd/system/
    sudo cp /opt/hunter/deploy/linux/hunter-backup.timer /etc/systemd/system/
    sudo systemd-analyze verify /etc/systemd/system/hunter.service /etc/systemd/system/hunter-gateway.service /etc/systemd/system/hunter-backup.service /etc/systemd/system/hunter-backup.timer
    sudo systemctl daemon-reload
    sudo systemctl enable --now hunter.service hunter-gateway.service
    sudo caddy validate --config /etc/caddy/Caddyfile
    sudo systemctl reload caddy

Перевірка без авторизації:

    curl --fail https://hunter.example.com/mobile-login
    curl -i https://hunter.example.com/api/projects

Сторінка входу має повернути 200, приватний API — 401. Відсутність цих двох результатів означає, що публічний доступ ще не готовий.

Створити одноразовий код через SSH:

    sudo -u hunter /opt/hunter/.venv/bin/python /opt/hunter/scripts/server_admin.py --database /var/lib/hunter/workspace.sqlite pair

Команда показує приватне посилання з кодом у fragment, який не надсилається HTTP-серверу. Код одноразовий, діє 10 хвилин, має ліміт 8 невдалих спроб. Не зберігати в журналах і не публікувати. Телефонна сесія діє до 30 днів; повторний вхід потребує нового коду через SSH, яке можливе й із телефона. Стара Windows-машина для цього не потрібна. Самообслуговування входу через пароль/passkey ще не реалізоване.

Відкликати всі телефони:

    sudo -u hunter /opt/hunter/.venv/bin/python /opt/hunter/scripts/server_admin.py --database /var/lib/hunter/workspace.sqlite revoke

Зміна origin також відкликає старі сесії. Іконку PWA зі старої тимчасової адреси треба встановити з нової адреси.

## Резервні копії та стан

Спочатку перевірити ручну копію, потім увімкнути timer:

    sudo systemctl start hunter-backup.service
    sudo systemctl status hunter-backup.service
    sudo systemctl enable --now hunter-backup.timer
    sudo systemctl list-timers hunter-backup.timer

Timer запускається щодня о 03:00 UTC з випадковою затримкою до 5 хвилин; Persistent надолужує пропущений запуск. Копії створюються у /var/lib/hunter/backups. Автоматичного видалення старих копій немає: стежити за вільним диском і періодично вивантажувати копії в інше сховище. Копії на тому самому сервері не захищають від втрати сервера.

    sudo systemctl status hunter hunter-gateway
    sudo journalctl -u hunter -u hunter-gateway -n 100 --no-pager
    sudo -u hunter /opt/hunter/.venv/bin/python /opt/hunter/scripts/server_admin.py --database /var/lib/hunter/workspace.sqlite status

gateway_ready означає живий heartbeat gateway, а не перевірку DNS/інтернету. Зовнішню адресу перевіряти окремо. Коди та cookie не включені в status.

## Критерії готовності та відкат

Перед перенесенням:
- Пройдено pytest tests -q на цільовому Linux.
- systemd-analyze verify і caddy validate успішні.
- Резервна копія перевірена й пробно відновлена в окремий файл.
- Кількість проєктів/завдань/пам’яті відповідає копії.
- Без входу немає доступу до API; після входу картки читаються й змінюються.
- Модель читає справжній матеріал; недоступний CryptoRank не позначається як успішне читання.
- Перезавантаження сервера не втрачає базу, сесії та відновлює службу.
- Фізичний Android відкриває HTTPS і встановлює PWA.

Відкат потрібен при втраті авторизації, помилках SQLite або втраті підтверджених даних. Зупинити hunter та hunter-gateway, зберегти поточну базу окремою копією, повернути попередній код і відновити перевірену копію в НОВУ назву. Вказати її HUNTER_DB в /etc/hunter.env. Оскільки база сесій прив’язана до назви основної бази, налаштувати origin і видати новий код; старі сесії не переносити. Лише потім запустити служби й повторити перевірки. Не виконувати сліпе копіювання поверх живого SQLite.

## Перевірено локально 10.10.2026

Нові тести: WAL snapshot, виключення непідтвердженої транзакції, збереження agent_learning_samples, перевірка хешу, заборона перезапису, зіпсована база, SSH-код/відкликання, узгоджені HUNTER_DB між API/gateway/CLI. Мобільний браузерний тест пройшов на ізольованому HTTPS fixture. Це не заміняє приймання справжнього Linux-сервера.

Реальна база пробно відновлена: 1477 проєктів, 705 завдань, 139 звітів, 19 записів пам’яті. Це кількості збережених записів, не кількість повністю перевірених проєктів або доказ поліпшення моделі. Звіт: data/server-migration-check.json. Робоча база не замінювалася.
