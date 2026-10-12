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

## Пошук нових проєктів і обмежена черга — 03.10.2026
Штатний пошук працює тільки через вебдодаток `D:\Projects\ai-hub-hunter-gemini` і `data/workspace.sqlite`. Старий `discovery/universal_scanner.py` з копії `D:\Projects_Meblibc02\...` записує в іншу `drop_hunter.db`, використовує зламаний DOM-селектор CryptoRank і не є частиною runtime на 4318.

Останні штатні результати до виправлення: CryptoRank перевірив 1176 записів, додав 0, усі 1176 вже були; Incrypted перевірив 32, додав 0, усі вже були. Це успішний незмінений каталог. 01.10 CryptoRank додав 6 нових карток, 02.10 — Titan (Canton), тому deduplication і виявлення змін працюють.

API джерел тепер повертає останню discovery-job та структурований результат. UI у «Знайдених проєктах» і «Джерелах» показує перевірено/нових/дублікатів і пояснює, що 0 нових не є помилкою. Кнопка «Перевірити каталоги зараз» є основним ручним запуском; `Search-New-Projects.ps1` — запасний CLI, який звертається до того самого локального API.

Черга підготовки нових карток обмежена 20 активними research jobs. При першому запуску міграція відкладає надлишкові queued jobs без видалення карток або прогресу. Discovery та analyze лишаються першими, tracking — перед new, а серед new першими опрацьовуються свіжі ID. Масовий імпорт не створює більше 20 research jobs одразу; scheduler поповнює вільні місця поступово.

## Історичні роздачі: 150 проєктів за 2 роки — 03.10.2026

Поточна ціль замінила незавершену ціль 1000: рівно 150 унікальних емітентів із подіями винагороди або claim у періоді 03.10.2024–03.10.2026. Сезони одного емітента не збільшують лічильник. Набір містить 16 часткових досьє з прочитаними першоджерелами та 134 структуровані досьє вторинного каталогу. Це 150 проаналізованих карток, а не 150 повних onchain-аудитів.

`research/study-1000/recent-150-projects.json` і `.csv` містять опис, умови, дату, алокацію, eligible/claimants, статус продукту й винагороди, фактори, джерела, прогалини та урок для агента. `recent-150-strategy.json` містить частоти 17 факторів і 15 пар із co-occurrence/lift. Частота та lift описують умови вибірки, але не доводять причинного впливу на payout і не гарантують майбутньої винагороди.

Для 134 вторинних досьє `fetch_recent_official_sources.py` перевірив по одному пріоритетному зовнішньому посиланню: 48 сторінок містять назву проєкту та релевантні reward-терміни, 21 потребує ручного читання, 65 недоступні прямим запитом. Автоматична релевантність не підвищує досьє до перевіреного рівня. Всі записи мають `fine_tuning_eligible=false`.

Вебдодаток віддає набір через `/api/research/history`, а повний інтерактивний звіт — через `/research/recent-150`. Grounded-агент отримує головні фактори як питання для пошуку в актуальному джерелі. Історичні умови не можуть стати фактом або завданням без точної цитати з поточної картки.

Відтворення: спочатку `python research/study-1000/build_recent_150.py`, потім `python research/study-1000/fetch_recent_official_sources.py`, потім повторно builder для приєднання аудиту. `recent-150-validation.json` перевіряє 150 унікальних карток, джерела, дії, HTML і заборону fine-tuning. Перевірка застосунку: 82 tests passed, одна наявна Starlette/httpx deprecation-warning. Root-level `pytest -q` також збирає три застарілі діагностичні скрипти й падає на заблокованому SQLAlchemy DLL та старому імпорті `ai_gateway`; штатна команда — `pytest tests -q`.


## Відбір дозволених карток — 06.10.2026
Виправлено starvation у pending_preparation: перевірка дозволів джерел і виключення Telegram виконуються до обмеження партії. Раніше 20 карток вимкнених джерел могли постійно займати вибірку, не потрапляючи в чергу, і затримувати CryptoRank/Incrypted. Регресійний тест містить 50 недозволених карток перед однією дозволеною. Дані карток і прогрес не змінено. Для застосування Python-зміни потрібен наступний перезапуск сервера; поточний аналіз Umbrella не перервано.


## Приклади техніки аналізу — 06.10.2026
Робочий grounded-агент добирає до двох коротких перевірених синтетичних демонстрацій за текстом: І/АБО, allocation vs payout, змішані витрати, різні дати. Вони позначені як метод читання, не джерело фактів. Версія та вміст входять у cache key; звіт явно містить fine_tuning_performed=false. Автоматичне перенавчання на власних відповідях заборонене архітектурою цього механізму: бібліотека контрольована у коді. Виправлення користувача залишаються прив’язаними до проєкту.
Відтворювана перевірка локальної моделі: .venv\Scripts\python.exe scripts/evaluate_agent_reading.py; результати data/agent-reading-evaluation.json. Це синтетичні регресійні приклади, не оцінка точності всіх реальних карток і не доказ покращення проти baseline. Timeout враховує очікування спільного inference-lock, тому не дорівнює неправильній відповіді моделі.


## Контроль HertzFlow — 06.10.2026
Виявлено забруднення snapshot 297 (Incrypted single=382945) загальним FAQ і рекламою. material тепер відхиляє динамічні single-сторінки замість видавати FAQ за інструкції. Пряма стаття https://incrypted.com/hertzflow-testnet/ прочитана успішно (1760 символів); додана як reward_rules ресурс картки 1446. Збережено окремий source-reviewed результат: 3 кроки, невідомі умови та дата старої статті 09.05.2026, snapshot 430. Актуальність бета-доступу/крана не підтверджена. Резервна копія data/backups/learning-review-2026-10-06.sqlite.
Спроба grounded Qwen на цій статті перевищила 240 секунд HTTP-очікування; inference-lock уже був отриманий. Семантичний успіх моделі НЕ підтверджений. Результат картки позначено codex-source-reviewed, не Ollama. Сервер перезапущено з усіма змінами. 87 pytest пройшли. Повний browser-smoke зупинився на застарілому очікуванні Arbitrum в історичній вибірці; окремий живий browser check картки 1446 пройшов: інвайт, тестові токени, дата/невідомі умови, без JS errors. Скриншот data/hertzflow-reviewed-desktop.png.


## Діагностика та прогрес Ollama — 09.10.2026
Додано streaming gateway з waiting/reading/generating/done/failed, числовими метриками та відкиданням обірваних відповідей. Частковий текст не публікується як готовий аналіз. Coordinator показує номер частини, символи та час; картка має «Як отримано аналіз». Допоміжний контекст обмежено однією історичною аналогією й трьома питаннями, посилання на дії мають пріоритет над share-кнопками. Навчальні демонстрації підтримують українські/російські терміни.
Реальний Qwen3:4b-instruct завершив HertzFlow за 309.52 с: prompt_eval 110.094 с (2789 input tokens), generation 199.234 с (911 output tokens). Початковий запит 8238+3334 символи, контрольний 4685+3334; увесь джерельний текст 1760 символів збережено. Це один запуск після попередніх timeout; прискорення чи узагальнена точність НЕ доведені. Пізніше додані багатомовні демонстрації можуть збільшити запит.
Отримано 3 requirements з цитатами, campaigns/tasks модель не сформувала. Codex перевірив цитати, відредагував опис, змінив necessity на unknown, додав межі актуальності та зберіг partial report у картці 1446 (snapshot 432). Три попередні кроки збережено. Ваги не перенавчалися. Сирий результат: data/hertzflow-compact-analysis.json; review: research/agent-training/hertzflow-production-review.json.
Виправлено preparation: старий failed job не перекриває новіший звіт; нові помилки та активні jobs залишаються видимі; partial report зберігає partial state. Старі job records не видаляються. Сервер перезапущено з фінальним кодом. 94 tests пройшли перед цим виправленням; після нього 19 API/intake tests пройшли, включно з новою регресією. Повний browser-smoke пройшов після актуалізації історичної вибірки. Жива картка 1446 перевірена desktop/mobile: partial, без старої помилки, 3 tasks + 3 requirements, 309 с, без JS errors/overflow. Скриншот data/hertzflow-ollama-review-2026-10-09.png.


## Світлий кольоровий інтерфейс — 09.10.2026
На запит користувача додано appearance.css: фіолетові дії аналізу, зелені У роботу, блакитний перегляд, рожеве відхилення; світлі кольорові вкладки, спокійний фон, нове оформлення карток і діалогу. Анімації появи, hover/press та індикатор завантаження вимикаються через prefers-reduced-motion. Є focus-visible і мобільна адаптація. Backend/дані не змінені. Жива перевірка 1446: desktop 1440px, mobile 390px, кольори кнопок, відсутність overflow/JS errors, reduced-motion. Скриншоти data/design-refresh-dialog.png, design-refresh-mobile.png, design-refresh-cards.png. Застосовується після оновлення сторінки, перезапуск сервера не потрібен.


## Автоматична пам’ять і незалежний збір — 10.10.2026
Реалізовано adaptive_learning.py: персистентна пам’ять типів помилок, максимум дві контрольовані підказки наступному аналізу, версія в кеші, пауза через API/інтерфейс. Нові відповіді та ретроспективний аудит явно розділені; ваги не перенавчаються, поліпшення якості ще не доведене. На старті 4 матеріали, одна активна підказка missing_plan. Збір discover відокремлений від research/analyze, claim атомарний, recovery один раз до запуску worker. 103 pytest та browser-smoke пройшли. Живі API/UI перевірені; CryptoRank 1184 + Incrypted 32, нових 0. Ollama була вимкнена; запущена з наявними моделями на D. Start-Hunter.ps1 тепер піднімає вже встановлений сервіс. Деталі, докази й незавершені частини: research/agent-training/automatic-memory.uk.md.


## Android PWA — 10.10.2026
Додані manifest, іконки 192/512, service worker лише для статичних ресурсів, екран втрати зв’язку, мобільна навігація. Gateway 4320: одноразовий код (10 хвилин, 8 спроб), Secure/HttpOnly/SameSite cookie, відкликання, точні Host/Origin, локальні маршрути керування телефонами не проксіюються. Дані/сесії/API не кешуються. 109 pytest пройшли; browser-smoke і локальний HTTPS phone-smoke пройшли (вхід, спільна картка, offline, logout). Self-signed/incognito тест НЕ доводить встановлення на фізичний Android. Cloudflare запуск дозволений користувачем, але provisioning API 104.16.230.132/231.132:443 дає TCP timeout, тоді як edge:7844 доступні. QR для непрацюючої адреси не видано. Підготовлений резервний localhost.run, очікує окремого дозволу; докладно docs/ANDROID.md.

### Живе підключення Android через localhost.run — 10.10.2026
Користувач явно дозволив резервний провайдер. Тунель запущений; перевірено дійсний HTTPS, відмову API без сесії (401), вхід за одноразовим кодом, читання приватного API (200), service worker, ширину 390 px і вихід із поверненням 401. Chromium у звичайному окремому профілі повернув installabilityErrors=[]; фізичний Android ще має встановити власник. Виправлено QR-вхід через hashchange у вже відкритій вкладці. Скрипт scripts/verify-live-phone.mjs, знімок data/android-live-https.png. Start-Phone підтримує явний -Provider localhost-run; автоматичного перемикання провайдера немає. Після появи URL перевіряються login і заборона анонімного API, лише потім оголошується успіх. QR для власника створюється окремо після перевірок, діє 10 хвилин.

## Підготовка постійного сервера — 10.10.2026

core/paths.py узгоджує HUNTER_DB для backend, mobile gateway, phone CLI та inference-lock. Раніше gateway і CLI жорстко використовували data/workspace-mobile.sqlite, через що зовнішній шлях бази розходився із сесіями backend. .env завантажується з кореня проєкту до обчислення шляхів; змінні середовища мають пріоритет.

Додано scripts/server_admin.py: origin, pair, revoke, status, backup, verify-backup, restore. Код можна створити через SSH без увімкненого ПК. Backup використовує SQLite backup API, SHA256 і quick_check; restore лише до нового файлу. Окрема база телефонних сесій та .env не експортуються. deploy/linux містить systemd backend/gateway, щоденний backup timer, env і Caddy template. Публічний проксі веде на захищений 4320; backend/Ollama залишаються loopback. Документація: docs/SERVER.uk.md.

115 pytest tests passed (одне наявне попередження Starlette/httpx). Нові регресії перевіряють живий WAL, незбережену транзакцію, пошкодження копії, відмову перезапису, SSH-коди й узгоджені шляхи в окремому процесі. phone-browser-smoke пройшов: вхід, спільні зміни картки, mobile viewport, service worker, offline, logout. Self-signed/incognito fixture не перевіряє фізичне встановлення Android.

Реальна копія успішно відновлена в окремий файл: 1477 projects, 705 tasks, 139 reports, 19 agent_learning_samples. Деталі в data/server-migration-check.json. Це кількості записів, не оцінка якості дослідження. Робоча база й чинні сесії не замінювалися. git diff --check пройшов. Хмарні ресурси не створювалися, домен і Linux/systemd/ARM запуск ще не перевірені; поточний сервер на ПК не перезапускався і агенти не переривалися. Повністю незалежний Android-доступ ще потребує фактичного перенесення та приймання на сервері.
