# Стан розробки — 27.09.2026

Робочий каталог: D:/Projects/ai-hub-hunter-gemini; гілка codex/evidence-based-agents.
Нова локальна адреса http://127.0.0.1:4318/. Старий застосунок 4317 окремий.
Старий проєкт збережений на GitHub main комітом a804c26c02d56559beab7593efc52d407e97d152.

## Реалізовано та перевірено
- Окрема data/workspace.sqlite; вихідні бази Gemini не змінені.
- Перенесено 117 карток, 472 пов'язані завдання, 59 позначок tracking. Ще 4 старі завдання без проєкту збережено в migration_issues.
- Старі оцінки/COMPLETED збережено як неперевірені legacy-дані.
- CryptoRank пріоритет 100, Incrypted 90, Airdrops.io 70, DropsTab/AirdropAlert 60, CertiK 50 (адаптер ризиків ще відсутній).
- Telegram додає тільки користувач. Дозвіл на канал не поширюється на інші канали.
- Живий збір: Airdrops.io 36 карток уже були; DropsTab 27 нових; AirdropAlert 38 нових. Додатково офіційний CryptoRank API дав 1168 карток; разом 1350 карток, не обов'язково різні проєкти.
- 75 навігаційних записів першої помилкової спроби DropsTab позначено excluded_catalog_navigation і архівовано для аудиту; вони виключені з лічильника.
- Черга в SQLite: дедуплікація запусків, відновлення після перезапуску, повторення з інтерфейсу, кеш готових частин аналізу.
- Щоденні перевірки каталогів та проєктів tracking, поки сервер працює. Невдала перевірка також має 24-годинну паузу.
- Знімки джерела, факти/кроки з точними цитатами, порівняння версій тексту/посилань, позначки застарілих доказів. Користувацьке виконання не скидається.
- Ollama qwen3:4b-instruct на CPU; також встановлена qwen3:4b. Llama на перевірці не знайдено.
- На початку 27.09 у базі 23 звіти; кількість не означає 23 повністю верифіковані дослідження. Повнота та помилки в кожному звіті окремі.
- Виправлення користувача включаються в контекст наступного аналізу; це пам'ять корекцій, не навчання ваг моделі.
- Світлий адаптивний UI, читабельна черга, стійкі повідомлення помилок, план і докази кожної картки.
- Реальні свічки Binance/OKX, інтерактивний графік, історичні сценарії з часовим holdout і порівнянням із незмінною ціною. Це ще не ML-прогнозування.

## Доступ до пріоритетних сайтів
Прямий HTTP для CryptoRank і Incrypted повертав 403. Водночас офіційний /v3/drophunting/map із наявним ключем повернув HTTP 200 і 1168 записів. Цей endpoint дає каталог назв, не завдання.
browser-extension/cryptorank-reader працює з API 4318: імпорт відкритих карток через особистий браузер, без cookies/API-панелі, із зупинкою на challenge.
Реальний MV3 service worker перевірений на контрольованому DOM із локальним API: каталог → картка → знімок → черга, зупинка на challenge. Це не доказ живого читання CryptoRank у браузері користувача.
Інструкція: browser-extension/cryptorank-reader/README.md. Ручна вставка тексту доступна у картці.

## Що ще не готове
1. Повна перевірка CryptoRank Reader у браузері користувача, пагінація та читання всіх кроків.
2. Багатоджерельне досьє: офіційні умови/whitepaper/roadmap/соцмережі, об'єднання карток одного проєкту, дедлайни.
3. CertiK-адаптер; повна історія Telegram за місяць (зараз один доступний HTML, неповнота позначена).
4. Дослідження 1000 унікальних проєктів за 8 років. Є 11 часткових кейсів, 0 завершених; історичні аналогії не є вимогами нової кампанії.
5. Котирування справжніх акцій компаній: XAAPL — токенізований інструмент, не пряма акція. Оцінка прогнозів після горизонту та навчання ринкової моделі.
6. Telegram-бот, PWA/Android, серверна авторизація/HTTPS/резервні копії. Локальний API не готовий до публічного розгортання.
7. Підготовка/симуляція дій гаманця з підписом користувача; автономний виконавець вимкнений.

## Запуск і перевірки
Start-Hunter.ps1 або .venv/Scripts/python.exe main.py.
pytest tests; scripts/browser-smoke.mjs використовує окрему тимчасову базу й порт 4319.
Браузерні перевірки: вибір проєкту, джерела, HTML-екранування, черга, історичний прогрес, графік, ширина 390 px.
Скріншот створювався, але перегляд зображення інструментом був недоступний; візуальну перевірку не заявляємо.
Starlette попереджає про майбутню зміну testclient/httpx; тести проходять.

Новий entry point: main.py -> web_tma.backend.server -> Coordinator.
Старі reset/restore/fix_db/browser-експерименти не входять у цей запуск; не запускати над робочою базою.

## Оновлення доступу та доказів
- Пошук по всьому каталогу на сервері, сторінки по 60 карток; API нормалізує ru/en URL CryptoRank.
- Variational: дослідницька нотатка з трьох джерел, завершений турнір відділено від чинної програми поінтів.
- Якщо агрегатор недоступний, агент читає до трьох офіційних документів із перевіреної нотатки. Довільний імпорт не надає такого дозволу. Живе читання обох документів Variational пройшло.
- Історичний прогрес обчислюється за наявністю доказів; алокації відділені від фактичних claims. 0/1000 повних досліджень.
- Секрет API тільки в ігнорованому .env; резервні копії SQLite у data/backups.
- Остання перевірка: 46 pytest, браузерний smoke пройшов; після подальших змін запускати відповідні перевірки.

- Для Uniswap, Arbitrum, EigenLayer додано published-оцінки claims із Dragonfly, зріз 28.01.2025; не позначено незалежно відтвореними результатами.

- Живий цикл Variational, job 77: Ollama прочитала 9782 символи двох документів. Після перевірки 4 торгові інструкції перенесено до довідки, збережено 2 початкові перевірки. Додано класифікацію reward_rules/platform_manual і перевірку меж цитат; 48 тестів та browser smoke пройшли.

- Дослідження розширено до 14 часткових кейсів: ENS, Optimism, dYdX. Optimism: відтворений аудит 248699 рядків офіційного CSV, точні цілочисельні суми, SHA-256; виплати цим не підтверджені.

- Додано 1inch: альтернативні критерії, повторна хвиля та relayer-гаманці. Разом 15 часткових кейсів, 0 завершених. Агенту уточнено збереження логіки І/АБО та етапів кампанії; версію кешу аналізу змінено.

## Поточні правила користувача
- Перевіряти тільки CryptoRank та Incrypted. Інші джерела вимкнено; без нової вказівки користувача їх не сканувати.
- Виключати прогнози/передбачення та торгівлю реальними токенами. Приймати лише активності з тестовими токенами; відсутність опису означає needs_review.
- Папка знайдених карток має фільтри test_only / needs_review / excluded. Це консервативний текстовий відбір, а не завершена ручна перевірка всіх інструкцій.

## Перевірка 28.09.2026
- Дослідницькі нотатки: Integra 1428, HertzFlow 1429, Drosera 1007, Overlayer і Note Systems (ID у data/card-review-2026-09-28.json). Усі needs_review; індексований гайд не підтверджує працездатність тестнету сьогодні.
- Integra: web-читання двох сайтів повернуло 502; HertzFlow недоступний через web; кран Drosera повернув 404. Це обмеження перевірки, не доказ закриття.
- Фільтр v2: заперечення безкоштовних дій не приховує окремої платної вимоги; ознаки завершеної кампанії блокують test_only. UI показує невідомі умови нотатки.
- Наступний крок: живе читання офіційних умов та faucet, без автоматичного підключення гаманця. Інші каталоги залишаються вимкненими.

## Дослідження 1000: розширений дозвіл 28.09.2026
Користувач дозволив офіційні документи проєктів і відкриті дані виплат. Це дозвіл на дослідження, не на ввімкнення інших каталогів або підписання транзакцій. Матеріали, журнал доступу, дати запусків і 12 source-checked extraction examples: research/study-1000/. Note Systems: поточна офіційна сторінка суперечить обіцянці конвертації testnet points в агрегаторі. ENS: запуск 2017, поза вікном 8 років; не рахувати токен 2021 як запуск протоколу. 1000 досьє не завершено.


## Historical rewards research — 2026-09-29

User clarified the study is about already launched projects with historical rewards, not the active testnet discovery catalogue. Somnia, Arbitrum, Cosmos and Polygon were explicitly added to the research scope. Official documents and public payout evidence remain authorized.

Canonical report: `research/study-1000/REPORT.uk.md`; searchable HTML: `REPORT.html`; canonical dataset: `historical-rewards.json` / `.csv`. Current count: 28 partial project dossiers (including one Sui sale comparison), 15 with published payout/claim or genesis-distribution accounts at differing evidence levels; not 1000 completed projects. Cosmos and Polygon are ecosystem groupings, not fabricated extra reward issuers. 44 Dune claim models are saved but have not been executed.

The research window now applies to reward events (2018-09-29 through 2026-09-29), not the first product launch. ENS launch in 2017 no longer disqualifies its 2021 airdrop. The application historical cases were expanded from 15 to 28. Two regression tests cover window boundaries and source requirements.

Published Monad CSV arithmetic independently recalculated: 76,021 unique addresses, 3,330,583,396 MON; median 12,000 MON. This is a published-list audit, not an independent transfer audit. Historical cost and final payout gaps remain explicit.

Ollama was initially stopped; the installed local service was started hidden for evaluation. qwen3:4b-instruct passed 5/7 curated extraction checks. Retained failures: missing the 300 MATIC threshold/operator in Saga; Arkham season returned as string instead of integer. No fine-tuning was performed. Dataset now has 7 new source-checked excerpts (19 with prior set).

Validation: 61 tests passed under `pytest tests -q`; provenance/arithmetic validation passed; HTML search and filters passed in headless Edge. Unscoped root `pytest -q` cannot collect legacy scripts: missing greenlet/Python playwright and obsolete ai_gateway import. These legacy checks were not changed by this research. Do not report all repository checks as passing.

1000-project objective remains incomplete. No background research scheduler was created. Do not count directory metadata, raw market listings, SQL definitions or speculative testnets as completed historical rewards research. Continue from the saved source audit and claim-model candidates, not from the current-project catalogue.


## Historical research expansion — 2026-09-29

Added 30 source-checked partial dossiers: 58 total including one sale comparison, not 1000 completed projects. 28 dossiers have narrative payout/claim/genesis evidence, none fully audited. Downloaded 387 of 389 archive candidate pages; secondary fields are isolated in archive-screening and CANDIDATES.html, excluded from training. Saved 53 expansion URL access records, 42 direct text snapshots. Added six quote-checked extraction examples, 25 total; no new inference or fine-tuning performed. Builders merge expansion-curated files without overwriting them; validation checks unique issuers, CSV/HTML counts, source hashes, quotes and Monad arithmetic. CUA browser inspection failed at runtime initialization; prior screenshot/check retained as historical. Goal of 1000 verified historical projects remains incomplete.
## Плани участі — 01.10.2026
Картка кожного проєкту отримала нумеровані умови, категорії, джерельні цитати й посилання, пороги/строки та окремий блок запропонованих додаткових дій. Невідомі правила показуються окремо. Стан джерела й застарілість збережено. Пропозиції не означають eligibility або гарантію.
Локальний grounded агент тепер повертає requirements: category, necessity, threshold, deadline, quote, source URL. Пороги/строки проходять точну перевірку включення до цитати; вигадані URL відкидаються. Інструкції продукту не стають умовами нагороди. Читач може перевірити до трьох явно пов’язаних сторінок умов; соціальні канали автоматично не додаються.
Одноразовий скрипт backfill_participation.py перевірив 66 tracking проєктів: 56 отримали джерельні кандидати, 10 недоступні. Кандидати — попередня розмітка, не завершений семантичний аудит. Сирі уривки не допущені до fine-tuning. Збережено резервну копію БД й data/participation-backfill.json. Статуси проєктів та виконання завдань не змінювалися.
Перевірки: 66 pytest tests; headless Edge desktop/mobile, цитати/посилання/строки, HTML escaping та відсутність горизонтального переповнення. Screenshots: data/participation-desktop.png / participation-mobile.png. Навчання ваг моделі не виконувалося; оновлено інструкції та валідацію агентів.
Новий запит 250: окремий період запусків mainnet 01.10.2024–01.10.2026. Нова дата токена або сезон старого протоколу не дорівнюють новому mainnet. Дослідження не завершено.
## Короткі описи знайдених проєктів — 02.10.2026
Виявлено: Sandbox map CryptoRank містить лише id/name/slug, тому імпортований службовий текст не є описом продукту. Додано project_overviews зі збереженою джерельною цитатою, URL, snapshot id та датою. API списку й деталі повертає огляд; UI відділяє його від умов кампанії. Додано «Дослідити» без зміни status; порожній test-only список пропонує явний перехід до needs-review.
Витягнуто 135 описів із наявних матеріалів/повторних карток того самого продукту; додано офіційний опис Polyester та functionSPACE. Підсумок: 136 карток з оглядом, 90 new і 46 tracking. Частина оглядів залишається мовою джерела. Назви без доказів не перетворюються на вигадані описи. Скрипт scripts/backfill_overviews.py відтворює джерельний імпорт. Новий формат grounded-v6-overview просить overview українською; умови також мають бути в requirements, навіть якщо модель записала їх у facts. Наявність цитати не підтверджує всі змістові твердження моделі; огляд залишається чернеткою.
Перевірки: 69 tests, Edge fixture і робочий UI desktop/mobile, джерельний опис Polyester, окрема кнопка дослідження, незмінність статусу проєкту, відкидання чужих/вигаданих цитат. Скриншоти data/discovered-overviews-desktop.png і data/discovered-overviews-mobile.png. Сервер перезапущено штатним Start-Hunter.ps1.

Виправлено також ранню взаємодію з пошуком/фільтром: обробники підключаються до очікування лічильників screening, тому швидка зміна фільтра не губиться.
## Кампанії та багатоджерельні інструкції — 02.10.2026
На запит користувача зі скриншотом CryptoRank eCash.com реалізовано кампанії/фази, строки, мережу, тип винагороди, витрати, час, нумеровані кроки з доказами, збереження прогресу, перемикання фаз, джерела перевірки, розбіжності та додаткові можливості. eCash: 3 фази, 7 кроків, 2 конфлікти, 6 офіційних документів. Прямий CryptoRank reader повернув 403; вебіндекс і наданий скриншот позначено окремо. Немає незалежної перевірки eligibility адреси, фінального курсу конвертації чи готовності конкретного binary. BTC snapshot-маршрут не є режимом лише тестових токенів. ПЗ не завантажувалось і транзакції не виконувались.
Поточні tasks дають інструкції 49 із 69 tracking-карток, з різним рівнем доказовості. Це не 49 повних аудитів. Для решти потрібне додаткове дослідження. Особливі проектні дозволи читання відкритих сайтів застосовано до вже обраних проєктів, щоб пауза сторонніх каталогів не блокувала дослідження їхніх ресурсів. Каталоги не ввімкнено, Telegram без дозволу не читається.
Coordinator читає зареєстровані ресурси й посилання джерела; якщо матеріалів мало/немає, використовує bounded Bing RSS як пошук кандидатів. Результат пошуку не означає офіційність. Ресурсні redirects можуть переходити лише на публічні HTTPS-сторінки, з DNS/size/content-type перевірками; discovery залишається в дозволеному домені. Щоденний scheduler працює лише із запущеним сервером. Статус ресурсу й помилки видимі в картці.
Виправлено пріоритет HTML selectors: CSS union раніше повертав parent main до вкладеного article/entry-content і захоплював сусідні картки. Нова схема кампаній перевіряє цитати, URL, дати/пороги; фази не є додатковими reward issuers. Постійні project_guides/project_findings захищають зібрані плани й конфлікти від неповних відповідей моделі. Прогрес залишається user_reported.
Реальна перевірка нової схеми Qwen перевищила старий 180-секундний timeout; семантичний успіх не заявляється. Модель працює на CPU i5-1235U, VRAM=0. Gateway отримав timeout 600 секунд, 4 inference threads та OS-lock між процесами; блокування/скасування перевірене ізольованим тестом. Оновлено policy до 13 правил і research/agent-training/participation-playbook.uk.md; fine-tuning не виконано.
Браузер Edge: fixture phase switching + persisted completion, реальна eCash-картка 3 фази/7 кроків без JS errors, mobile overflow відсутній. Screenshots: data/ecash-guide-desktop.png / ecash-guide-mobile.png. Фінальна перевірка після виправлення неоднозначної атрибуції джерел: 76 pytest пройшли, одна deprecation-попередження Starlette/httpx. Цитату з кількох документів не приписувати довільно першому; опис із неоднозначною атрибуцією відкласти для перевірки.

Дозвіл 02.10.2026 на доповнення карток із інших ресурсів уточнює попереднє обмеження: discovery каталогів залишається CryptoRank/Incrypted, а дослідження вже обраних проєктів охоплює їхні відкриті документи й додаткові знайдені ресурси.

## Автоматична підготовка вхідних карток — 02.10.2026
Кожне add_project ставить новий дозволений проєкт у research, не змінюючи new на tracking. Повторний імпорт не скидає вибір користувача й не дублює роботу. Автоматичний процес зберігається в meta automatic_card_preparation=1. Старі new-картки проходять backfill партіями до 20 за цикл scheduler; оновлення та повторні спроби не частіше ніж раз на добу. Обрані tracking мають пріоритет серед research jobs. Налаштовані паузи каталогів і дозволи Telegram збережено.
API списку та detail повертають preparation: waiting/queued/running/draft/partial/failed, відсутні розділи, кількість кроків, помилку та дату аналізу. Draft означає наявність опису, кроків і звіту, а не завершений аудит умов чи гарантію винагороди. UI показує всі знайдені картки за замовчуванням; існуючий фільтр test_only доступний. Дії користувача: У роботу, Не беремо, Залишити у знайдених. Окрема вкладка Не беремо дозволяє повернути картку; черга ще не початого research скасовується при відхиленні. Уже запущене читання може завершитися, але статус і прогрес не змінює.
Підготовка всього старого каталогу не заявляється завершеною: CPU Ollama опрацьовує матеріали послідовно, джерела можуть бути недоступні. Автоматичне збирання описів та інструкцій не виконує зовнішніх дій і не підключає гаманець.

Перевірка автоматичного intake: 80 pytest пройшли (1 deprecation-попередження Starlette/httpx).

Edge browser smoke пройшов: вибір У роботу, відхилення, вкладка Не беремо, повернення у знайдені зі збереженням 1/1 виконаного кроку; mobile overflow і JS errors відсутні. Робочий сервер: 1267 new-карток, початкова партія 20 new research jobs; API повертає preparation для списку. Це початок поступової підготовки, не завершення всіх карток.
