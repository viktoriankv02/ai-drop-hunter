# Історичні роздачі: 150 проєктів за останні 2 роки

**Період подій:** 2024-10-03–2026-10-03. **Дата зрізу:** 03.10.2026.

Рівно 150 унікальних емітентів; повторні сезони об’єднано. Поіменні досьє з прочитаними джерелами відділені від структурованого скринінгу вторинної директорії. Алокація, eligible, claimants і фактичні перекази — різні показники.

## Покриття та межі доказів

- Першоджерела прочитано, досьє часткове: **16**.
- Змішані поіменні джерела: **0**.
- Вторинна директорія, потрібна первинна перевірка: **134**.
- Додатково завантажено офіційні сторінки з релевантними термінами: **48**; вони ще очікують ручної перевірки тверджень.
- Повністю відтворений аудит усіх переказів: **0**.
- Fine-tuning дозволено: **0**; записи спершу мають пройти незалежну перевірку.

## Взаємозв’язки та фактори

Таблиця показує, як часто фактор прямо згаданий у зібраних умовах. Це описова частота, а не оцінка ймовірності нагороди й не доказ, що дія спричинила виплату.

| Фактор | Проєктів | Частка | З перевірених досьє | Як застосувати |
|---|---:|---:|---:|---|
| `points_quests` | 118 | 78.7% | 6 | Зберігати season, формулу points, mandatory/bonus дії та версію правил. |
| `claim_and_vesting` | 102 | 68.0% | 7 | Стежити за початком/кінцем claim, vesting, unlock і поверненням невитребуваних токенів. |
| `capital_exposure` | 99 | 66.0% | 5 | Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. |
| `nft_or_asset_holding` | 98 | 65.3% | 6 | Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння. |
| `community_contribution` | 97 | 64.7% | 7 | Оцінювати якість і підтверджуваність внеску; масовий spam підвищує Sybil-ризик. |
| `snapshot_state` | 93 | 62.0% | 7 | Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. |
| `ranking_or_tier` | 89 | 59.3% | 6 | Зберігати формулу score, межі tier і capped/uncapped частини; не припускати лінійну конвертацію. |
| `activity_diversity` | 75 | 50.0% | 2 | Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. |
| `duration_consistency` | 72 | 48.0% | 3 | Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. |
| `real_product_usage` | 72 | 48.0% | 7 | Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. |
| `early_participation` | 63 | 42.0% | 5 | Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. |
| `anti_sybil_identity` | 48 | 32.0% | 2 | Не автоматизувати дублікати особистостей; перевіряти правила адрес, кластерів, KYC і географії. |
| `activity_volume` | 47 | 31.3% | 6 | Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. |
| `testnet_participation` | 31 | 20.7% | 3 | Вести журнал транзакцій, feedback і знайдених помилок; тестнет сам по собі не гарантує токени. |
| `referrals` | 30 | 20.0% | 2 | Вважати referral додатковим множником, якщо правила не визначають його обов’язковим. |
| `developer_contribution` | 27 | 18.0% | 6 | Зберігати PR, commit, deployment і прийнятий результат, а не лише факт активності. |
| `node_validator_work` | 25 | 16.7% | 1 | Контролювати uptime, версію клієнта, епохи, ключі та фактичну вартість сервера. |

### Поєднання факторів

Lift понад 1 означає, що пара зустрічалася разом частіше, ніж очікувалося з її окремих частот. Це допомагає будувати чекліст, але не доводить причинності або розміру винагороди.

| Фактор A | Фактор B | Разом | Частка | Lift |
|---|---|---:|---:|---:|
| `node_validator_work` | `testnet_participation` | 13 | 8.7% | 2.52 |
| `developer_contribution` | `testnet_participation` | 9 | 6.0% | 1.61 |
| `early_participation` | `node_validator_work` | 16 | 10.7% | 1.52 |
| `activity_volume` | `referrals` | 14 | 9.3% | 1.49 |
| `community_contribution` | `testnet_participation` | 28 | 18.7% | 1.40 |
| `nft_or_asset_holding` | `snapshot_state` | 83 | 55.3% | 1.37 |
| `community_contribution` | `node_validator_work` | 22 | 14.7% | 1.36 |
| `ranking_or_tier` | `referrals` | 24 | 16.0% | 1.35 |
| `real_product_usage` | `referrals` | 19 | 12.7% | 1.32 |
| `anti_sybil_identity` | `node_validator_work` | 10 | 6.7% | 1.25 |
| `early_participation` | `testnet_participation` | 16 | 10.7% | 1.23 |
| `nft_or_asset_holding` | `node_validator_work` | 20 | 13.3% | 1.22 |
| `node_validator_work` | `points_quests` | 24 | 16.0% | 1.22 |
| `duration_consistency` | `ranking_or_tier` | 52 | 34.7% | 1.22 |
| `activity_diversity` | `node_validator_work` | 15 | 10.0% | 1.20 |

## Стратегія відпрацювання

1. Спочатку оцінити довіру: офіційний домен, команда, фінансування, стан mainnet/продукту, правила та ризики.
2. Визначити основну корисну дію продукту. Взаємодія має бути реальною, повторюваною лише там, де правила враховують тривалість або епохи.
3. Зберігати докази: дата, wallet, network, tx hash, route, amount, fee, balance before/after, quest/season і URL версії правил.
4. Покривати додаткові фактори лише після основної дії: різноманітність функцій, governance, feedback, контент, referral або NFT.
5. Встановити бюджет на gas, fees, capital lock і сервер. Зупиняти стратегію, якщо очікувана невизначена винагорода не виправдовує ризик.
6. Не створювати Sybil-кластери, wash-volume, spam або фіктивні referrals. Такі дії часто ведуть до виключення.
7. Після snapshot продовжувати відстеження: eligibility checker, claim, vesting, unlock, deadline і зміни правил.

## 150 досьє

### 1. Flare

**Дата:** 2026-01-30 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Поіменне історичне досьє з матеріалами про умови та подію винагороди.
**Статуси:** source_checked_historical_product; completed_program_reported.

**Умови/дії:**

- Щомісячні FlareDrops за WFLR і придатним стейкінгом: середній баланс за трьома випадковими блоками періоду утримання.
- Claim протягом 67 днів;
- невитребувана частина спалюється.

**Фактори:** claim_and_vesting.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** 36 щомісячних випусків — один емітент. Відокремлювати завершені FlareDrops від стейкінгових винагород, що тривають.

**Прогалини:** Незалежний перерахунок переказів і фінальних одержувачів не виконано. Витрати учасників і поточну працездатність продукту окремо не перевірено.

**Джерела:** [Джерело 1](https://flare.network/flaredrops) · [Джерело 2](https://flare.network/news/flaredrop-guide)

### 2. Monad

**Дата:** 2025-11-24 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Поіменне історичне досьє з матеріалами про умови та подію винагороди.
**Статуси:** source_checked_historical_product; issuer_reported_claims.

**Умови/дії:**

- П’ять напрямів: внесок у спільноту;
- активні onchain-користувачі;
- криптоспільноти;
- розробники Monad;
- публічні блага й освіта.
- Враховано довготривалий внесок, ручний перегляд і рекомендації спільноти.
- Вікно claim: 14.10–03.11.2025.

**Фактори:** claim_and_vesting.
**Обсяг:** 3330583396. **Eligible:** невідомо. **Claimants:** 76021.
**Урок:** Тестнет-транзакції не дорівнюють гарантованій алокації. Вчити класифікацію внесків, об’єднання субкатегорій і різницю між escrow та доступними коштами.

**Прогалини:** Не відтворено всі перекази escrow → одержувач. Не пораховано витрати або прибуток кожного учасника.

**Джерела:** [Джерело 1](https://monad.xyz/blog/the-mon-airdrop-results) · [Джерело 2](https://docs.monad.xyz/) · [Джерело 3](https://dune.com/blog/dune-digest-037) · [Джерело 4](https://raw.githubusercontent.com/monad-crypto/airdrop-addresses/main/monad_airdrop_results.csv)

### 3. Plasma

**Дата:** 2025-09-25 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Поіменне історичне досьє з матеріалами про умови та подію винагороди.
**Статуси:** source_checked_historical_product; published_distribution_analysis.

**Умови/дії:**

- Офіційно анонсовано бонус 25 млн XPL для малих депозитаріїв, які пройшли Sonar-перевірку та взяли участь у продажу.
- Окремо продано 10% supply;
- 2,5 млн XPL зарезервовано для Stablecoin Collective.

**Фактори:** не класифіковано.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Зберігати продаж, бонус і резерв спільноти окремо. Депозит, KYC, блокування та нові кошти для купівлі — різні вимоги.

**Прогалини:** Первинне підтвердження всіх бонусних переказів. Повна формула добору менших депозитаріїв. Незалежна перевірка чисел вторинного аналізу.

**Джерела:** [Джерело 1](https://www.plasma.org/company/blog/plasma-mainnet-beta-and-xpl) · [Джерело 2](https://www.yieldnetwork.io/blog/plasma-predeposit)

### 4. Linea

**Дата:** 2025-09-10 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Поіменне історичне досьє з матеріалами про умови та подію винагороди.
**Статуси:** source_checked_historical_product; issuer_reported_claims.

**Умови/дії:**

- Офіційні tokenomics називають LXP та onchain-метрики справжнього використання;
- стратегічні builders мають окремий пул.
- Відкриття роздачі 10.09.2025.

**Фактори:** developer_contribution.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Не приймати форумні пропозиції за фінальні правила; точність rounded-метрик обмежена.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано. Повний остаточний поріг eligibility й абсолютні claims.

**Джерела:** [Джерело 1](https://linea.build/blog/linea-tokenomics) · [Джерело 2](https://linea.build/blog/linea-the-token-to-power-ethereums-second-decade) · [Джерело 3](https://linea.build/blog/2025-launched-a-new-era-for-linea-and-l2s)

### 5. Somnia

**Дата:** 2025-09-02 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Поіменне історичне досьє з матеріалами про умови та подію винагороди.
**Статуси:** source_checked_historical_product; live_claim_program.

**Умови/дії:**

- Квести й тестнет, контент і внески спільноти;
- окремі категорії SomniYaps, Quills і Discord.
- Для основної групи: 20% одразу, 80% через вісім щотижневих частин по 10%;
- приблизно 90 днів на виконання.
- В Odyssey обов’язкові місії потребували gas, платні bonus-місії були добровільні.

**Фактори:** community_contribution, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Агент має вести післязапусковий календар. Не трактувати 60 днів як автоматичне отримання 100% без виконання умов.

**Прогалини:** Підсумок claims і повернених невитребуваних токенів. Реальні витрати учасників.

**Джерела:** [Джерело 1](https://blog.somnia.network/p/say-hi-to-somi) · [Джерело 2](https://blog.somnia.network/p/the-somnia-odyssey-a-60-day-adventure) · [Джерело 3](https://www.improbable.io/news/improbable-developed-somnia-launches-mainnet-after-record-breaking-testnet-performance)

### 6. Sahara AI

**Дата:** 2025-06-25 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Sahara AI is a full-stack, AI-native blockchain platform enabling anyone to create, contribute to, and monetize AI development, with a focus on accessibility, equity, and open collaboration.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participation in Data Services Platform (DSP) tasks (earning Sahara Points)
- Participation in Sahara Legends campaign (earning Shards)
- Ecosystem builder or enterprise partner contributions
- Discord community roles (managers, mods, event hosts, platinum role holders, top UGC creators)
- Snapshot for all categories: 2025-05-31 23:59 UTC
- Wallets must be active and pass Sybil/quality checks
- For DSP and Legends: multipliers for active Web3 wallets (holding ≥0.01 ETH at snapshot)
- Sybil/low-quality DSP accounts: 20% reward; Sybil Legends accounts: excluded
- Additional Airdrop Opportunities
- Exchange Airdrops
- OKX Airdrop (0.40%)
- Exclusive airdrop for OKX users participating at TGE
- Binance HODLer Airdrop (2.75%)
- For eligible Binance users, distributed in phases (at launch, +6mo, +9mo)
- Platform-Specific/Community Airdrops

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, activity_diversity, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, developer_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 8.15% of total supply (Airdrops: 5.00% Knowledge Drop, 0.40% OKX, 2.75% Binance HODLer). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/sahara-ai/) · [Посилання з каталогу — потребує перевірки](http://knowledgedrop.saharaai.com/) · [Посилання з каталогу — потребує перевірки](https://discord.gg/sahara-ai) · [Посилання з каталогу — потребує перевірки](https://saharaai.com) · [Посилання з каталогу — потребує перевірки](https://saharaai.com/blog/knowledge-drop) · [Посилання з каталогу — потребує перевірки](https://saharaai.com/blog/sahara-token) · [Посилання з каталогу — потребує перевірки](https://saharalabs.ai/blog/ai-data-collection-and-labeling)

### 7. Newton Protocol

**Дата:** 2025-06-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** The Newton Protocol is a decentralized infrastructure layer for verifiable onchain automation and secure agent authorization. It enables protocols, DAOs, and users to execute complex actions through verifiable agents, without relying on centralized bots or offchain coordination.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Newton.xyz Usage
- Used Newton.xyz to interact with the protocol before June 12, 2025 at 03:59:59 AM UTC
- Community Engagement
- Engaged in community activities through Magic Newton Portal, Guild.xyz and Discord before June 12, 2025 at 03:59:59 AM UTC
- Kaito Yappers Campaign
- Participated in Newton’s Kaito yappers campaign before June 19, 2025 at 11:59:59PM UTC
- Magic Labs Partners
- Performed onchain actions with an active, email-linked Magic Labs embedded wallet on Ethereum mainnet or Polygon mainnet with select partners within the 6-month period between July 1, 2024 and December 21, 2024
- Additional Airdrop Opportunities
- Staking Bonus
- 25% Bonus
- Users who stake their claimed NEWT immediately and keep it staked for 30 consecutive days will receive a one-time 25% bonus
- Distribution
- Bonus staking rewards will be distributed directly to participating Newton.xyz accounts around the end of August 2025
- Verification Methods

**Фактори:** duration_consistency, capital_exposure, activity_diversity, points_quests, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10% of total supply (100,000,000 NEWT). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/newton-protocol/) · [Посилання з каталогу — потребує перевірки](https://blog.newt.foundation/) · [Посилання з каталогу — потребує перевірки](https://blog.newt.foundation/newt-token-airdrop/) · [Посилання з каталогу — потребує перевірки](https://docs.newt.foundation/) · [Посилання з каталогу — потребує перевірки](https://docs.newt.foundation/how-to-guides/newt-token-airdrop) · [Посилання з каталогу — потребує перевірки](https://docs.newt.foundation/newton-protocol/token-distribution-and-vesting) · [Посилання з каталогу — потребує перевірки](https://docs.newt.foundation/newton-protocol/token-distribution-and-vesting#liquidity-support-community-allocation)

### 8. Mango Network

**Дата:** 2025-06-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Mango Network is a Layer 1 blockchain with Multi-VM Omnichain infrastructure, supporting MoveVM, EVM, and SVM, providing secure, modular, and high-performance Web3 infrastructure.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participated in Mango Network testnet events
- Held OG or active community contributor roles
- Mango Points holders: airdrop is proportional, but points are weighted by quality of testnet participation and community contribution
- All tokens are fully unlocked at TGE
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Users with at least 210 Binance Alpha Points can claim 1,666 MGO on a first-come, first-served basis
- Claiming the airdrop consumes 15 Binance Alpha Points
- Must claim on the Alpha Events page within 24 hours of trading open
- If not claimed within 24 hours, eligibility is forfeited
- Claim Process
- Mainnet airdrop claim opens after TGE at checker.mangonet.io
- Users can check eligibility and claim via the official checker
- For Binance Alpha, claim is via Binance Alpha Events page
- Always verify contract address before trading or claiming

**Фактори:** snapshot_state, activity_volume, capital_exposure, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, claim_and_vesting.
**Обсяг:** 5% of total supply (fully unlocked at once). **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/mango-network/) · [Посилання з каталогу — потребує перевірки](https://checker.mangonet.io/) · [Посилання з каталогу — потребує перевірки](https://mangonet.io/) · [Посилання з каталогу — потребує перевірки](https://x.com/MangoOS_Network/status/1935912883982045419) · [Посилання з каталогу — потребує перевірки](https://x.com/MangoOS_Network/status/1937481687358930964) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1937412093415936412)

### 9. Humanity

**Дата:** 2025-06-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Humanity Protocol is a privacy-preserving blockchain with Proof of Humanity consensus, decentralized identity, and zero-knowledge proofs for sybil resistance, self-sovereign identity, and user-owned data.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Verified as a unique human via Humanity Protocol (Proof of Humanity, DID, VC, or palm scan)
- Linked social credentials to Human ID and/or participated in global rollout events
- Contributed to the community (e.g., Discord, Kaito staking, builder, or other real user activity)
- Registered and connected wallet to Humanity account before the claim deadline
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Eligible users must use Binance Alpha Points to claim on the Alpha Events page after trading opens
- Further details announced on June 25, 2025
- Staking & Future Fairdrops
- Staking $H increases eligibility for future Fairdrops from Humanity and partner projects
- Stakers are prioritized for future airdrops and ecosystem rewards
- Claim Process
- Visit
- testnet.humanity.org
- and log in to your Humanity account

**Фактори:** early_participation, activity_volume, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, community_contribution, developer_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** [Not specified; includes Fairdrop and Binance Alpha airdrop]. **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/humanity/) · [Посилання з каталогу — потребує перевірки](https://fairdrops.com) · [Посилання з каталогу — потребує перевірки](https://testnet.humanity.org/) · [Посилання з каталогу — потребує перевірки](https://www.humanity.org/) · [Посилання з каталогу — потребує перевірки](https://www.humanity.org/blog/h-is-here-introducing-the-first-ever-fairdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/Humanityprot/status/1937075561358107030) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1936721860462358771)

### 10. DeLorean

**Дата:** 2025-06-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** DeLorean Labs is the Web3 arm of DeLorean Motor Company, pioneering tokenized electric vehicles and on-chain vehicle reservation, marketplace, and analytics systems on Sui.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Minted a Time Capsule NFT during official mint windows (Oct 28, 2024 or Nov 18, 2024)
- Held a Time Capsule NFT at snapshot (date not specified)
- Completed quest-based tasks on DeLorean Labs Space on Galxe (Airdrop Race)
- For Sui ecosystem communities: received a voucher and completed Lap 1 on Galxe
- For non-Sui communities: completed Lap 1 (Pit Stop) before voucher
- Must complete laps sequentially to earn points for each lap
- Only completed tasks during each lap’s period earn points
- To redeem, must complete Lap 1 and claim during open claim window
- Additional Airdrop Opportunities
- Exchange Airdrops (Binance Alpha)
- Eligible users must use Binance Alpha Points to claim airdrop on the Alpha Events page
- Claim opens when Alpha trading opens (2025-06-24 11:00 UTC)
- Further details announced on June 24
- Platform-Specific Airdrops (Galxe)
- Complete quest-based tasks on Galxe for each lap

**Фактори:** early_participation, snapshot_state, real_product_usage, activity_volume, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting.
**Обсяг:** [Unknown, millions of $DMC tokens distributed; exact % not disclosed]. **Eligible:** [Not specified; includes Time Capsule NFT holders, Galxe quest participants, Binance Alpha users]. **Claimants:** [Not specified].
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/delorean/) · [Посилання з каталогу — потребує перевірки](https://deloreanlabs.com) · [Посилання з каталогу — потребує перевірки](https://x.com/DeLoreanlabs/status/1889365417061413022) · [Посилання з каталогу — потребує перевірки](https://x.com/DeLoreanlabs/status/1934030151790010574) · [Посилання з каталогу — потребує перевірки](https://x.com/DeLoreanlabs/status/1935842065528590540) · [Посилання з каталогу — потребує перевірки](https://x.com/DeLoreanlabs/status/1936089410052731317) · [Посилання з каталогу — потребує перевірки](https://x.com/DeLoreanlabs/status/1937515553091952681)

### 11. Sonic Labs

**Дата:** 2025-06-22 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Sonic is a high-performance EVM Layer 1 blockchain with sub-second finality, fee monetization for developers, and a unique airdrop and vesting mechanism.
**Статуси:** source_checked_historical_product; live_claim_program.

**Умови/дії:**

- Primary Requirements
- Earned allocation through points (testnet, arcade, shards, quests, community engagement)
- Apps (Gems) and users (Points) both eligible for airdrop
- Snapshot taken on June 18, 2025
- Additional Airdrop Opportunities
- App developers (Gems) receive 50% liquid, 50% vested over 90 days
- Users (Points) receive 25% liquid, 75% vested over 270 days as a tradable NFT (fNFT)
- fNFT can be traded on Paintswap secondary market
- Claim Process
- Claim starts after TGE via official frontend (to be announced)
- Users: 25% claimable immediately, 75% linearly vested over 270 days as fNFT
- Users can claim vested portion at any time; unclaimed portion is burned according to burn formula
- Users have 6 months to claim fNFT; after that, unclaimed tokens are burned
- Apps: 50% claimable immediately, 50% vested over 90 days
- Apps have 3 months to claim tokenized Gems; after that, unclaimed tokens are burned
- Special Conditions

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, activity_volume, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, developer_contribution, claim_and_vesting.
**Обсяг:** 80,778,181.95 S (Season 1, 42.4% of 190,500,000 S). **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Відокремлювати кінець накопичення, vesting, фінальний claim і фактичний burn. Не змішувати Sonic Labs із Sonic SVM.

**Прогалини:** Незалежний перерахунок переказів і фінальних одержувачів не виконано. Витрати учасників і поточну працездатність продукту окремо не перевірено.

**Джерела:** [Джерело 1](https://docs.soniclabs.com/funding/sonic-airdrop) · [Джерело 2](https://www.soniclabs.com/blog/sonic-airdrop-burn-and-final-claim-deadline/) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/sonic/) · [Посилання з каталогу — потребує перевірки](https://soniclabs.com) · [Посилання з каталогу — потребує перевірки](https://x.com/SonicAssistant/status/1932855935032074693) · [Посилання з каталогу — потребує перевірки](https://x.com/SonicAssistant/status/1935378430230470724)

### 12. Redbrick

**Дата:** 2025-06-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Redbrick is a gaming and creator platform on BNB Chain, rewarding users, creators, and NFT holders with BRIC tokens for engagement, achievements, and community participation.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Redbrick account with linked EVM wallet, Discord, and X (Twitter) account
- Points: 14.4 Points = 1 BRIC (based on Redbrick account balance)
- Badges: 1 Badge = 1 BRIC
- Genesis Land NFT: 1 Land = 10,000 BRIC (NFT must be held at claim time)
- BRIC Role: 1 Role = 2,000 BRIC (one per account)
- Panda Adventure: Participated and made at least one TON purchase (Aug 21, 2024 – Feb 13, 2025)
- Zealy: Active participation in Zealy quests and community tasks
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Allocation
- 6% of total supply
- Requirements
- Binance Alpha Points
- Distribution
- Two phases

**Фактори:** early_participation, snapshot_state, duration_consistency, activity_volume, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 3% of total supply (Play to Airdrop); 6% Binance Alpha. **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/redbrick/) · [Посилання з каталогу — потребує перевірки](https://airdrop.redbrick.land) · [Посилання з каталогу — потребує перевірки](https://docs.redbrick.land/introduction/what-is-redbrick/usdbric-token-allocation) · [Посилання з каталогу — потребує перевірки](https://medium.com/redbrick-official/panda-adventure-airdrop-guide-4f15a021c2fb) · [Посилання з каталогу — потребує перевірки](https://medium.com/redbrick-official/redbrick-airdrop-guide-e13e2071e9b9) · [Посилання з каталогу — потребує перевірки](https://redbrick.land/) · [Посилання з каталогу — потребує перевірки](https://x.com/RedbrickLand/status/1936268305624711350)

### 13. Artela Network

**Дата:** 2025-06-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Artela Network is a fully on-chain AI platform that rewards community participation, testnet activities, and NFT holders with ART tokens for building the future of decentralized AI.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Register as Artela Renaissance testnet activity user
- Complete “Meet Artela” task and bind social media account before November 23, 2024
- Complete at least two tasks in each phase of Renaissance activities
- Social media accounts must be linked (unlinked accounts not eligible)
- Additional Airdrop Opportunities
- Capila NFT Holders Bonus
- Each address receives ART based on number of NFTs held
- Snapshot taken on January 12, 2025, 00:00:00 UTC
- Example: Holding two Capila NFTs grants two bonus allocations
- Artefarm Players Special Bonus
- Addresses that participated in Artefarm and hold Capila NFTs receive additional rewards
- Check Artefarm official X account for specific details
- Partner Airdrops
- GoPlus Airdrop
- Claimable at

**Фактори:** snapshot_state, duration_consistency, capital_exposure, activity_diversity, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 21,000,000 ART tokens. **Eligible:** Over 150,000 addresses. **Claimants:** [Not specified].
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/artela-network/) · [Посилання з каталогу — потребує перевірки](https://artela.network/) · [Посилання з каталогу — потребує перевірки](https://artela.network/blog/artela-airdrop-explore-your-art-allocation-step-into-the-fully-on-chain-ai-future) · [Посилання з каталогу — потребує перевірки](https://arthome.artela.network/arthome) · [Посилання з каталогу — потребує перевірки](https://arthome.artela.network/arthome/airdrop/aspecta) · [Посилання з каталогу — потребує перевірки](https://arthome.artela.network/arthome/airdrop/goplus) · [Посилання з каталогу — потребує перевірки](https://discord.com/invite/artelanetwork)

### 14. Spark

**Дата:** 2025-06-17 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Spark is an onchain capital allocator with $3.86B deployed across DeFi, CeFi, and RWA, unlocking capital efficiency at scale while maintaining conservative risk profiles through auto-balancing allocations.
**Статуси:** source_checked_historical_product; issuer_reported_distribution.

**Умови/дії:**

- Primary Requirements
- Ignition Airdrop (300M SPK)
- Stablecoin Holdings
- USDS, sUSDS, sUSDC, sDAI, or SAI
- Hold at least $1,000 total across any of these tokens
- Snapshot dates
- April 15, 2023, April 15, 2024, April 15, 2025 (all 23:59:59 UTC)
- Qualifying chains
- Mainnet, Base, Arbitrum
- Possible units
- One for each of the four listed tokens
- xDAI Holdings
- Hold at least 1,000 xDAI on any of the snapshot dates
- Gnosis
- One
- DAI Holdings

**Фактори:** snapshot_state, real_product_usage, nft_or_asset_holding.
**Обсяг:** 300M Ignition + 130.4M Pre-farming Season 1 + Season 2 pool + 500K Layer3 + Overdrive (unclaimed Ignition). **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** У одного емітента різні правила залишків і строки. Належність до мережі та конкретний актив перевіряються для кожної гілки, а не кампанії загалом.

**Прогалини:** Фінальні суми claims, залишки за фазами та витрати учасників не перераховано. Поточний стан продукту потребує окремої перевірки.

**Джерела:** [Джерело 1](https://docs.spark.finance/airdrop/) · [Джерело 2](https://docs.spark.finance/airdrop/pre-farm) · [Джерело 3](https://docs.spark.finance/airdrop/ignition) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/spark-fi/) · [Посилання з каталогу — потребує перевірки](https://app.spark.fi/SPK/airdrop) · [Посилання з каталогу — потребує перевірки](https://docs.spark.fi/airdrop/) · [Посилання з каталогу — потребує перевірки](https://docs.spark.fi/airdrop/ignition#spk-ignition-airdrop) · [Посилання з каталогу — потребує перевірки](https://docs.spark.fi/airdrop/layer3) · [Посилання з каталогу — потребує перевірки](https://docs.spark.fi/airdrop/overdrive) · [Посилання з каталогу — потребує перевірки](https://docs.spark.fi/airdrop/pre-farm)

### 15. Defi App

**Дата:** 2025-06-10 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Crypto's 'Everything App' that makes DeFi as easy as using an iPhone, combining instant cross-chain swaps, yield farming, and perps trading with zero gas fees, zero bridging and full self-custody.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Season 1 Airdrop (500M HOME)
- Degen Arena XP
- Based on 5B total XP generated during 3-month beta
- Trading Activity
- Real trading and yield farming on platform
- Multi-chain Usage
- Bonuses for multi-chain swappers
- Embedded Wallet
- Adoption of embedded wallet features
- Community Participation
- Kaito Yapper rankings and Discord engagement
- Power User Bonuses
- Multi-chain Swappers
- Bonus allocations for cross-chain activity
- Embedded Wallet Adopters

**Фактори:** duration_consistency, real_product_usage, activity_volume, capital_exposure, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 500,000,000 HOME (5% of supply) + potential 500M bonus (community vote). **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/defi-app/) · [Посилання з каталогу — потребує перевірки](https://defi.app) · [Посилання з каталогу — потребує перевірки](https://docs.defi.app/knowledge-base/home-token/tokenomics) · [Посилання з каталогу — потребує перевірки](https://x.com/defidotapp/status/1930986187767857427) · [Посилання з каталогу — потребує перевірки](https://x.com/defidotapp/status/1930986290008248715) · [Посилання з каталогу — потребує перевірки](https://x.com/defidotapp/status/1932396195944464556)

### 16. Skate

**Дата:** 2025-06-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Skate is a multi-VM infrastructure protocol enabling seamless cross-chain dApps, with a native AMM, EigenLayer AVS staking, and a unified liquidity layer across EVM and altVM chains.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Skate Park participants (point system, “Ollies”)
- Range Protocol/SkateFi users (vaults, LPs, managers)
- Discord participants, Kaito Yappers, Kaito Early Yappers
- Community contributors and early supporters
- Binance Alpha Points holders (for Binance Alpha airdrop)
- Additional Airdrop Opportunities
- Additional airdrop reserve for future campaigns and bonus rewards
- “Claim and Stake” option: users who stake their airdrop to Skate EigenLayer AVS receive a 30% bonus
- Claim Process
- Check eligibility and claim at
- claim.skatechain.org
- Connect wallet and follow instructions to claim
- Option to “Claim and Stake” for bonus
- Binance Alpha airdrop: claim via Binance Alpha event page using Alpha Points
- Special Conditions

**Фактори:** early_participation, snapshot_state, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10% of total supply (initial airdrop); additional airdrop reserve for future campaigns. **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/skate/) · [Посилання з каталогу — потребує перевірки](https://claim.skatechain.org) · [Посилання з каталогу — потребує перевірки](https://www.skatechain.org/) · [Посилання з каталогу — потребує перевірки](https://x.com/SkateFDN/status/1930555302417449171) · [Посилання з каталогу — потребує перевірки](https://x.com/SkateFDN/status/1930939249303724494) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1930864260823081216) · [Посилання з каталогу — потребує перевірки](https://x.com/skate_chain/status/1925970127754776864)

### 17. Fly

**Дата:** 2025-06-07 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Fly is a DeFi protocol and DEX aggregator with gamified airdrop and engagement mechanics, rewarding active users, traders, and community members through a dynamic Earndrop™ system.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Active Fly app users, community members, and ambassadors
- Top 1000 Sonic ecosystem users (points leaderboard)
- Boost campaign participants
- Partner community members (see Earndrop Phase 2)
- Airdrop registration and dashboard claim required
- Additional Airdrop Opportunities
- Earndrop™: Ongoing dynamic distribution for active users, traders, and partner communities
- Eggs: Non-tradeable placeholders for xFLY, must be hatched by engaging in the ecosystem (trading, staking, holding xFLY)
- Partner protocols and communities receive Earndrop™ allocations, including: KodiakFi, eulerfinance, ShadowOnSonic, RelayProtocol, NileExchange, XPRESSprotocol, SOCKETProtocol, Rings_Protocol, AmpedFinance, MetropolisDEX, beets_fi, GOGLZ_SONIC, paint_swap, StableJack_xyz, eggsonsonic, StabilityAI, SpookySwap, _WOOFi, tomo_wallet, derpedewdz, Angles_Sonic, HeyAnonai, wagmicom, vfat_io, leap_wallet, Equalizer0x, MuttskiTheDog, SwapXfi, honeypotfinance, TheHedgehog_io, 0xBeraPaw, and more.
- Claim Process
- Claim airdrop and Earndrop™ via the Fly dashboard (
- app.fly.trade/fly
- Eggs must be hatched to claim underlying xFLY tokens
- Hatching requires holding/locking xFLY and/or trading on Fly
- Eggs rot if not hatched (25% per week, fully rot in 28 days)

**Фактори:** snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** [Not specified; includes airdrop and Earndrop™]. **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/fly-trade/) · [Посилання з каталогу — потребує перевірки](http://app.fly.trade/fly) · [Посилання з каталогу — потребує перевірки](https://app.fly.trade/swap) · [Посилання з каталогу — потребує перевірки](https://x.com/flytrade_/status/1915130170672918923) · [Посилання з каталогу — потребує перевірки](https://x.com/flytrade_/status/1931134273702281451) · [Посилання з каталогу — потребує перевірки](https://x.com/flytrade_/status/1932485221393264845)

### 18. YieldNest

**Дата:** 2025-06-05 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** YieldNest is a DeFi-native protocol focused on advanced yield strategies, community governance, and cross-chain expansion, with YND as its governance and utility token.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Accumulated Seeds via YieldNest’s Loyalty Program (restaking, DeFi integrations)
- Season OG (Epoch 1+2): Ended Aug 20, 2024
- Season 1: Aug 20–Oct 22, 2024
- Season 2: Oct 22, 2024–TGE
- Held specific governance tokens or NFTs from partner protocols (Llama NFT, StakeDAO, Curve, Yearn, Convex, Spectra, Thena, Leviathan News, Nest AI, PrimeStaked, Kernel, Bitget, Gate, Zerion)
- Completed exclusive wallet campaigns or XP tasks for certain partners
- Additional Airdrop Opportunities
- Bonus allocations for veSDT, veCRV, veYFI, locked CVX, veTHE, SQUID LP, NEST, and other partner token/NFT holders
- Future airdrops and Seeds seasons planned
- Claim Process
- Claim via the official YieldNest app
- app.yieldnest.finance/claim-ynd
- Connect eligible wallet and follow on-screen instructions
- Only claimable after TGE; always verify the official domain
- No funds required to claim; beware of scams

**Фактори:** snapshot_state, duration_consistency, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 6.56% of total supply (Genesis Airdrop). **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/yieldnest/) · [Посилання з каталогу — потребує перевірки](https://app.yieldnest.finance/claim-ynd) · [Посилання з каталогу — потребує перевірки](https://app.yieldnest.finance/swap?tokenIn=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&tokenOut=0x7159cc276D7d17Ab4b3bEb19959E1F39368a45Ba&ChainId=1) · [Посилання з каталогу — потребує перевірки](https://docs.yieldnest.finance/governance-and-tokenomics/ynd-and-veynd-tokenomics/ynd-token-distribution) · [Посилання з каталогу — потребує перевірки](https://gov.yieldnest.finance/t/official-yieldnest-airdrop-everything-you-need-to-know/161) · [Посилання з каталогу — потребує перевірки](https://medium.com/@yieldnest/yieldnest-ynd-tokenomics-own-govern-earn-7dba54a27960) · [Посилання з каталогу — потребує перевірки](https://www.yieldnest.finance)

### 19. Lagrange

**Дата:** 2025-06-04 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Lagrange is a decentralized ZK Prover Network powering proof generation for ZK rollups, verifiable AI, and modular execution, with a focus on scalable, privacy-preserving cryptographic proofs.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Registered for the $LA airdrop between May 28 and June 2, 2025
- Connected EVM-compatible wallet or X account to the official registration portal
- Chose one supported blockchain network (Ethereum, Base, Arbitrum, Optimism, Polygon, Scroll, Gnosis, Solana) for claiming
- Completed Proof of Uniqueness (PoU) identity verification via Privado ID
- Only the first registered account per unique human is eligible
- Community Engagement
- Users who actively participated in Lagrange’s ecosystem, such as playing Turing Roulette or engaging in other community activities, were eligible. Specific actions like interacting with Lagrange’s platform or events were prioritized.
- Token or NFT Holders
- Eligibility extended to holders of specific tokens or NFTs tied to Lagrange’s ecosystem or partner projects, as outlined during the airdrop announcement. This included certain DeFi or ecosystem-related assets.
- Claim Process
- Registration required on the official portal during the window
- After successful PoU verification, registration is finalized
- Claim $LA tokens at TGE using the registered wallet on the chosen network
- Ensure sufficient gas for claim transaction
- Monitor official channels for TGE and claim instructions

**Фактори:** snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** [Not specified; part of Community & Ecosystem allocation]. **Eligible:** [Not specified]. **Claimants:** [Not specified].
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/lagrange/) · [Посилання з каталогу — потребує перевірки](http://claim.lagrangefoundation.org) · [Посилання з каталогу — потребує перевірки](http://register.lagrangefoundation.org) · [Посилання з каталогу — потребує перевірки](https://www.lagrangefoundation.org) · [Посилання з каталогу — потребує перевірки](https://www.lagrangefoundation.org/blog/introducing-the-lagrange-token) · [Посилання з каталогу — потребує перевірки](https://www.lagrangefoundation.org/blog/register-for-the-la-token-airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/LagrangeFndn/status/1927758012615205180)

### 20. GPUnet

**Дата:** 2025-06-04 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** GPUnet is a decentralized platform democratizing access to high-performance computing and GPU resources for AI, data analysis, and scientific research.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participated as a Quester in Season 1
- Held a node (533 GPU per node)
- Held GPoints from testnet participation
- Series-A investor (remaining allocation)
- Additional Airdrop Opportunities
- Future seasons and roadshow events will distribute additional GPU (1M GPU reserved)
- Claim Process
- Claim airdrop at
- subnet.gpu.net
- TGE and claim opened June 4, 2025
- GPU trading live from June 6, 2025
- Special Conditions
- Only eligible accounts (questers, node holders, GPoints holders, investors) can claim
- Always use official claim portal to avoid scams
- Additional Notes

**Фактори:** snapshot_state, duration_consistency, activity_volume, capital_exposure, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, claim_and_vesting.
**Обсяг:** [Not specified; includes 1M GPU for future seasons/roadshow]. **Eligible:** 11,000+ accounts on GANChain, 294 active validators, 66 providers. **Claimants:** [Not specified].
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/gpu-net/) · [Посилання з каталогу — потребує перевірки](http://subnet.gpu.net) · [Посилання з каталогу — потребує перевірки](https://docs.gpu.net/usdgpu-token-launch) · [Посилання з каталогу — потребує перевірки](https://www.gpu.net/) · [Посилання з каталогу — потребує перевірки](https://x.com/gpunet/status/1930208861731868947) · [Посилання з каталогу — потребує перевірки](https://x.com/gpunet/status/1930222021188956439) · [Посилання з каталогу — потребує перевірки](https://x.com/gpunet/status/1930975386969768161)

### 21. Reddio

**Дата:** 2025-05-29 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Reddio is a parallel EVM network that has achieved stable testnet performance with up to 13,000 TPS, focusing on providing an open parallel EVM network without traditional fundraising methods.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participation in the parallel EVM Testnet
- Holding staking cards
- Community role participation
- UR rarity card holders for OG role
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha
- Binance Alpha Points required for participation
- 400,000,000 RDO allocated for upcoming campaigns
- Additional Notes
- Project has not raised funds through public offerings
- No ICOs, community fundraising, or NFT sales
- Focus on providing open parallel EVM network
- Mainnet launch planned after token launch

**Фактори:** snapshot_state, capital_exposure, points_quests, testnet_participation, nft_or_asset_holding, community_contribution.
**Обсяг:** 8% of total supply (800M RDO). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/reddio/) · [Посилання з каталогу — потребує перевірки](https://docs.reddio.com/zkevm/tokeneconomy/tokendistribution) · [Посилання з каталогу — потребує перевірки](https://reddio.com) · [Посилання з каталогу — потребує перевірки](https://x.com/BinanceWallet/status/1927666304393392338) · [Посилання з каталогу — потребує перевірки](https://x.com/reddio_com/status/1834245971997536485) · [Посилання з каталогу — потребує перевірки](https://x.com/reddio_com/status/1896531055315943530) · [Посилання з каталогу — потребує перевірки](https://x.com/reddio_com/status/1915050393211715712)

### 22. SOPHON

**Дата:** 2025-05-28 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A consumer-focused Layer 2 scaling solution built on ZKsync, aiming to make crypto more accessible and user-friendly.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Node holders (Sophon Guardians)
- Flat amount per holder
- Additional amount based on total node purchase value
- Must have participated in Sophon Node Sale
- Currently operating Light Nodes or Full Nodes
- Early Platform Users
- Users who used Sophon after mainnet launch
- ZKsync power users
- Active community members
- NFT Holders
- Holders of specified NFT collections
- Must be part of “Friends of Sophon” program
- Larger allocation for participating collections
- Additional Airdrop Opportunities
- Exchange Airdrops

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 900,000,000 SOPH (9% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/sophon/) · [Посилання з каталогу — потребує перевірки](https://blog.sophon.xyz) · [Посилання з каталогу — потребує перевірки](https://blog.sophon.xyz/soph-token-airdrop/) · [Посилання з каталогу — потребує перевірки](https://claim.sophon.xyz) · [Посилання з каталогу — потребує перевірки](https://docs.sophon.xyz) · [Посилання з каталогу — потребує перевірки](https://sophon.xyz) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1927678547767796007)

### 23. Resolv

**Дата:** 2025-05-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Resolv is a DeFi yield infrastructure protocol offering sustainable, composable yield strategies and long-term staking rewards, with a focus on aligned participation and ecosystem integrations.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Earned points by using Resolv products (USR, RLP, etc.)
- Points boosted by holding stRESOLV, Blueprint NFT, referrals, and loyalty/Believer status
- Season 1 registration required for airdrop eligibility (closed 2025-05-25)
- Allocation based on total points earned and user segment (see Token Distribution)
- Additional Airdrop Opportunities
- Season 2 (2025-05-09 to 2025-09-09): At least 5% of total supply allocated to points earners and stakers
- Ongoing boosts for early/loyal users, NFT holders, and referrals
- Claim Process
- All tokens distributed as stRESOLV (staked version) at claim
- Claim at
- claim.resolv.xyz
- Unstaking possible (2-week cooldown, ends incentives/boosts)
- Large allocations: 50,000 RESOLV claimable immediately, remainder unlocks over 6 months via Liquifi
- Special Conditions
- Season 1 registration required to confirm/secure allocation

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** Not specified. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/resolv/) · [Посилання з каталогу — потребує перевірки](https://claim.resolv.xyz) · [Посилання з каталогу — потребує перевірки](https://resolv.xyz) · [Посилання з каталогу — потребує перевірки](https://resolvlabs.substack.com/p/resolv-weekly-may-16) · [Посилання з каталогу — потребує перевірки](https://x.com/ResolvCore/status/1927351294580154840)

### 24. Puffverse (PFVS)

**Дата:** 2025-05-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Puffverse is a 3D metaverse platform that connects Web3 virtuality with Web2 reality, featuring PuffGo multiplayer party games and NFT-based gaming experiences.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Gaming Requirements
- Own at least one Puff NFT (Puff Genesis, Puff Football, Puff New Year, or Puff Astronaut)
- Participate in PuffGo League matches
- Download both PuffGo and PuffTown apps
- Use same account for both apps
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha Requirements
- Minimum 204 Alpha Points required
- 15 Alpha Points will be spent upon claiming
- Must claim within 24 hours of opening
- Claim through Binance App using search function
- Access via Alpha Events page
- IGO Points Conversion
- Convert IGO Points to PFVS at 1:1 ratio

**Фактори:** early_participation, duration_consistency, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 875 PFVS per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/puffverse/) · [Посилання з каталогу — потребує перевірки](https://medium.com/@Puffverse/puffgo-official-league-season-is-ready-together-with-the-pfvs-tge-584f2e2b37fa) · [Посилання з каталогу — потребує перевірки](https://puffverse.io) · [Посилання з каталогу — потребує перевірки](https://x.com/Puffverse/status/1927344982702051505) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1926936504703517105) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1927311308870873524)

### 25. SOON

**Дата:** 2025-05-23 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** SOON is a Web3 trading platform focused on copy-trading and livestreaming integration, featuring the $SOON token as the core utility token for governance, staking, and ecosystem incentives across Solana, BNB Chain, and Base networks.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Binance Alpha Requirements
- Minimum 190 Alpha Points required
- 15 Alpha Points consumed upon claiming
- Must claim within 24 hours
- Source: Binance Alpha Airdrop Program
- Additional Airdrop Opportunities
- Community Distribution
- SOONest (5%): 100% at TGE
- SOONer (8%): 3-month vesting
- SOON Squad (8%): 6-month cliff, 12-month vesting
- SOON Pill (8%): 12-month cliff, 36-month vesting
- Community Incentives (10%): 20% at TGE, 36-month vesting
- NFT Holders (12%): 17% at TGE, 12-month vesting
- Streamer Incentives
- Up to 80% commission on trading fees

**Фактори:** snapshot_state, activity_volume, capital_exposure, activity_diversity, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, developer_contribution, referrals, claim_and_vesting.
**Обсяг:** 180 SOON per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/soon/) · [Посилання з каталогу — потребує перевірки](https://airdrop.soo.network) · [Посилання з каталогу — потребує перевірки](https://medium.com/@soon_SVM/simpfor-fun-v2-launch-with-soon-tokenomics-and-roadmap-bf69dfa15a7e) · [Посилання з каталогу — потребує перевірки](https://simpfor.fun) · [Посилання з каталогу — потребує перевірки](https://soo.network/) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1925824065018741001) · [Посилання з каталогу — потребує перевірки](https://x.com/soon_svm/status/1924379566531096632)

### 26. LoopedHYPE

**Дата:** 2025-05-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** LoopedHYPE ($LOOP) is a yield-generating DeFi protocol on HyperEVM, enabling users to earn multipliers and airdrops by staking LOOP and participating in liquid looping strategies.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the LoopedHYPE airdrop was based on the following requirements
- Phase-1 Requirements
- Snapshot taken on March 8, 2025
- Eligible users: LHYPE holders and participants in liquid looping strategies before the snapshot
- stLOOP (staked LOOP) amount determines Looping Mode and points multiplier
- Users can stake LOOP at any time before each phase’s closing to earn a multiplier for the following drop
- Missed Phase-1? Buy and stake LOOP before Phase-2 closes to earn the next multiplier
- LP positions in stLOOP/LOOP and LOOP/LHYPE pools also earn points
- Late claim possible for missed registration (allocation at a later date if eligible)

**Фактори:** snapshot_state, capital_exposure, points_quests, nft_or_asset_holding, claim_and_vesting, ranking_or_tier.
**Обсяг:** Not specified (multi-phase, TVL milestone-based). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/loopedhype/) · [Посилання з каталогу — потребує перевірки](https://docs.loopingcollective.org) · [Посилання з каталогу — потребує перевірки](https://loopedhype.com/airdrop-registration) · [Посилання з каталогу — потребує перевірки](https://loopingcollective.org) · [Посилання з каталогу — потребує перевірки](https://x.com/Looped_HYPE)

### 27. Huma Finance

**Дата:** 2025-05-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Huma Finance is a decentralized payfi protocol that has facilitated over $4.4 billion in payfi transactions, focusing on bringing real yield on-chain through its ecosystem partners.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Liquidity Providers
- Provided liquidity to designated pools (Huma Institutional and Huma 2.0) before snapshot
- Total Feathers outstanding at snapshot: 2,682,116,734
- 65% of airdrop allocation
- Ecosystem Partners
- Active payfi ecosystem partners contributing to payfi yield opportunities
- 25% of airdrop allocation
- 6-month vesting schedule
- Community Engagement
- Content creators
- Active participants in social campaigns (Discord, Galxe, Kaito)
- Community contributions to protocol development and security
- 10% of airdrop allocation
- Fully unlocked at TGE
- Additional Airdrop Opportunities

**Фактори:** snapshot_state, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, community_contribution, claim_and_vesting.
**Обсяг:** 5% of total supply (Season 1). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/huma-finance/) · [Посилання з каталогу — потребує перевірки](https://huma.finance/) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1926917675105571014) · [Посилання з каталогу — потребує перевірки](https://x.com/humafinance) · [Посилання з каталогу — потребує перевірки](https://x.com/humafinance/status/1925439234955255912)

### 28. Tokyo Games Token (TGT)

**Дата:** 2025-05-21 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Tokyo Games Token (TGT) is an ecosystem token issued under the philosophy of 'Shaping the Future of Web3 Gaming from Japan', backed by Japan's leading gaming companies including Cygames, SBI, and gumi.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Binance Alpha Requirements
- Minimum 199 Alpha Points required
- 15 Alpha Points will be spent upon claiming
- Must claim within 24 hours of opening
- Claim through Binance App using search function
- Access via Alpha Events page
- Source: Binance Alpha Airdrop Program
- Additional Airdrop Opportunities
- Telegram Mini App (LOVE DROP)
- Available through Catizen Telegram Mini App
- 43 million potential users
- 5% fee in TGT deducted at claim time
- No claim required for in-game usage
- Immutable Passport
- Requires Immutable Passport account

**Фактори:** capital_exposure, activity_diversity, points_quests, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 500 TGT per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/tokyo-games-token/) · [Посилання з каталогу — потребує перевірки](https://medium.com/@TOKYOBEAST/catizen-tokyo-beast-marketing-partnership-announcement-495568e4245d) · [Посилання з каталогу — потребує перевірки](https://medium.com/@TOKYOBEAST/how-to-claim-tgt-airdrop-rewards-including-the-tgt-vip-card-and-tokyo-beast-love-drop-f40b98024ff2) · [Посилання з каталогу — потребує перевірки](https://tokyogamestoken.gitbook.io/tgt-whitepaper) · [Посилання з каталогу — потребує перевірки](https://tokyogamestoken.io) · [Посилання з каталогу — потребує перевірки](https://x.com/TOKYOGAMES_FDN/status/1922278432655953969) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1925130505424408604)

### 29. Merlin Chain

**Дата:** 2025-05-20 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Merlin Chain is a native Bitcoin Layer2 committed to empowering Bitcoin's native assets, protocols, and products on Layer1 through its Layer2 network, integrating ZK-Rollup network, decentralized oracle network, and on-chain BTC fraud proof modules.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Minimum 193 Binance Alpha points required
- Must confirm claim within 24 hours of start time
- Claiming consumes 15 Binance Alpha points
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha airdrop
- Claim window: 24 hours from start time
- Must confirm claim on Alpha Events page
- Points consumed: 15 Binance Alpha points
- Claim Process
- Pre-registration: Not required
- Claim confirmation required on Alpha Events page
- Automatic forfeiture if not claimed within 24 hours
- Special Conditions
- Claims must be confirmed within 24 hours

**Фактори:** activity_diversity, points_quests, claim_and_vesting.
**Обсяг:** 1,000 MERL per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Стежити за початком/кінцем claim, vesting, unlock і поверненням невитребуваних токенів.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/merlin-chain/) · [Посилання з каталогу — потребує перевірки](https://binance.com/en/support/faq/detail/12e7f2e555704f9c8e852d1c1afb032a) · [Посилання з каталогу — потребує перевірки](https://medium.com/@merlinchaincrypto/announcement-on-merlins-seal-airdrop-claim-61408e836ca2) · [Посилання з каталогу — потребує перевірки](https://medium.com/@merlinchaincrypto/introducing-merlin-chain-token-merl-376fe43f180d) · [Посилання з каталогу — потребує перевірки](https://medium.com/@merlinchaincrypto/merlins-seal-the-biggest-fair-launch-of-layer2-5614001b2582) · [Посилання з каталогу — потребує перевірки](https://merlinchain.io) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1924754627322364113)

### 30. Giza

**Дата:** 2025-05-20 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Giza is an AI-powered DeFi platform pioneering agent-driven finance, rewarding users for capital commitment, community engagement, and technical contributions.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Giza airdrop was based on the following requirements
- ARMA Users
- Entrusted capital to Giza’s autonomous agents (ARMA)
- Points formula: Points = 0.01 × USD deposited × hours
- Minimum 60 points required (e.g., $50 for 5 consecutive days)
- 11 allocation tiers based on point totals
- Snapshot taken on April 8, 2024
- Social Contributors
- Participation in Layer3, Galxe, or Megaphone campaigns
- Layer3: All tasks + ARMA activation (2,155/3,016 qualified)
- Galxe: All social tasks + 1 referral (3,635/66,175 qualified)
- Megaphone: All tasks, max 20 referrals (9,090/87,866 qualified)
- Each qualified campaign: 180 GIZA per user
- Extensive filtering to prevent sybil activity
- Community Stewards
- Discord Pharaoh Role: 1,800 GIZA per user (leadership, engagement)

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, community_contribution, referrals, anti_sybil_identity, ranking_or_tier.
**Обсяг:** 13,800,000 GIZA (approx. 1.37% of total supply). **Eligible:** 15,882 (across all categories). **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/giza/) · [Посилання з каталогу — потребує перевірки](https://gizatech.xyz/blog/giza-airdrop) · [Посилання з каталогу — потребує перевірки](https://www.gizatech.xyz/) · [Посилання з каталогу — потребує перевірки](https://x.com/gizatechxyz)

### 31. Xterio

**Дата:** 2025-05-19 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Xterio is a gaming and AI platform that combines strategic multi-phase airdrops with comprehensive reward mechanisms to build and maintain a vibrant ecosystem for gamers, AI product users, and developers.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- NFT Holders Airdrop
- Based on Dinosty NFT holdings
- Snapshot taken 36 hours after announcement
- 1% of total supply (10,000,000 XTER) allocated
- Game Incentives
- Roar holders: 0.5% (5,000,000 XTER)
- Skin collection points: 0.4% (4,000,000 XTER)
- Top 200 players: 0.1% (1,000,000 XTER)
- Based on in-game power ranking
- Top 100 players from Zone 1 & 2 combined
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Minimum 194 Binance Alpha points required
- Must claim within 24 hours of start time
- Claiming consumes 15 Binance Alpha points

**Фактори:** snapshot_state, activity_diversity, points_quests, nft_or_asset_holding, developer_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 2% of total supply (20,000,000 XTER). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/xterio/) · [Посилання з каталогу — потребує перевірки](https://docs.xter.io/token-economy/token-allocation) · [Посилання з каталогу — потребує перевірки](https://www.xter.io/) · [Посилання з каталогу — потребує перевірки](https://x.com/XterioGames/status/1877027068375916856) · [Посилання з каталогу — потребує перевірки](https://x.com/XterioGames/status/1877688566727459107) · [Посилання з каталогу — потребує перевірки](https://x.com/XterioGames/status/1890432230280839608) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1924374642170417472)

### 32. REVOX

**Дата:** 2025-05-17 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** REVOX is a Web3 ecosystem focused on loyalty and engagement rewards, featuring the $REX token for governance, premium features access, and enhanced benefits across all REVOX products and partnerships.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Platform Engagement
- REVOX Points > 1999 with activity growth after October 1
- REVOX Premium Points > 0
- AI Credits Purchase ($) for exclusive rewards
- Snapshot taken on December 7, 2024
- NFT Ownership
- 3-Star Catto NFT holders receive basic $REX rewards
- 4-Star Catto NFT holders receive enhanced $REX rewards
- Snapshot taken on December 5, 2024
- ReadON APP Engagement
- ReadON DAO Points > 99
- ReadON SBT Level > 2
- Snapshot taken on November 19, 2024
- Galxe Loyalty
- Galxe Loyalty Points > 499

**Фактори:** snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 1.5M REX total distribution. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/revox/) · [Посилання з каталогу — потребує перевірки](https://docs.revox.ai/) · [Посилання з каталогу — потребує перевірки](https://docs.revox.ai/tokenomics/tokenomics-v2#token-global-allocation) · [Посилання з каталогу — потребує перевірки](https://readonofficial.medium.com/revox-airdrop-eligibility-criteria-99e25e4f70b7) · [Посилання з каталогу — потребує перевірки](https://reward.revox.ai/) · [Посилання з каталогу — потребує перевірки](https://www.revox.ai/) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1923634605749596413)

### 33. MapleStory NEXPACE

**Дата:** 2025-05-15 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** NEXPACE is a Web3 IP-expansion initiative backed by Nexon, featuring the NXPC token as an integral part of the MapleStory Universe (MSU) ecosystem, bringing the iconic 23-year-old gaming IP to blockchain.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Genesis Point (Galxe)
- Completed MSU Quest during Genesis period
- Quest completion before March 4, 2025
- Points weighted for Pioneer Test and Gear Up period
- Internal sybil filtering applied
- NXPC Competition
- Participation in Enhancement and Marketplace categories
- Based on NESO token usage
- Real-time leaderboard tracking
- Total distribution: 2,013,610 NXPC
- MapleStory N 7-Day Check-In
- Complete 7 daily check-ins during Pioneer Test
- Reward: 10 NXPC per eligible user
- MSU Alphabet Fusion
- Submit Alphabet, Number, or Name Length NFTs

**Фактори:** early_participation, real_product_usage, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 14,222,857 NXPC (1.422% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/maplestory/) · [Посилання з каталогу — потребує перевірки](https://medium.com/maplestory-universe/press-release-nexpace-launches-maplestory-n-and-nxpc-token-charting-a-new-chapter-for-6076e8af7627) · [Посилання з каталогу — потребує перевірки](https://msu.io) · [Посилання з каталогу — потребує перевірки](https://msu.io/claim) · [Посилання з каталогу — потребує перевірки](https://msu.io/news/notices/2816534) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1922888013685850437)

### 34. Privasea AI

**Дата:** 2025-05-14 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Privasea AI is a privacy-focused AI platform that rewards long-term community engagement through a unique token distribution mechanism that incentivizes patient participation.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- ImHuman App Users
- 657,641 eligible wallets
- Must be verified by Proof of Humanity
- Minimum 400 stars required
- Base allocation: 110 PRAI tokens
- Additional tokens based on star count
- Testnet Participants
- DeepSea Testnet node operators: 38,574 wallets
- Must complete at least one phase
- Quest Participants
- Galxe questers: 20,239 wallets
- Minimum 100 points at snapshot
- Early supporters: 4,283 wallets
- WorkHeart USB node owners: 5,000 wallets
- OKX Wallet, Gate Web3 & Intract quest participants: ~35,000 wallets

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, referrals, anti_sybil_identity, claim_and_vesting.
**Обсяг:** Not specified. **Eligible:** ~760,737 wallets. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/privasea-ai/) · [Посилання з каталогу — потребує перевірки](https://airdrop.privasea.ai) · [Посилання з каталогу — потребує перевірки](https://binance.com/en/events/privasea-tge) · [Посилання з каталогу — потребує перевірки](https://binance.com/en/support/faq/detail/12e7f2e555704f9c8e852d1c1afb032a) · [Посилання з каталогу — потребує перевірки](https://www.privasea.ai/) · [Посилання з каталогу — потребує перевірки](https://x.com/BinanceWallet/status/1922561073288548641) · [Посилання з каталогу — потребує перевірки](https://x.com/Privaseafdn)

### 35. Solana Name Service

**Дата:** 2025-05-13 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Solana Name Service (SNS) is a decentralized naming system for Solana addresses, providing human-readable .sol domain names and identity management on the Solana blockchain.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Solana Name Service airdrop was based on the following requirements
- Domain Holders
- Held a .sol domain name
- Set a primary .sol domain
- Special categories: 9, 99, 999, 10k, 100k domain holders
- Top 50 buyers by volume
- Community Members
- Solana communities (including monkedao.sol and pyth.sol subdomain holders)
- $FIDA token holders
- Active SNS ambassadors
- Note: Some domains may not resolve properly if
- Listed for sale and in escrow
- Managed by sub-registrar and in escrow
- Recently linked to new unverified wallet

**Фактори:** snapshot_state, activity_volume, nft_or_asset_holding, community_contribution, anti_sybil_identity.
**Обсяг:** 630 million $SNS (claimed). **Eligible:** Not specified. **Claimants:** 27,000+ wallets.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/solana-name-service/) · [Посилання з каталогу — потребує перевірки](https://airdrop.sns.id/) · [Посилання з каталогу — потребує перевірки](https://docs.sns.id/) · [Посилання з каталогу — потребує перевірки](https://docs.sns.id/collection/tokenomics/sns-token#usdsns-genesis-airdrop) · [Посилання з каталогу — потребує перевірки](https://www.sns.id/) · [Посилання з каталогу — потребує перевірки](https://www.sns.id/blog/sns-tge-lfg-campaign) · [Посилання з каталогу — потребує перевірки](https://x.com/sns)

### 36. Redacted (RDAC)

**Дата:** 2025-05-13 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Redacted is a community-focused platform built with the belief that strong communities deserve real ownership, featuring a comprehensive ecosystem including Jirasan, MultiFarm, and Redacted Airways.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Community Requirements
- Jirasan NFT holders (based on final pre-TGE snapshot)
- Magically Crates users with at least one Eth mainnet transaction in last 6 months
- MultiFarm pool participants (7,500 wallets)
- Redacted Airways Quest participants
- Swipooor Beta Testers (top 100 wallets by engagement)
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha Requirements
- Minimum 205 Alpha Points required for standard claim
- Users with 170-204 Alpha Points AND UID ending with 7 qualify for lucky airdrop
- 15 Alpha Points will be spent upon claiming
- Must claim within 24 hours of opening
- Claim through Binance App using search function
- Access via Alpha Event page

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 482 RDAC per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/redacted/) · [Посилання з каталогу — потребує перевірки](https://claim.redactedgroup.io) · [Посилання з каталогу — потребує перевірки](https://redactedgroup.io) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1922224856843661700) · [Посилання з каталогу — потребує перевірки](https://x.com/redactedcoin/status/1913201240953250181) · [Посилання з каталогу — потребує перевірки](https://x.com/redactedcoin/status/1915377798249697662) · [Посилання з каталогу — потребує перевірки](https://x.com/redactedcoin/status/1915737728454459820)

### 37. Doodles

**Дата:** 2025-05-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Doodles is an NFT-based social platform launching its native token DOOD on Solana, with plans to bridge to Base L2, focusing on community-driven content creation and ecosystem growth.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- NFT holding requirements
- OG Doodles
- Space Doodles (with Space Miles bonus)
- Dooplicators
- Genesis Boxes
- Iconic Wearables
- Grail Wearables
- Exclusive Wearables
- Essential Wearables
- Posters
- Beta Passes
- Certified Virals
- Doodles Passes
- Transaction thresholds: None specified
- Time period specifications: Snapshot at TGE

**Фактори:** early_participation, snapshot_state, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 298,865,583 DOOD (Binance Alpha) + 30% of total supply (NFT holders). **Eligible:** 30,271 (Binance Alpha) + NFT holders. **Claimants:** To be determined.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/doodles/) · [Посилання з каталогу — потребує перевірки](https://dood.doodles.app) · [Посилання з каталогу — потребує перевірки](https://dood.doodles.app/faq) · [Посилання з каталогу — потребує перевірки](https://doodles.app) · [Посилання з каталогу — потребує перевірки](https://dreamnet.doodles.app/tokenomics/distribution-and-value-alignment) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1920073738676060627) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1920771570420580551)

### 38. Space and Time

**Дата:** 2025-05-08 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized database network that enables fast queries and tamper-proof analytics for onchain apps, using a sub-second ZK Coprocessor optimized for SQL to let smart contracts process data at scale.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Testnet Users: Active usage of Space and Time leading up to mainnet
- Community NFT Holders: Holders of official Community NFT collection (versions 1-5)
- Community Participants: Active contributors on X, Discord, Zealy, and Galxe
- Community Leaders: Official moderators and advocates
- Testnet Node Operators: Ran a Space and Time node during early testnet phases
- Chainlink Ecosystem Participants: Including eligible LINK Stakers
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Minimum 150 Alpha Points required for 512 SXT
- Lucky airdrop of 512 SXT for users with 66-149 Alpha Points and UIDs ending in 1
- Distribution within 10 minutes after Alpha listing
- Chainlink Rewards
- Available to eligible LINK Stakers
- Based on time-weighted average stake
- Snapshot taken on March 31, 2025

**Фактори:** early_participation, snapshot_state, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 375,000,000 SXT (7.5% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/space-and-time/) · [Посилання з каталогу — потребує перевірки](https://blog.chain.link/chainlink-rewards-season-genesis/) · [Посилання з каталогу — потребує перевірки](https://www.spaceandtime.io/) · [Посилання з каталогу — потребує перевірки](https://www.spaceandtime.io/blog/gigaclaim-0-eligibility-and-how-to-claim) · [Посилання з каталогу — потребує перевірки](https://www.spaceandtime.io/blog/introducing-sxt-chain) · [Посилання з каталогу — потребує перевірки](https://x.com/SpaceandTimeDB/status/1919754683322888636) · [Посилання з каталогу — потребує перевірки](https://x.com/SpaceandTimeDB/status/1919754707771523235)

### 39. PumpBTC

**Дата:** 2025-05-01 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** PumpBTC is an AI-driven, cross-chain Bitcoin staking and liquidity protocol, enabling BTC holders to earn yield, participate in governance, and unlock DeFi opportunities across 27+ ecosystems.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Season 1 & 2 Participants: Active in staking, points, referral programs, or community activities
- Holders of PumpBTC Pass, PumpBera, Beramas NFT, or Thank You Satoshi Pizza
- PumpFellow Participants: Contributed via the PumpFellow program
- Community Contributors: Engaged meaningfully on socials, leaderboards, or events (e.g., voted for PumpBTC on Kaito pre-TGE)
- Additional Airdrop Opportunities
- Staking PUMP increases airdrop rewards and ecosystem incentives
- vePUMP (vote-escrowed PUMP) for long-term commitment: lock PUMP for governance voting, yield sharing, and boosted rewards
- Claim Process
- Airdrop claim is live at
- airdrop.pumpbtc.xyz
- All airdrop tokens are fully unlocked at TGE
- Check eligibility on the official claim portal
- Caution: Only use official links to avoid scams
- Special Conditions
- vePUMP: Lock PUMP to receive governance power, yield sharing, and boosted rewards

**Фактори:** snapshot_state, duration_consistency, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 90,000,000 PUMP (9% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/pumpbtc/) · [Посилання з каталогу — потребує перевірки](https://airdrop.pumpbtc.xyz) · [Посилання з каталогу — потребує перевірки](https://discord.com/invite/pumpbtc) · [Посилання з каталогу — потребує перевірки](https://mainnet.pumpbtc.xyz/) · [Посилання з каталогу — потребує перевірки](https://pumpbtc.gitbook.io/) · [Посилання з каталогу — потребує перевірки](https://x.com/Pumpbtcxyz) · [Посилання з каталогу — потребує перевірки](https://x.com/Pumpbtcxyz/status/1907072128207536446)

### 40. BOOP

**Дата:** 2025-05-01 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** BOOP is a social-focused platform on Solana that rewards community engagement and trading activity through airdrops and token incentives, with a unique cult-based reward system for token holders and creators.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Social Airdrop
- Based on X (Twitter) activity
- Tiered distribution based on
- Quality of followers
- Engagement metrics
- Social presence
- 50% immediate allocation
- 50% distributed to token holders
- Source: Community Rewards
- Degen Airdrop
- Based on Solana memecoin trading activity
- Snapshot taken in early April 2025
- Requires 0.5 SOL worth of BOOP-launched token purchase
- Source: Trading Rewards
- Additional Airdrop Opportunities

**Фактори:** early_participation, snapshot_state, activity_volume, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 291 BOOP per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/boop/) · [Посилання з каталогу — потребує перевірки](https://boop.fun) · [Посилання з каталогу — потребує перевірки](https://docs.boop.fun/airdrops) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1919293546730754210) · [Посилання з каталогу — потребує перевірки](https://x.com/boopdotfun/status/1921578683611095282)

### 41. Haedal Protocol

**Дата:** 2025-04-29 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Haedal Protocol is a Liquid Staking Token (LST) protocol on the Sui blockchain, offering haSUI, haWAL, and haeVault products for DeFi users.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Active users of Haedal products (haSUI, haWAL, haeVault)
- Users who leveraged Haedal LSTs across major DeFi protocols on Sui
- Core community members and social supporters
- Active moderators and ambassadors
- Content creators and community contributors
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha: 356 HAEDAL for users with ≥80 Alpha Points
- Distribution within 10 minutes after trading goes live
- Partner Community Airdrops
- Partner communities included
- Bucket
- Cetus
- DeepBook
- Hippo

**Фактори:** snapshot_state, activity_volume, capital_exposure, activity_diversity, points_quests, community_contribution, claim_and_vesting.
**Обсяг:** 5% of total HAEDAL supply. **Eligible:** ~1 million users on Sui. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/haedal/) · [Посилання з каталогу — потребує перевірки](https://haedal.io) · [Посилання з каталогу — потребує перевірки](https://haedal.xyz/airdrop) · [Посилання з каталогу — потребує перевірки](https://medium.com/@haedal/haedal-airdrop-is-here-a-gift-to-the-sui-ecosystem-f53ebaed792f) · [Посилання з каталогу — потребує перевірки](https://web3.okx.com/airdrop-checker/3) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1917133095108563152)

### 42. Initia

**Дата:** 2025-04-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Initia is a multichain infrastructure protocol and rollup framework, enabling full-stack appchains and interwoven economies across Cosmos, Ethereum, and beyond.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Testnet Participants
- Jennie NFT with level 3 or above
- At least 2 of 5 attainable stickers (including Frozen Jennie)
- Participation in The Initiation: Part One and Two testnets
- 194,294 eligible testnet users
- Sybil filtering applied
- Interwoven Stack Partners
- Top 2,000 LayerZero users (across Ethereum, Optimism, Arbitrum, Base, BSC) as of Sep 21, 2024, who claimed LayerZero airdrop and continued usage
- Top 2,000 IBC users (Noble, Osmosis, Neutron) as of May 14, 2024
- Top 2,000 milkTIA holders (Osmosis, protocols) as of Feb 28, 2025
- Social Contributors
- 769 Discord roles (Militia Captain, Militia Lieutenant, OG Telegram, Community Event Winner, Eco-Reclaimers, Holo Weavers, Isolation Navigators, Yapper, First Weeker, etc.) as of Mar 28, 2025
- 369 Init Intern’s Unpaid Telegram Group members as of Mar 28, 2025
- Top 4,000 Kaito users on Initia Leaderboard (X/Yapper) as of Mar 28, 2025
- Additional Airdrop Opportunities

**Фактори:** snapshot_state, duration_consistency, activity_diversity, testnet_participation, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 50,000,000 INIT (5% of total supply). **Eligible:** 194,294 (testnet) + partner and social contributors. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/initia/) · [Посилання з каталогу — потребує перевірки](https://init.xyz/checker) · [Посилання з каталогу — потребує перевірки](https://initia.xyz/) · [Посилання з каталогу — потребує перевірки](https://kaito.ai/) · [Посилання з каталогу — потребує перевірки](https://x.com/initiaFDN/status/1906666010910060586)

### 43. DOLO (Dolomite)

**Дата:** 2025-04-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Dolomite is a decentralized lending protocol that enables users to supply and borrow assets across multiple networks including Arbitrum One, Mantle, and Polygon zkEVM.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Snapshot taken on January 6th, 2025 at 0:00 UTC
- Platform usage metrics
- Dollar value of assets supplied
- Dollar value of assets borrowed
- Amount of time supplying
- Amount of time borrowing
- Dolomite XP Program participation
- Minerals Program participation
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Eligibility period: April 15-21, 2025
- Requirements
- Maintain daily average holding of $50+ on Binance Exchange and Wallet
- Accumulate $100+ worth of Alpha purchases on Binance Exchange
- Allocation: 260 DOLO per eligible user

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, nft_or_asset_holding, claim_and_vesting, ranking_or_tier.
**Обсяг:** 20% of total supply. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/dolomite/) · [Посилання з каталогу — потребує перевірки](https://docs.dolomite.io) · [Посилання з каталогу — потребує перевірки](https://docs.dolomite.io/dolo/airdrop) · [Посилання з каталогу — потребує перевірки](https://dolomite.io) · [Посилання з каталогу — потребує перевірки](https://dolomite.io/airdrop) · [Посилання з каталогу — потребує перевірки](https://dolomite.io/checker) · [Посилання з каталогу — потребує перевірки](https://x.com/BinanceWallet/status/1914641805322359189)

### 44. Zora

**Дата:** 2025-04-23 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Zora is a decentralized NFT platform and marketplace that enables creators to mint, trade, and earn from their digital content through various protocols including Coins, Auction House, and Markets.
**Статуси:** source_checked_historical_product; live_claim_program.

**Умови/дії:**

- Primary Requirements
- Posted, minted, traded or referred on Zora platform
- Activity must be on official Zora factories and contracts
- Includes ERC-721, ERC-1155, and ERC-20 contracts
- Covers all official Zora platforms (web, iOS, Android)
- Includes third-party platforms integrating Zora Protocol
- Additional Airdrop Opportunities
- Binance Alpha Airdrop
- Must have purchased at least $50 on Alpha using Spot or Funding accounts
- Purchase period: March 22, 2025 00:00:00 UTC to April 20, 2025 23:59:59 UTC
- Allocation: 4,276 ZORA per eligible user
- Special Conditions
- Personal and work-related wallets of Zora employees are excluded
- Addresses flagged as high-risk by Elliptic are ineligible
- No end date for claiming retroactive airdrop
- Additional Notes

**Фактори:** snapshot_state, real_product_usage, activity_volume, developer_contribution, referrals, claim_and_vesting.
**Обсяг:** 1,000,000,000 ZORA (10% of total supply). **Eligible:** 2,415,024 unique addresses. **Claimants:** Not specified.
**Урок:** Відрізняти дату TGE, snapshot і дату роздачі; eligible count не записувати в recipients.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано. Точні кінцеві claims і фінальні строки.

**Джерела:** [Джерело 1](https://support.zora.co/en/articles/5653441) · [Джерело 2](https://claim.zora.co/faq) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/zora/) · [Посилання з каталогу — потребує перевірки](https://claim.zora.co) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1914285019268317268) · [Посилання з каталогу — потребує перевірки](https://x.com/zora/status/1915060861095256356) · [Посилання з каталогу — потребує перевірки](https://x.com/zora/status/1915060866451697997) · [Посилання з каталогу — потребує перевірки](https://zora.co)

### 45. MilkyWay

**Дата:** 2025-04-23 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** MilkyWay is the first and largest modular liquid staking and restaking protocol for Celestia, rewarding users for staking, restaking, and community engagement through mPoints and NFTs.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- mPoint holders: Earned by staking, restaking, and DeFi usage since December 2023
- Minimum 500 mPoints (after multipliers) to qualify (sybil-resistant cutoff)
- Moolitia NFT holders: Early supporters with whitelist access
- milkINIT Testers: Participants in Initia testnet
- EVM wallet must be linked on MilkyWay for NFT and DeFi activity
- Additional Airdrop Opportunities
- MILK cartons: Each applies a 1.25x boost to mPoints
- Bonus campaigns: Up to 4x point boosters and special events (Milklympics, etc.)
- Community engagement and feedback
- Claim Process
- Check allocation at
- Airdrop Checker
- Claim on-chain at TGE or opt-in to claim on CEX (MEXC, Gate.io, KuCoin)
- For CEX claim: Connect wallet, opt-in, select exchange, enter details, submit before April 26, 2025, 12 PM UTC
- mPoints snapshot and eligibility finalized before claim

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10% of total supply (100,000,000 MILK). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/milk/) · [Посилання з каталогу — потребує перевірки](https://massdrop.milkyway.zone) · [Посилання з каталогу — потребує перевірки](https://milk.xyz/airdrop) · [Посилання з каталогу — потребує перевірки](https://milkyway.zone/) · [Посилання з каталогу — потребує перевірки](https://milkyway.zone/airdrop) · [Посилання з каталогу — потребує перевірки](https://milkyway.zone/checker) · [Посилання з каталогу — потребує перевірки](https://x.com/MilkyWayFDN/status/1915095643007389879)

### 46. Balance

**Дата:** 2025-04-21 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Balance is a Web3 platform that combines social features with AI agents, offering a comprehensive ecosystem for community engagement and rewards.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- E-PAL Users
- Log in to Balance website using Web3 wallet
- Bind E-PAL email address
- Tokens airdropped directly to connected wallet
- Balance Early & Active Supporters
- Complete Invite & Quest tasks through Points System
- Participate in creating and interacting with AI Agents
- Balance Community Active Twitter Users
- Connect wallet to airdrop claiming page
- Bind Twitter account
- Balance Pioneer Badge NFT Holders
- Connect wallet holding Pioneer Badge NFT
- Automatic eligibility check
- Balance Key Node Operators
- Connect wallet holding Key Node

**Фактори:** early_participation, snapshot_state, activity_volume, activity_diversity, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, referrals, claim_and_vesting.
**Обсяг:** 3,500 EPT per eligible user. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/balance-fun/) · [Посилання з каталогу — потребує перевірки](https://balance.fun) · [Посилання з каталогу — потребує перевірки](https://foundation.balance.fun) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/0x6F7ce819004184B358E4A0670f6Cd95d1BE0febb/oBummT5_FJlXCmPoTh_Qk_z4kkcXT9q9RvjhYMLS0-w) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1913127423404614035)

### 47. Magic Eden

**Дата:** 2025-04-17 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Magic Eden is a leading cross-chain NFT marketplace, rewarding active users with $ME tokens for staking and quest participation.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Active participation in Magic Eden Quests during Season 1 (Chapter 1)
- Staking $ME tokens during Season 1
- Both staking and quest participation required (passive stakers not eligible)
- User rank determined by combination of staking power (amount and lockup duration) and quest activity
- Snapshot taken at March 31, 2025, 11:59:59pm UTC
- Additional Airdrop Opportunities
- Future seasons planned, with $ME rewards distributed based on user rank (staking + quest participation)
- Leaderboard and boosted actions (swaps, Ordinals, Solana/ETH NFTs) in Season 2
- Claim Process
- Airdrop sent to user’s ‘claim wallet’ (same as TGE claim wallet)
- No action required for eligible users; tokens are distributed automatically
- Claim wallet can be viewed in the Earning tab (wallet with 🔗 icon)
- All allocations are final and cannot be adjusted
- Special Conditions
- Only active quest participants with staking are eligible (passive stakers excluded)

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10,000,000 $ME (Season 1). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/magiceden/) · [Посилання з каталогу — потребує перевірки](https://help.magiceden.io/en/articles/10953399-me-airdrop-faq-season-1-quests) · [Посилання з каталогу — потребує перевірки](https://magiceden.io/) · [Посилання з каталогу — потребує перевірки](https://x.com/MagicEdenComm/status/1912935273509330969)

### 48. Wayfinder

**Дата:** 2025-04-10 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Wayfinder is an AI-powered platform that combines social missions and wallet missions with a unique caching program, offering a comprehensive ecosystem for community engagement and rewards.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Community missions participants
- Wallet missions participants
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha: Users who traded on Alpha using Spot or Funding accounts before April 10, 2025, 00:00 UTC
- Allocation: 490 PROMPT per eligible user
- Distribution: Before April 10, 2025, 13:10 UTC
- Special Conditions
- Unclaimed rewards from Social and Wallet missions will be swept back to Foundation on May 15, 2025, 23:59 UTC
- Reclaimed tokens will be re-allocated to Community Future Reward Incentives pool
- Kaito rewards will be returned to Community Future Reward Incentives pool on May 10, 2025
- Caching program continues on weekly basis for 3-year duration

**Фактори:** duration_consistency, activity_volume, activity_diversity, points_quests, community_contribution, claim_and_vesting.
**Обсяг:** 490 PROMPT (Binance Alpha) + Social missions (1%) + Wallet missions (1%). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/wayfinder/) · [Посилання з каталогу — потребує перевірки](http://app.wayfinder.ai) · [Посилання з каталогу — потребує перевірки](http://cache.wayfinder.ai/claim-prompt) · [Посилання з каталогу — потребує перевірки](https://cache.wayfinder.ai/claim-prompt) · [Посилання з каталогу — потребує перевірки](https://www.wayfinder.ai) · [Посилання з каталогу — потребує перевірки](https://x.com/AIWayfinder/status/1910306083924484521) · [Посилання з каталогу — потребує перевірки](https://x.com/AIWayfinder/status/1923090665367535712)

### 49. Mind Network

**Дата:** 2025-04-10 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Mind Network is building a quantum-resistant, fully homomorphic encryption (FHE) infrastructure for secure, privacy-preserving data and AI computation in Web3.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- CitizenZ Passport NFT Holders
- Must have held the NFT before the snapshot (2025-03-31 23:59 UTC).
- Mainnet Contributors
- Delegated $vFHE at snapshot; allocation based on amount delegated. TGV from Mind Network activities qualifies for a multiplier.
- Advocate Program
- Based on successful and valid referrals.
- AgentConnect Hub Registrants
- All verified registrants share 0.3% of the pool; additional 0.7% reserved for future waves.
- Community Contributors
- Eligible if any of the following
- Actively participated in the testnet
- Exclusive Discord role
- Zealy participation
- At least 600 Mind Network Galxe points
- Hold a Mind FHEellow NFT

**Фактори:** snapshot_state, activity_diversity, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, referrals, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** Not specified. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/mind-network/) · [Посилання з каталогу — потребує перевірки](https://agent.mindnetwork.xyz/airdrop) · [Посилання з каталогу — потребує перевірки](https://forms.gle/5eJD2RmFKrG2UfEw8) · [Посилання з каталогу — потребує перевірки](https://mindnetwork.medium.com/mind-network-airdrop-188ff3d78fa5) · [Посилання з каталогу — потребує перевірки](https://mindnetwork.xyz) · [Посилання з каталогу — потребує перевірки](https://x.com/mindnetwork_xyz/status/1908888827047051764)

### 50. Babylon

**Дата:** 2025-04-10 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Babylon is a Bitcoin staking protocol that enables BTC holders to earn rewards by staking their Bitcoin while maintaining self-custody.
**Статуси:** source_checked_historical_product; allocation_or_rules_only.

**Умови/дії:**

- Primary Requirements
- Phase 1 Bitcoin staking participation
- Pioneer Pass NFT ownership (snapshot at Polygon block 68305555)
- GitHub contributions to eligible repositories
- Additional Airdrop Opportunities
- Stake Participation Airdrop (30M BABY)
- Cap 1: 550 BABY per stake (30K stakes)
- Cap 2: 150 BABY per stake (14K stakes)
- Cap 3: 100 BABY per stake (112K stakes)
- Base Staking Reward Airdrop (335M BABY)
- Proportional to stake size and duration
- Shared among active stakes at each BTC block
- Minus finality provider commission
- Bonus Staking Reward Airdrop (200M BABY)
- Multiplier on base staking reward
- Requires successful transition to Phase 2

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, developer_contribution, ranking_or_tier.
**Обсяг:** 600M BABY (6% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Реєстрація та підпис умов потрібні навіть без claim-транзакції; майбутній bonus не зараховувати як вже отриманий.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано.

**Джерела:** [Джерело 1](https://babylon.foundation/blogs/babylon-early-adopters-airdrop) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/babylon/) · [Посилання з каталогу — потребує перевірки](https://baby.tech) · [Посилання з каталогу — потребує перевірки](https://baby.tech/bedrock) · [Посилання з каталогу — потребує перевірки](https://baby.tech/checker) · [Посилання з каталогу — потребує перевірки](https://baby.tech/etherfi) · [Посилання з каталогу — потребує перевірки](https://baby.tech/lombard) · [Посилання з каталогу — потребує перевірки](https://baby.tech/pumpbtc)

### 51. ArcadiaFi

**Дата:** 2025-04-10 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** ArcadiaFi is a DeFi liquidity management platform on Base, enabling users to earn points and rewards through lending, borrowing, and referrals, with a unique airdrop and staking mechanism.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Earn Arcadia points by lending and borrowing assets on ArcadiaFi
- Minimum 10,000 points to qualify for airdrop (cut-off)
- Points earned for
- Lending: 1 point per $1 per hour
- Borrowing: 0.1–0.3 points per $1 of debt per hour (varies by season)
- Points decay if funds are withdrawn
- Points boosts for early participation, v1 users, OGs, and veAERO holders
- Sybil resistance: linear conversion up to sybil threshold, quadratic for large holders
- Additional Airdrop Opportunities
- Referrals: Earn points for referring users (10% of referred points, 5% boost for referees)
- Featured Pools: 5% boost for pools with partner tokens
- Loyalty: Higher rewards for users who remain active and do not withdraw
- Season 2: Additional 10% airdrop if approved by stAAA holders
- Claim Process
- Airdrop claims go live at TGE

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, referrals, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10% of total supply (Season 1); up to 20% if Season 2 passes. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/arcadia/) · [Посилання з каталогу — потребує перевірки](https://arcadia.finance/) · [Посилання з каталогу — потребує перевірки](https://arcadiafinance.medium.com/introducing-arcadia-points-092d470793f6) · [Посилання з каталогу — потребує перевірки](https://arcadiafinance.medium.com/points-season-2-rewards-and-loyalty-2808cc212961) · [Посилання з каталогу — потребує перевірки](https://arcadiafinance.medium.com/points-season-4-referrals-d4a580c3623d) · [Посилання з каталогу — потребує перевірки](https://x.com/ArcadiaFi/status/1909720448579064023) · [Посилання з каталогу — потребує перевірки](https://x.com/Earndrop_io/status/1910705481208955144)

### 52. Ooga Booga

**Дата:** 2025-04-04 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized exchange on Berachain that rewards active traders and community members through a fee-based airdrop system, with special recognition for early testnet participants.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Generated trading fees for Ooga Booga
- Better quotes than BEX or Kodiak by 0.15%
- Positive slippage contributions
- Top 3,000 fee contributors
- Additional Airdrop Opportunities
- Role Multipliers
- Gud Bera: 1.5x multiplier
- Super Bera: 2x multiplier
- Genesis Bera: 1.25x multiplier
- Presale Multiplier
- Fjord and Ramen Finance participants: 1.1x multiplier
- Stacks with role multiplier
- Maximum one role multiplier applied
- Special Conditions
- Role multipliers don’t stack with each other

**Фактори:** early_participation, activity_volume, testnet_participation, community_contribution, ranking_or_tier.
**Обсяг:** ~10% of total supply. **Eligible:** ~3,000 (top fee contributors). **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Вести журнал транзакцій, feedback і знайдених помилок; тестнет сам по собі не гарантує токени.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/oogaboogoa/) · [Посилання з каталогу — потребує перевірки](https://0xoogabooga.notion.site/faq) · [Посилання з каталогу — потребує перевірки](https://app.oogabooga.io) · [Посилання з каталогу — потребує перевірки](https://app.oogabooga.io/airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/0xoogabooga/status/1907922854991045061) · [Посилання з каталогу — потребує перевірки](https://x.com/0xoogabooga/status/1907947831895486568)

### 53. StakeStone

**Дата:** 2025-04-03 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** StakeStone is an omnichain liquidity infrastructure protocol, enabling efficient, active liquidity provision and distribution across multiple blockchains.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Provided liquidity in supported protocols/campaigns (BNB, Berachain, Manta, BTC, etc.)
- Participated in referral programs
- Accumulated points in campaign-specific systems (STONE-W1, STONE-BTC, Bera-Wave, STONE-BNB)
- Held G-NFT (Genesis NFT) as of March 2024
- Early participation in Berachain Vaults, Aria Premiere, GOAT Network, etc.
- BTC ecosystem early supporters (deposited >1 ETH)
- Manta New Paradigm depositors (>1 ETH + at least one other campaign)
- cSTONE early supporters
- Other qualifying contributions as recognized by StakeStone
- Additional Airdrop Opportunities
- Binance Web3 Wallet campaign rewards (distributed later)
- Future incentives from the “Airdrop and future incentives” pool (e.g., Berachain PoL Vaults)
- Claim Process
- Claim opens: 2025-04-03 10:30 AM UTC
- Claim duration: 30 days (ends 2025-05-03 10:30 AM UTC)

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 74,000,000 STO (7.4% of total supply, first wave). **Eligible:** Over 330,000. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/stakestone/) · [Посилання з каталогу — потребує перевірки](https://airdrop.stakestone.io) · [Посилання з каталогу — потребує перевірки](https://medium.com/@Stake_Stone_/96b7fb0976f3) · [Посилання з каталогу — потребує перевірки](https://medium.com/@Stake_Stone_/stakestone-airdrop-deep-dive-96b7fb0976f3) · [Посилання з каталогу — потребує перевірки](https://stakestone.io) · [Посилання з каталогу — потребує перевірки](https://x.com/Stake_Stone/status/1907678727129137444)

### 54. Hyperlane

**Дата:** 2025-04-03 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Hyperlane is a permissionless interoperability protocol enabling open, secure, and customizable cross-chain messaging and bridging across 140+ blockchains.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Sent messages using Hyperlane protocol before 2025-02-28 23:59:59 UTC (snapshot)
- Paid at least ~$5 in protocol fees
- Staked/validated on Hyperlane
- Provided liquidity (e.g., TIA LP on Manta/Arbitrum before 2024-01-30)
- Held eligible NFTs (Celestine Sloth Society, Mammoths)
- Top contributors in Pilot Academy
- Chains/apps using Hyperlane as canonical bridge receive increased weighting
- Sybil filtering: negative multipliers for likely Sybil addresses; full exclusion for addresses in Chaos Labs dataset or with <$5 in fees
- Additional Airdrop Opportunities
- Expansion Rewards: Ongoing, quarterly distribution over 4 years, based on protocol usage
- HyperStreak multiplier: Up to 1.6x for continuous holding of stHYPER and protocol usage each quarter (max by preclaiming stHYPER or staking on TGE day)
- Foundation may boost rewards for actions like canonical bridge implementation, liquidity provision, feature integrations, ISM/hook development
- Claim Process
- Preclaim period: 2025-04-03 to 2025-04-14 04:00 UTC (users add addresses, choose HYPER/stHYPER, specify network)
- Claim period: Starts week of 2025-04-20, ends 2025-05-22 13:00 UTC

**Фактори:** snapshot_state, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 75,000,000 HYPER (7.5% of total supply at TGE for Expansion Drop). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/hyperlane/) · [Посилання з каталогу — потребує перевірки](http://claim.hyperlane.foundation) · [Посилання з каталогу — потребує перевірки](https://hyper.xyz/checker) · [Посилання з каталогу — потребує перевірки](https://hyperlane.xyz) · [Посилання з каталогу — потребує перевірки](https://medium.com/@hyperlane_fdn/introducing-hyper-f3846883f1f5) · [Посилання з каталогу — потребує перевірки](https://x.com/hyperlane/status/1907796961257992465) · [Посилання з каталогу — потребує перевірки](https://x.com/hyperlane_fdn/status/1907796297442275549)

### 55. Wizzwoods

**Дата:** 2025-03-31 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Wizzwoods is the largest and most active gaming ecosystem on Berachain, pioneering cross-chain GameFi with NFTs, sustainable tokenomics, and deep DeFi integration.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Hold eligible NFTs (Chrono-Wizard Bear, Berachain Bear series, Tabichain Captain Node)
- Complete cross-chain transfer (for Chrono-Wizard Bear holders)
- Be among the first 2,000 claimants for Berachain Bear or Tabichain Captain Node rewards
- Be a top 100 or randomly selected marketplace trader by transaction volume
- Additional Airdrop Opportunities
- Future cross-chain gaming and NFT campaigns as Wizzwoods expands to partner chains
- Claim Process
- Start at
- hub.wizzwoods.com
- Complete required actions (e.g., cross-chain transfer, claim via wallet)
- Claiming opens at TGE (2025-03-31)
- Details and deadlines to be announced on official channels
- Special Conditions
- Some rewards are limited to the first 2,000 claimants per category
- Marketplace trader rewards based on volume or random selection

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, node_validator_work, nft_or_asset_holding, claim_and_vesting.
**Обсяг:** Not specified (includes $WIZZ tokens and exclusive Morph Card NFTs). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/wizzwoods/) · [Посилання з каталогу — потребує перевірки](https://hub.wizzwoods.com/) · [Посилання з каталогу — потребує перевірки](https://x.com/WizzwoodsGame/status/1905238551698276848)

### 56. KINTO

**Дата:** 2025-03-31 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** An L2 rollup designed to accelerate the transition to an on-chain financial system, featuring user-owned KYC/AML and native account abstraction for enhanced security and user experience.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Mining Program Participants
- Base mining rewards (1.5x during Sakura)
- $K staking (50% extra mining bonus)
- Trading volume requirements
- Lending requirements
- Referral Program
- New user referrals
- Requirements for referred users
- Deposit $500 for 1+ month
- Trade $5,000 in perpetuals
- Stake 10+ $K tokens
- Additional Airdrop Opportunities
- Trading Rewards
- Swap $5,000 worth of assets
- Lend $5,000 worth of collateral

**Фактори:** duration_consistency, real_product_usage, activity_volume, capital_exposure, referrals, anti_sybil_identity, ranking_or_tier.
**Обсяг:** 1% of token supply (Sakura Season). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kinto/) · [Посилання з каталогу — потребує перевірки](http://engen.kinto.xyz/explore/K) · [Посилання з каталогу — потребує перевірки](https://kinto.xyz) · [Посилання з каталогу — потребує перевірки](https://medium.com/mamori-finance) · [Посилання з каталогу — потребує перевірки](https://medium.com/mamori-finance/airdrop-season-one-momiji-8aee69b665a1) · [Посилання з каталогу — потребує перевірки](https://medium.com/mamori-finance/kintos-launch-engen-1755d7cd53d6) · [Посилання з каталогу — потребує перевірки](https://medium.com/mamori-finance/spring-mining-season-sakura-d529db8399f7)

### 57. Usecorn

**Дата:** 2025-03-28 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A Bitcoin-focused DeFi network built on Arbitrum that enables BTC holders to access DeFi markets through BTCN, a hybrid tokenized Bitcoin, with features including lending, staking, and governance through the $CORN token.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Kaito AI yapping participation and BTCFi leadership
- Kaito Genesis NFT holders (snapshot: March 10, 2025, held 30+ days)
- $KAITO holder badge holders (2x $CORN boost)
- Link X account to wallet in Corn App within 14 days of TGE
- Additional Airdrop Opportunities
- Initial Token Distribution (10%)
- Kernels Season 1 (Pre-network, offchain points)
- Kernels Season 2 (Points on Maizenet)
- Yap to Eat with Kaito.ai
- Harvester Vaults (Pre-TGE rewards)
- New Programs
- Cornfields Season 1 (Network-wide incentives)
- $CORN Locking (21-week lock period)
- Claim Process
- 14-day window to link X account to EVM wallet

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10% of total supply (210M $CORN). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/usecorn/) · [Посилання з каталогу — потребує перевірки](https://blog.usecorn.com/corn-tokenomics-e56e73e4580f) · [Посилання з каталогу — потребує перевірки](https://corn.money/airdrop) · [Посилання з каталогу — потребує перевірки](https://usecorn.com) · [Посилання з каталогу — потребує перевірки](https://x.com/use_corn/status/1905261736946712857)

### 58. Immortal Rising 2

**Дата:** 2025-03-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A blockchain-based idle RPG where players earn and trade assets through play-to-earn (P2E) mechanics, built on the Immutable zkEVM blockchain.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Immortal Rising 2 airdrop was based on the following requirements
- ORB Point Accumulation
- Earned through daily check-ins, in-game missions, social tasks (e.g., X posts, Discord events), and referrals
- ORB impact directly affects airdrop allocation
- Participation in P2A Launchpool Seasons
- Engagement in Seasons 1, 2, and 3
- Season 2 (ended Jan 9, 2025) split a 50M $IMT pool between ORB Impact and Soulbound Token (SBT) tracks
- Immutable Passport Integration
- Players must link their Immutable Passport to their in-game profile and Immortal Vault account
- Pre-Registration and Early Participation
- Users who pre-registered before Sept 19, 2024, or joined the Closed Beta Test (CBT) had bonus eligibility
- Community Engagement
- Participation in events like Skill Showdown or Guild Promotions on Discord helped earn ORB/SBTs

**Фактори:** early_participation, duration_consistency, activity_volume, points_quests, community_contribution, referrals, anti_sybil_identity, ranking_or_tier.
**Обсяг:** 70 million $IMT (7% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/immortal-rising-2/) · [Посилання з каталогу — потребує перевірки](http://news.immortalrising2.com/news/imtairdrop) · [Посилання з каталогу — потребує перевірки](https://airdrop.immortalrising2.com) · [Посилання з каталогу — потребує перевірки](https://immortalrising2.com)

### 59. Zeebu

**Дата:** 2025-03-26 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Zeebu is a decentralized B2B settlement platform that aims to reshape enterprise payments through blockchain technology and DeFi solutions.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Must have joined before March 31, 2025
- Must pass Sybil verification
- Must complete tier-specific tasks
- Additional Airdrop Opportunities
- Tier System
- Blue Tier: SocialFi + Holding
- Silver Tier: SocialFi + Staking
- Gold Tier: Node Staking + Delegation
- Platinum Tier: Node Activation + Governance Participation
- ZIP Farming
- Blue Tier: 4.04 Billion ZIP (55,790 users)
- Silver Tier: 7.37 Billion ZIP (126 users)
- Gold Tier: 23.57 Billion ZIP (23 users)
- Platinum Tier: 3.88 Trillion ZIP (58 users)
- Special Conditions

**Фактори:** capital_exposure, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 60M ZBU. **Eligible:** 39,900 verified users (after Sybil protection). **Claimants:** 8,685 users claimed 69,961.9725 ZBU.
**Урок:** Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Контролювати uptime, версію клієнта, епохи, ключі та фактичну вартість сервера.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/zeebu/) · [Посилання з каталогу — потребує перевірки](https://www.zeebu.com/blog/zbu-season-1-airdrop-official-distribution-timeline-claim-details) · [Посилання з каталогу — потребує перевірки](https://x.com/zeebuofficial/status/1910347161960694224) · [Посилання з каталогу — потребує перевірки](https://x.com/zeebuofficial/status/1911124739143418151) · [Посилання з каталогу — потребує перевірки](https://x.com/zeebuofficial/status/1915444081381302737) · [Посилання з каталогу — потребує перевірки](https://zeebu.fi)

### 60. Term Finance

**Дата:** 2025-03-26 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Term Finance is a fixed-rate lending protocol on Ethereum, rewarding early adopters and active community members with $TERM tokens for protocol usage and engagement.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Earn Term Points through protocol usage
- Participating in auctions
- Lending via Blue Sheets
- Depositing into Vaults
- Genuine community engagement
- Discord discussions
- Twitter interactions
- Community contests, quests, educational initiatives
- Other social activities contributing to Term’s growth
- Rewards scale with points and quality of engagement
- Additional Airdrop Opportunities
- Ongoing protocol activity tracked for future seasons
- Season 2 airdrop planned; $TERM holdings will be in play for Season 2
- Claim Process
- Visit

**Фактори:** early_participation, duration_consistency, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 5,000,000 $TERM (Season One). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/term-finance/) · [Посилання з каталогу — потребує перевірки](http://app.term.finance/claim-basic) · [Посилання з каталогу — потребує перевірки](http://app.term.finance/rewards) · [Посилання з каталогу — потребує перевірки](http://term.finance/rewards) · [Посилання з каталогу — потребує перевірки](https://app.term.finance/) · [Посилання з каталогу — потребує перевірки](https://x.com/term_labs/status/1904684778688749572)

### 61. Singularity Finance

**Дата:** 2025-03-26 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Singularity Finance is a decentralized AI solutions platform that tokenizes AI compute power, bringing the Real World Asset (RWA) AI economy onchain while making AI solutions accessible to everyone.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Testnet Participation
- Complete testnet tasks
- Accumulate points through testing
- Points remain eligible for mainnet airdrop
- Additional Airdrop Opportunities
- Point Multipliers
- Hold SDAO tokens
- Hold SFI tokens
- Stake SDAO tokens
- Stake SFI tokens
- Special Conditions
- Testnet access continues until end of March 2025
- New tasks will be added for additional point accumulation
- Points multiplier applies for long-term supporters
- Early contributions are recognized and rewarded

**Фактори:** early_participation, capital_exposure, points_quests, testnet_participation, ranking_or_tier.
**Обсяг:** Not specified. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/singularity/) · [Посилання з каталогу — потребує перевірки](https://singularity.finance/rewards) · [Посилання з каталогу — потребує перевірки](https://singularityfinance.ai) · [Посилання з каталогу — потребує перевірки](https://singularityfinance.ai/testnet/claim) · [Посилання з каталогу — потребує перевірки](https://x.com/Singularity_Fi) · [Посилання з каталогу — потребує перевірки](https://x.com/Singularity_Fi/status/1877747479032340815) · [Посилання з каталогу — потребує перевірки](https://x.com/Singularity_Fi/status/1880929949122744653)

### 62. Kiloex

**Дата:** 2025-03-26 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** KiloEx is a decentralized perpetual exchange operating on BNBChain, opBNB, and Manta, offering trading, staking, and governance features with a focus on user rewards and ecosystem growth.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Trading Points: Earned for all trades on KiloEx’s mainnet
- 24.5 points per 1000 USDT traded
- Deposit Points: Earned for all deposits
- Before Oct 23, 2023: (USDT amount * Hours/24) * 0.05
- After Oct 23, 2023: (USDT amount * Hours/24) * 0.025
- After Feb 1, 2024: (USDT amount * Hours/24) * 0.0125
- Check-in Points: Daily check-ins
- Progressive points: 1-7 points per day
- Maximum 28 points after 7 consecutive days
- Referral Points: 15-25% bonus on referred users’ points
- OAT Points: Earned through various activities
- Additional Airdrop Opportunities
- Exchange Listings
- Binance Alpha 2.0
- Bybit

**Фактори:** duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, referrals, ranking_or_tier.
**Обсяг:** 100 million KILO (10% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kiloex/) · [Посилання з каталогу — потребує перевірки](https://app.kiloex.io/airdrop/claim?chain=opBNB) · [Посилання з каталогу — потребує перевірки](https://docs.kiloex.io) · [Посилання з каталогу — потребує перевірки](https://docs.kiloex.io/kiloex/airdrop-and-reward/airdrop-pioneer-season) · [Посилання з каталогу — потребує перевірки](https://kilo.network)

### 63. KelpDAO

**Дата:** 2025-03-26 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** KelpDAO is a DeFi ecosystem with multiple products including Kelp (rsETH), Gain (tokenized vaults), and Kernel (shared security layer), currently managing ~$2B in assets.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Season 1 participant (ended December 31, 2024)
- Minimum 150 Kernel Points/Kelp Grand Miles
- ~$100 worth of ETH restaked during Season 1
- Successfully passed Sybil verification
- Additional Airdrop Opportunities
- Season 1 Airdrop
- Minimum 100 KERNEL per eligible wallet
- Top ~1% wallets receive larger allocations
- 70% unlocked at TGE for top wallets
- Remaining 30% vested over 3 months (10% each month)
- All other wallets receive 100% at TGE
- Special Conditions
- Must have participated in Season 1 (ended December 31, 2024)
- Must pass Sybil verification
- Season 2 is ongoing for future rewards

**Фактори:** duration_consistency, capital_exposure, activity_diversity, points_quests, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 10% of total KERNEL supply. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kelpdao/) · [Посилання з каталогу — потребує перевірки](https://blogs.kerneldao.com/blog/kernel-airdrop-early-checker-is-live) · [Посилання з каталогу — потребує перевірки](https://kernel.community/airdrop) · [Посилання з каталогу — потребує перевірки](https://kernel.community/checker) · [Посилання з каталогу — потребує перевірки](https://kerneldao.com) · [Посилання з каталогу — потребує перевірки](https://kerneldao.com/airdrop-checker) · [Посилання з каталогу — потребує перевірки](https://kerneldao.com/claim-airdrop)

### 64. Particle Network

**Дата:** 2025-03-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A chain-agnostic trading platform powered by Particle Network's chain abstraction technology, enabling universal accounts and cross-chain trading through the $PARTI token.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- $PARTI Diamonds holders (snapshot: March 24, 2025, 07:00 AM UTC)
- $ALLY holders (snapshot: March 24, 2025, 08:00 AM UTC)
- CAPYBARA NFT holders (snapshot: March 24, 2025, 04:00 AM UTC)
- The People’s Launchpad users
- Particle Pioneer users
- Particle WaaS users (limited quantity, first-come, first-served)
- Additional Airdrop Opportunities
- OKX Wallet Bonus
- Extra 5% reward
- Maximum 100 tokens
- First-come, first-served basis
- Claim Process
- Connect community accounts to UniversalX account
- Check eligibility through UniversalX platform
- Claim tokens through UniversalX

**Фактори:** early_participation, snapshot_state, duration_consistency, activity_volume, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 9% of total supply. **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/particle/) · [Посилання з каталогу — потребує перевірки](https://blog.particle.network/parti-airdrop/) · [Посилання з каталогу — потребує перевірки](https://universalx.app) · [Посилання з каталогу — потребує перевірки](https://universalx.app/grow/airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/ParticleNtwrk/status/1904515174620422574)

### 65. Nillion

**Дата:** 2025-03-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Nillion is a decentralized network focused on secure and private data processing.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Nillion (NIL) airdrop was based on the following requirements
- Community Engagement
- Requirements
- Held a core community Discord Role (e.g., Volunteer, Blind Warrior, Nill Pilled, Marshal, OG)
- Membership of the Nillion Assembly community (survey participation)
- Minted one of the 8 POAPs during the weekly community Blinding Ceremony livestreams
- Participated in the early community Nillion Network naming competition on JokeRace
- Reason
- Demonstrates long-term commitment, leadership, and active participation in the Nillion community and cultural events.
- Reward
- Calculated based on individual Discord roles, survey participation, POAP minting, and JokeRace voting. Participants received NIL tokens according to their engagement and contributions.
- Developer and Open Source Engagement
- Submitted a quality Pull Request to public Nillion repositories
- Built a hackathon project or bounty project on Nillion
- Participated in high-quality GitHub Discussions, assisted with technical content, developer experience testing, or attended Developer Office Hours
- Used the Nillion SDK with telemetry enabled and provided an ETH address

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, developer_contribution, anti_sybil_identity, ranking_or_tier.
**Обсяг:** 75,000,000 NIL tokens (7.5% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/nillion/) · [Посилання з каталогу — потребує перевірки](https://nillion.com/) · [Посилання з каталогу — потребує перевірки](https://nillion.com/news/nillion-airdrop-is-here/) · [Посилання з каталогу — потребує перевірки](https://nillion.notion.site/Token-Allocation-FAQs-1b31827799b480fe86c9c336188a4375) · [Посилання з каталогу — потребує перевірки](https://x.com/nillionnetwork/status/1899811137203458313) · [Посилання з каталогу — потребує перевірки](https://x.com/nillionnetwork/status/1904157568118722690)

### 66. RHEA Finance

**Дата:** 2025-03-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized finance platform with a unique reputation-based reward system.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the RHEA Finance airdrop was based on the following requirements
- Point System Ranking
- Every transaction on RHEA earns points.
- No Initial Restrictions
- There are no rules or restrictions until the system goes live.
- Reputation Yield
- oRHEA tokens grow based on user activity—the more you engage, the more you earn.
- Conversion & Continuity
- oRHEA tokens will later be converted into RHEA and xRHEA, with continued rewards after the Token Generation Event (TGE).

**Фактори:** real_product_usage, points_quests, ranking_or_tier.
**Обсяг:** 10% of total RHEA supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Зберігати формулу score, межі tier і capped/uncapped частини; не припускати лінійну конвертацію.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/rhea-finance/) · [Посилання з каталогу — потребує перевірки](https://rhea.finance) · [Посилання з каталогу — потребує перевірки](https://x.com/rhea_finance/status/1897682652582596670)

### 67. GooDog

**Дата:** 2025-03-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** GooDog is a community-first meme and governance token on DBK Chain, distributing 50% of supply via airdrop to DeBank users, NFT minters, testers, and liquidity providers.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- DeBank Web3 ID minters
- DeBank Social Rank Top 50,000 (tiered rewards by rank)
- DBK Chain Genesis NFT minters
- Rabby Desktop Genesis NFT minters
- Snapshot-based eligibility (block numbers specified for NFT minters)
- Additional Airdrop Opportunities
- Crowdfund/LP incentives (first-come, first-served)
- Referral rewards (10,000 GD per claimed user, +50% bonus with web3id referral)
- Top 1000 followers & reposters of GooDog/Official account
- Home/DEX testers (first-come, first-served)
- Claim Process
- Automatic airdrop for top recipients (over 500,000 GD)
- Manual claim option opens March 22, 2025 (UTC 0)
- Claim window: 6 months from opening
- Claim via

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, nft_or_asset_holding, community_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 50% of total supply (various categories, see below). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/goodog/) · [Посилання з каталогу — потребує перевірки](https://debank.com/stream/3086303) · [Посилання з каталогу — потребує перевірки](https://debank.com/stream/3090170) · [Посилання з каталогу — потребує перевірки](https://dex.goodog.io/) · [Посилання з каталогу — потребує перевірки](https://docs.goodog.io/ignition) · [Посилання з каталогу — потребує перевірки](https://goodog.io/) · [Посилання з каталогу — потребує перевірки](https://goodog.io/ignition)

### 68. Amnis Finance

**Дата:** 2025-03-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** The top liquid staking protocol on Aptos, empowering APT holders to maximize returns while maintaining liquidity.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Early Adopters
- The airdrop is designed to reward early users of Amnis Finance.
- APT Stakers
- Users who staked APT within the Amnis protocol and minted amAPT.
- Liquidity Providers
- Users who provided amAPT/APT liquidity on platforms such as LiquidSwap and PancakeSwap.
- stAPT Depositors
- Those who deposited stAPT on Aries.
- Participants accumulate points through these activities, influencing the amount of AMI tokens they can claim.

**Фактори:** early_participation, snapshot_state, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, claim_and_vesting.
**Обсяг:** 80,000,000 AMI tokens (8% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/amnis-finance/) · [Посилання з каталогу — потребує перевірки](https://amnis.finance/) · [Посилання з каталогу — потребує перевірки](https://docs.amnis.finance/) · [Посилання з каталогу — потребує перевірки](https://docs.amnis.finance/amnis-protocol/events/amnis-retroactive-airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/AmnisFinance/status/1903487149384892559) · [Посилання з каталогу — потребує перевірки](https://x.com/AmnisFinance/status/1904503689764872221)

### 69. Lisk

**Дата:** 2025-03-20 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized platform designed to enable developers to build scalable blockchain applications.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Participants needed to fulfill several conditions to qualify for the Lisk airdrop
- 1. Wallet Setup
- Must use an
- EVM-compatible wallet
- (e.g., MetaMask, Rabby, or Phantom) connected to the
- Lisk network
- Adding Lisk Mainnet to the wallet might require
- bridging ETH
- from Ethereum Mainnet or another Layer 2 network to cover transaction fees.
- 2. Guild Verification (Anti-Sybil Protection)
- To prevent fraudulent claims, users had to meet at least
- two
- of the following conditions
- Complete a
- standard CAPTCHA
- verification (anti-spam check).

**Фактори:** duration_consistency, real_product_usage, activity_volume, capital_exposure, points_quests, nft_or_asset_holding, community_contribution, developer_contribution, referrals, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** Up to 15 million LSK tokens. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/lisk/) · [Посилання з каталогу — потребує перевірки](https://lisk.com) · [Посилання з каталогу — потребує перевірки](https://lisk.com/blog/posts/lisk-airdrop-season1-ends/) · [Посилання з каталогу — потребує перевірки](https://lisk.com/blog/posts/lisk-lsk-airdrop/) · [Посилання з каталогу — потребує перевірки](https://portal.lisk.com/airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/LiskHQ/status/1895512407654723803) · [Посилання з каталогу — потребує перевірки](https://x.com/LiskHQ/status/1896295019193237983)

### 70. Walrus Protocol

**Дата:** 2025-03-19 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized storage network built on the Sui blockchain, aiming to provide secure, efficient, and decentralized data storage solutions.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Walrus Protocol airdrop was based on the following requirements
- Sui Wallet Setup
- Install a Sui-compatible wallet (e.g., Sui Wallet or Phantom) and switch the network to the Sui Testnet.
- Obtaining Testnet Tokens
- Acquire testnet SUI tokens via the Sui Testnet faucet or through the Sui Discord channel.
- Staking $WAL Tokens
- Stake at least 1 $WAL token with an approved validator on the Walrus staking platform.
- Minting NFTs
- Mint a Flatland NFT on the Walrus website using your Sui Wallet.
- Community and Social Engagement
- Participate in Walrus-related campaigns on platforms like Galxe.
- Engage actively in the Walrus Discord.
- Follow Walrus on social channels to stay updated and participate in contests.
- Sui Ecosystem Interaction
- Engage with other Sui protocols, hold SUI domains, or interact with Sui dApps, as active participation in the ecosystem may influence eligibility.
- Testnet Participation

**Фактори:** real_product_usage, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution.
**Обсяг:** 500 million WAL tokens (10% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/walrus-protocol/) · [Посилання з каталогу — потребує перевірки](https://claim.walrus.xyz/airdrop/link-social) · [Посилання з каталогу — потребує перевірки](https://www.walrus.xyz/) · [Посилання з каталогу — потребує перевірки](https://www.walrus.xyz/blog/wal-mainnet-nft-airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/WalrusProtocol/status/1902729820754071740)

### 71. Gyroscope Protocol

**Дата:** 2025-03-19 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized protocol focused on providing a stable and resilient digital currency.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the GYFI airdrop was determined by the Gyroscope DAO through a series of Gyroscope Improvement Proposals (GIPs)
- SPIN holders
- As established in GIP-1, SPIN holders can convert their SPIN to GYFI at a rate of 1,066 SPIN per GYFI.
- Founding Member NFT holders
- According to GIP-2, Founding Member NFT holders are eligible to claim GYFI, with the amount dependent on the rarity of their NFT.
- Galxe participants
- GIP-2 also established that participants in a Gyroscope Galxe campaign are eligible to claim GYFI.
- In total, approximately 12,000 addresses are eligible for GYFI. Additional categories may be added in the future, with considerations for sybil risks.

**Фактори:** snapshot_state, points_quests, nft_or_asset_holding, anti_sybil_identity, claim_and_vesting.
**Обсяг:** Up to 15% of total GYFI supply (assuming all users choose GIP-1 Option 3). **Eligible:** Approximately 12,000 addresses. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/gyroscope-protocol/) · [Посилання з каталогу — потребує перевірки](https://docs.gyro.finance/governance/gyfi-tokenomics) · [Посилання з каталогу — потребує перевірки](https://docs.gyro.finance/governance/gyfi-tokenomics/eligibility) · [Посилання з каталогу — потребує перевірки](https://gyro.finance) · [Посилання з каталогу — потребує перевірки](https://x.com/GyroStable/status/1902065139031191958)

### 72. Bedrock

**Дата:** 2025-03-15 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Bedrock is the first multi-asset liquid restaking protocol, pioneering Bitcoin staking with uniBTC. It enables holders to earn rewards while maintaining liquidity, unlocking new yield opportunities in Bitcoin’s $1T market.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility is based on
- Bedrock Diamonds
- earned through various activities
- Stakers
- Users who hold
- uniTokens
- (e.g., uniBTC, uniETH, uniIOTX, brBTC).
- DeFi Participants
- Users who participated in
- DeFi protocols
- with
- Referrers
- Users who referred at least
- one friend
- to Bedrock.
- Fan NFT & Community Badge Holders

**Фактори:** early_participation, snapshot_state, capital_exposure, nft_or_asset_holding, community_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 5.5% of the total BR token supply. **Eligible:** 200,000+ addresses. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/bedrock/) · [Посилання з каталогу — потребує перевірки](https://docs.bedrockdao.com/governance/usdbr-airdrop/airdrop-season-1) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/0xF3c0C25090ae1458FC152947Aab57253cB8E0F0F/XqYtzwPbEEIzDThcuDIXxzj_52hBNc1m7f9iGy2rRgY) · [Посилання з каталогу — потребує перевірки](https://www.bedrock.technology/) · [Посилання з каталогу — потребує перевірки](https://x.com/Bedrock_DeFi/status/1901201572841017458)

### 73. Shardeum

**Дата:** 2025-03-14 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Shardeum is an EVM-based, linearly scalable Layer 1 blockchain platform that offers low gas fees while maintaining decentralization and security.
**Статуси:** source_checked_historical_product; issuer_reported_distribution.

**Умови/дії:**

- Eligibility for the Shardeum airdrop was based on the following requirements
- Phase 1: Early Contributors (Feb 22, 2022 – Jun 22, 2024)
- On-Chain Contributors
- Evaluated based on network interactions, transaction volume, and activity consistency.
- Validators
- Assessed on node uptime, participation across network versions, and contribution impact.
- Off-Chain Contributors
- Recognized for activities such as community building, content creation, and event organization.
- Phase 2: Incentivized Testnet Participants (Jun 26, 2024 – Mar 1, 2025)
- Assessed on task completion, activity consistency, and engagement across testnet stages.
- Evaluated based on node operation hours, task completion, and consistent participation.
- Detailed eligibility criteria and allocation per category are outlined in the official announcement.

**Фактори:** early_participation, real_product_usage, activity_volume, points_quests, testnet_participation, node_validator_work, community_contribution, anti_sybil_identity.
**Обсяг:** 5,516,575 SHM tokens (2.22% of initial SHM supply). **Eligible:** 63,494. **Claimants:** Not specified.
**Урок:** Зберігати «до» як верхню межу, розрізняти дату звіту 2026 та кампанії 2025; перевірку після активності робити окремим етапом.

**Прогалини:** Незалежний перерахунок переказів і фінальних одержувачів не виконано. Витрати учасників і поточну працездатність продукту окремо не перевірено. Фактичне відшкодування gas та індивідуальні платежі не перераховано; 1300 — shortlist, не число отримувачів.

**Джерела:** [Джерело 1](https://shardeum.org/blog/evm-testnet-shm-airdrop-verification/) · [Джерело 2](https://shardeum.org/blog/shardeum-monthly-marketing-report-decemeber-2025/) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/shardeum/) · [Посилання з каталогу — потребує перевірки](https://discord.gg/shardeum) · [Посилання з каталогу — потребує перевірки](https://docs.shardeum.org) · [Посилання з каталогу — потребує перевірки](https://shardeum.org) · [Посилання з каталогу — потребує перевірки](https://shardeum.org/) · [Посилання з каталогу — потребує перевірки](https://shardeum.org/blog/shardeum-shm-airdrop-eligibility-registration/) · [Посилання з каталогу — потребує перевірки](https://testnet.shardeum.org)

### 74. Pell Network

**Дата:** 2025-03-13 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Pell Network is an Omnichain Decentralized Validated Service (DVS) Network driven by BTC restaking, aiming to extend BTCFi into the cryptoeconomic security domain and fully unlock Bitcoin’s security potential.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility is based on the Epoch 1 snapshot taken on January 31, 2025, at 00:00 UTC. Two primary groups qualify for the airdrop
- 1. Pell Points Holders (5% of Total Supply - 105,000,000 PELL)
- Users who held Pell Points during Epoch 1.
- Categories
- Early Stakers
- Users who staked before the snapshot.
- Pell Event Participants
- Users engaged in Pell campaigns before January 31, 2025.
- Active Community Members
- Earned Pell Points via Twitter, Discord, Pell Mini App, or as active contributors/MVPs.
- Claim Deadline: March 27, 2025, 9:00 UTC.
- Special Cases
- Binance x Bitlayer x Pell Mining Gala Participants
- Can claim via Binance Web3 event page from March 13, 2025, 10:00 UTC.
- Pell x Binance New Year Red Packet Participants
- $PREPELL tokens will convert 1:1 into PELL.

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, claim_and_vesting.
**Обсяг:** 126,000,000 PELL (6% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/pell-network/) · [Посилання з каталогу — потребує перевірки](https://app.pell.network/claim) · [Посилання з каталогу — потребує перевірки](https://docs.pell.network/pell-tokenomics) · [Посилання з каталогу — потребує перевірки](https://pell.network/) · [Посилання з каталогу — потребує перевірки](https://pellrestaking.substack.com/p/pell-epoch-1-airdrop-detailed-overview) · [Посилання з каталогу — потребує перевірки](https://x.com/Pell_Network/status/1900108253738262572)

### 75. DefinitiveFi

**Дата:** 2025-03-13 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A multichain trading platform providing advanced order types across major chains with a noncustodial, gasless, and MEV-resistant experience.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Existing Definitive Users
- Includes S1 points holders, pre-points traders, and early yield users.
- Active Onchain Traders
- Addresses that traded over $100K cumulative volume from September 1, 2024, to February 28, 2025, on
- ANY
- of the following protocols
- Hyperliquid, Jupiter, Odos, 0x, Photon, Bananagun, Drift, CowSwap, and BullX.
- Example
- ✅ Eligible - If you traded over $100K cumulative volume on Jupiter from September 1 through February 28.
- ❌ Not Eligible - If you traded only $50K cumulative volume on Jupiter and $50K cumulative volume on Odos.
- TWAP Order Requirement
- Users must complete a Time-Weighted Average Price (TWAP) trade to confirm eligibility.
- Referral Bonus
- Referring eligible users before the claim date grants a 20% bonus on the referred users’ baseline airdrop.
- Last Chance Drawing
- Ineligible users can complete specific quests to enter a 200,000 $EDGE drawing, where 500 winners will be randomly selected.

**Фактори:** early_participation, snapshot_state, real_product_usage, activity_volume, points_quests, nft_or_asset_holding, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 200,000 $EDGE for Last Chance Drawing, full distribution amount not specified. **Eligible:** 124,000 addresses. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/definitivefi/) · [Посилання з каталогу — потребує перевірки](https://app.definitive.fi/claim) · [Посилання з каталогу — потребує перевірки](https://definitive.fi) · [Посилання з каталогу — потребує перевірки](https://discord.com/invite/definitive) · [Посилання з каталогу — потребує перевірки](https://docs.definitive.fi) · [Посилання з каталогу — потребує перевірки](https://docs.definitive.fi/platform/edge-token-airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/DefinitiveFi/status/1900212855527608473)

### 76. Peaq

**Дата:** 2025-03-11 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** peaq is a layer-1 blockchain enabling the Machine Economy, supporting decentralized physical infrastructure networks (DePINs) and real-world Web3 applications.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- “Get Real” Campaign Airdrop
- Wallet Connection
- Requires an Ethereum-compatible wallet (MetaMask, WalletConnect) connected to Peaq Network.
- Quest Completion
- Engage with real-world DePIN applications like
- Silencio
- (noise pollution tracking) and
- MapMetrics
- (navigation data).
- Earn
- XP (Experience Points)
- and
- NP (Network Points)
- to rank on the leaderboard.
- Referral Bonus
- 1% XP from referred users.

**Фактори:** snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, points_quests, nft_or_asset_holding, developer_contribution, referrals, ranking_or_tier.
**Обсяг:** 210 million PEAQ tokens (~$50M) across multiple seasons. **Eligible:** 15,000+ participants in “Get Real” Season 1. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/peaq/) · [Посилання з каталогу — потребує перевірки](https://app.hedgey.finance/claim/13a16567-db7b-4a91-8a4a-939faab8348a) · [Посилання з каталогу — потребує перевірки](https://app.hedgey.finance/claim/a04cde54-16d7-44f6-a220-b5cc758648fe) · [Посилання з каталогу — потребує перевірки](https://www.krest.network/blog/peaq-airdrop-for-krest-holders-how-to-double-your-rewards) · [Посилання з каталогу — потребує перевірки](https://www.peaq.network/) · [Посилання з каталогу — потребує перевірки](https://www.peaq.network/blog/the-peaq-token-launch-all-you-need-to-know) · [Посилання з каталогу — потребує перевірки](https://x.com/peaq/status/1899166100119867867)

### 77. Bubblemaps

**Дата:** 2025-03-11 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Bubblemaps is the first supply auditing tool for DeFi tokens and NFTs, utilizing unique and colorful bubbles to simplify on-chain data analysis.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Bubblemaps airdrop was based on the following requirements
- Bubblemaps V2 Beta Waitlist
- Users must have joined the Bubblemaps V2 Beta Waitlist via invite or direct waitlisting.
- Platform Usage
- Actively use the Bubblemaps V2 platform.
- Invite active users to the platform.
- Earn points through usage and referrals; higher scores increase the chances of receiving rewards.
- Leaderboard & Lottery Selection
- Users were selected based on their leaderboard rank or through the lottery system.
- Top 10 users: Highest allocation.
- Top 100 users: Medium allocation.
- Top 5000 users: 900 winners selected via lottery and sybil detection.

**Фактори:** points_quests, nft_or_asset_holding, referrals, anti_sybil_identity, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** Approximately 50,000 users have participated in the points campaign so far.. **Claimants:** невідомо.
**Урок:** Зберігати season, формулу points, mandatory/bonus дії та версію правил. Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння. Вважати referral додатковим множником, якщо правила не визначають його обов’язковим.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/bubblemaps/) · [Посилання з каталогу — потребує перевірки](https://blog.bubblemaps.io/its-official-the-incoming-token/) · [Посилання з каталогу — потребує перевірки](https://bubblemaps.io) · [Посилання з каталогу — потребує перевірки](https://docs.google.com/spreadsheets/d/1E3sUl0VMn_icqf40xor0zUNOyXk2I6lGtcr6hLheeP8/) · [Посилання з каталогу — потребує перевірки](https://wiki.bubblemaps.io/bmt/airdrop/v2-users) · [Посилання з каталогу — потребує перевірки](https://x.com/bubblemaps/status/1899384817734803470)

### 78. Sirath

**Дата:** 2025-03-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Sirath Network is a RollApp built on the Dymension Ecosystem, utilizing rollup technology to aggregate transactions and publish proofs to the main network, reducing transaction costs and increasing speed.
**Статуси:** reported_alive_by_secondary_directory; claim_start_reported_by_secondary_source.

**Умови/дії:**

- DYM Stakers
- Individuals who stake DYM tokens, likely on the Dymension mainnet or associated platforms, are positioned to qualify. Staking typically involves locking up tokens to support network security and operations, and airdrops often reward such participants to encourage long-term commitment.
- Testnet Contributors
- Users who have actively participated in the Dymension testnet—potentially including testing Sirath Network functionalities as a RollApp—are also eligible. This could involve tasks like running nodes, submitting transactions, or engaging with testnet features, though exact tasks aren’t specified.

**Фактори:** real_product_usage, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, community_contribution.
**Обсяг:** 20% of total token supply (Exact total supply not specified). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/sirath/) · [Посилання з каталогу — потребує перевірки](https://docs.sirath.network/learn/tokenomics/vesting#community-incentive) · [Посилання з каталогу — потребує перевірки](https://sirath.network/) · [Посилання з каталогу — потребує перевірки](https://sirath.network/articles/sirath-genesis) · [Посилання з каталогу — потребує перевірки](https://x.com/SirathNetwork/status/1898773309380333925)

### 79. RedStone Oracles

**Дата:** 2025-03-06 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A modular blockchain oracle providing secure and scalable data feeds
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- The initial Miner Airdrop allocated 5% of total RED supply, claimable via
- official claim website
- An additional 2% from “Ecosystem & Data Providers” is allocated for community members initially excluded, based on extended eligibility and proof of participation. Claiming starts on March 6, 2025, via
- bonus claim website
- A further 4.5% from “Community & Genesis” will be distributed 6 months after TGE (September 6, 2025). Eligible projects must utilize RedStone price feeds and will distribute tokens to users of pools secured by RedStone price feeds.

**Фактори:** early_participation, duration_consistency, activity_diversity, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 5% of total RED supply (initial), additional 2% allocated, further 4.5% in 6 months. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/redstone-oracles/) · [Посилання з каталогу — потребує перевірки](http://bonus.redstone.finance) · [Посилання з каталогу — потребує перевірки](http://claim.redstone.finance) · [Посилання з каталогу — потребує перевірки](https://blog.redstone.finance/2025/02/12/introducing-red-tokenomics/) · [Посилання з каталогу — потребує перевірки](https://defillama.com/oracles/RedStone) · [Посилання з каталогу — потребує перевірки](https://redstone.finance) · [Посилання з каталогу — потребує перевірки](https://x.com/redstone_defi/status/1897647415374872733)

### 80. Mint Blockchain

**Дата:** 2025-03-06 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Опис продукту у джерелі не структуровано.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- 10% of the total supply (120,000,000 MINT) is claimable by eligible users.
- The first 5,000 MintID holders who stake their MintID will receive a “Minty NFT” airdrop.
- Users holding an activated GreenID with ME injected are eligible to claim MINT.
- Users accumulating MP and holding a Mint Expedition NFT are eligible to claim MINT.
- Additional eligibility criteria may apply based on specific campaigns (e.g., Mint Bigbang, Mint x GoPlus Christmas Airdrop, Mint x OKX Pioneer Explorer NFT Campaign).

**Фактори:** early_participation, snapshot_state, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, claim_and_vesting.
**Обсяг:** 120,000,000 MINT tokens. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/mint-blockchain/) · [Посилання з каталогу — потребує перевірки](https://www.mintchain.io) · [Посилання з каталогу — потребує перевірки](https://www.mintchain.io/airdrop/claim) · [Посилання з каталогу — потребує перевірки](https://x.com/Mint_Blockchain/status/1897890105156943945)

### 81. Elixir

**Дата:** 2025-03-06 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Elixir is the most widely adopted network by RWAs, bringing funds from institutions like
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Apothecary potion holders (7% of the total ELX airdrop allocation)
- Community contributors (0.4%) including Cult OGs, private cult members, ritual winners, Discord role holders, POAP holders, and top XP earners
- Elixir Electric Bazaar NFT holders (0.1%)
- Early testnet validators connected to their Apothecary (0.25%)
- DeFi stablecoin power users (0.25%)
- TVL snapshot taken on February 28, 2024 – Users who had funds in the protocol on this date received a 30% boost
- Airdrop recipients were automatically delegated to the ‘ElixirFoundation’ validator
- Users who remained delegated throughout the three-month decentralization phase will have doubled their initial ELX airdrop allocation
- Users had to connect their EVM wallet to their SUI wallet before March 1, 2024, with a final grace period until March 31, 2024

**Фактори:** early_participation, snapshot_state, capital_exposure, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, ranking_or_tier.
**Обсяг:** 8% of total ELX supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/elixir/) · [Посилання з каталогу — потребує перевірки](https://claim.elixir.xyz) · [Посилання з каталогу — потребує перевірки](https://discord.com/invite/elixirnetwork) · [Посилання з каталогу — потребує перевірки](https://elixir.finance) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/0x25832C2fC7B7380E5B74Ea280ea2D2C98a0d5644/XXZuIQ1Awjzn2KkNGENrJcl1zvsj2RVUWKunVHFq2rA) · [Посилання з каталогу — потребує перевірки](https://x.com/elixir/status/1897403017080803427)

### 82. Unlock Protocol

**Дата:** 2025-03-03 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized protocol for memberships, subscriptions, and ticketing onchain, enabling creators and developers to monetize access to their communities.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Community members were eligible based on their engagement with Unlock Protocol throughout 2023 and 2024. Activities that contributed to eligibility included
- Integrating Unlock Protocol
- into third-party platforms (e.g., Hats Protocol)
- Creating paid memberships or subscriptions
- using Unlock Protocol
- Hosting paid events
- with onchain ticketing via Unlock
- Participating in governance votes
- or delegating voting power
- Engaging in discussions
- within the Unlock Protocol Discord
- Holding a paid onchain membership
- or subscription
- Attending a paid event
- utilizing onchain tickets
- Demonstrating extensive usage

**Фактори:** points_quests, nft_or_asset_holding, community_contribution, developer_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 7,000,000 $UP tokens. **Eligible:** Over 10,000 members. **Claimants:** невідомо.
**Урок:** Зберігати season, формулу points, mandatory/bonus дії та версію правил. Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння. Оцінювати якість і підтверджуваність внеску; масовий spam підвищує Sybil-ризик.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/unlock-protocol/) · [Посилання з каталогу — потребує перевірки](https://airdrops.unlock-protocol.com) · [Посилання з каталогу — потребує перевірки](https://app.charmverse.io/unlock-dao/) · [Посилання з каталогу — потребує перевірки](https://discord.unlock-protocol.com) · [Посилання з каталогу — потребує перевірки](https://paragraph.xyz/@unlockprotocol/unlock-protocol-airdrop-7m-up-tokens) · [Посилання з каталогу — потребує перевірки](https://unlock-protocol.com) · [Посилання з каталогу — потребує перевірки](https://warpcast.com/unlock-protocol)

### 83. Henlo

**Дата:** 2025-03-03 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Henlo is a community-driven memecoin project built in the Berachain ecosystem, focusing on culture over utility.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- The airdrop is divided into two categories
- $HENLO Eligibility (21.4%)
- Users holding or participating in
- Henlo THJ
- Honey Comb
- Mibera Superset
- Infinity Gate
- Honey Jars (all generations)
- Henlo Beras
- Bong Bears and all rebases
- Henlo Chaos
- Henlo Dune Dashboard Mints
- Jani Friendtech Keys
- Jani’s Closet Mints
- Henlo Article Mints
- Paragraph Subscribers

**Фактори:** snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, referrals, ranking_or_tier.
**Обсяг:** 21.4% of total supply for $HENLO, 9.6% for $oHENLO. **Eligible:** 50,203 wallets. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/henlo/) · [Посилання з каталогу — потребує перевірки](https://app.ramen.finance/henlo) · [Посилання з каталогу — потребує перевірки](https://checker.henlo.com/) · [Посилання з каталогу — потребує перевірки](https://paragraph.xyz/@henlo/henlo-tokenomics) · [Посилання з каталогу — потребує перевірки](https://www.henlo.com/) · [Посилання з каталогу — потребує перевірки](https://x.com/henlo/status/1896388928133038168)

### 84. Rivalz

**Дата:** 2025-02-21 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Rivalz is building the World Abstraction Layer for AI and Agents, providing an AI-focused infrastructure that enables scalable and self-sovereign AI economies.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Testnet Users
- Must have participated in the Rivalz Testnet and met minimum
- point requirements
- in each epoch
- Epoch 1
- Minimum 2,000 rClient points, 500 social engagement points
- Epoch 2
- Minimum 1,000 rClient points, 500 social engagement points
- Epoch 3
- Minimum 1,000 rClient points, 5,000 social engagement points
- Referral points were counted as an amplifier.
- The
- top 5,000 users
- on the Rivalz Galxe leaderboard are also eligible.
- Strategic Partner Communities
- Chainlink, Aethir, Pixelmon, Puffer Finance

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 350,000,000 RIZ (7% of total supply). **Eligible:** 1,200,000 users. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/rivalz/) · [Посилання з каталогу — потребує перевірки](https://blog.rivalz.ai) · [Посилання з каталогу — потребує перевірки](https://blog.rivalz.ai/rivalz-testnet-airdrop-celebrating-the-community/) · [Посилання з каталогу — потребує перевірки](https://docs.google.com/forms/d/e/1FAIpQLSe52MPGWjPwpc12XoZqgz9T4aIxktOIdOaLzatP1oYmmgCGaQ/viewform) · [Посилання з каталогу — потребує перевірки](https://x.com/Rivalz_AI/status/1892938362102686062)

### 85. Quai

**Дата:** 2025-02-21 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A modular blockchain network focused on scalability, decentralization, and rewarding early contributors.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Quai airdrop was based on the following requirements
- General Requirements
- Open to participants from all countries except those on the OFAC sanctions list
- KYC is required via Fractal.id with a $5 ETH fee (non-refundable if from a restricted country)
- Claiming requires linking a Discord account and registering a Quai-compatible mainnet wallet (Pelagus Wallet)
- Participation Programs
- Stone Age, Iron Age, Bronze Age, Golden Age Testnets
- Quai Ambassador Rewards
- Social Media Rewards, Kaito Leaderboard, Galxe Campaigns
- Builder Grants (subject to a vesting schedule)

**Фактори:** early_participation, points_quests, testnet_participation, community_contribution, developer_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 38.7M QUAI (Testnet Rewards) + 26M QUAI (Social Media Rewards) + 1M QUAI (Builder Grants). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Вести журнал транзакцій, feedback і знайдених помилок; тестнет сам по собі не гарантує токени.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/quai/) · [Посилання з каталогу — потребує перевірки](https://claims.qu.ai) · [Посилання з каталогу — потребує перевірки](https://pelaguswallet.io) · [Посилання з каталогу — потребує перевірки](https://qu.ai) · [Посилання з каталогу — потребує перевірки](https://qu.ai/blog/announcing-the-quai-network-claims-page/)

### 86. Pi Network

**Дата:** 2025-02-20 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized cryptocurrency network focused on mobile mining and peer-to-peer transactions.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- To qualify for the Pi Network airdrop, users must meet the following criteria
- Mining Participation
- Users must have actively mined PI tokens through the Pi Network mobile app before the airdrop.
- KYC Verification
- Completion of Know Your Customer (KYC) verification was required before
- February 28, 2025
- to secure eligibility.
- Mainnet Migration
- Users had to migrate their PI balance to the Mainnet by
- Automatic Distribution
- Eligible users receive their PI directly in their Pi Wallet without needing to manually claim tokens.

**Фактори:** snapshot_state, real_product_usage, anti_sybil_identity, claim_and_vesting.
**Обсяг:** $12.6 billion worth of PI tokens. **Eligible:** Over 19 million KYC-verified Pioneers. **Claimants:** 10.14 million Mainnet migrations recorded.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Не автоматизувати дублікати особистостей; перевіряти правила адрес, кластерів, KYC і географії.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/pi-network/) · [Посилання з каталогу — потребує перевірки](https://minepi.com/) · [Посилання з каталогу — потребує перевірки](https://minepi.com/blog/open-network-launch-date/) · [Посилання з каталогу — потребує перевірки](https://x.com/PiCoreTeam) · [Посилання з каталогу — потребує перевірки](https://x.com/PiCoreTeam/status/1891257712085733567)

### 87. Kaito

**Дата:** 2025-02-20 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized AI-powered ecosystem designed to facilitate knowledge discovery, content creation, and governance within the InfoFi economy.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Kaito airdrop was based on the following requirements
- Engagement Metrics
- Yaps
- Proof-of-work, proof-of-engagement, and proof-of-insight
- Kaito Value Alignment
- Public discussions about Kaito, analyzed and quantified
- Kaito Long-term Loyalty
- Engagement before the launch of Kaito Yaps over the past three years
- Platform Participation
- Ecosystem Participation
- Active involvement in Kaito Pro and Kaito Yaps
- Governance Participation
- Contributions to Yapper Launchpad voting
- Regional and Emerging Yappers
- Recognizing diverse geographic participation and rising creators
- Onchain Reputation

**Фактори:** early_participation, activity_diversity, nft_or_asset_holding, community_contribution, claim_and_vesting.
**Обсяг:** 19.5% of total supply allocated for community airdrops and incentives. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kaito/) · [Посилання з каталогу — потребує перевірки](https://docs.kaito.ai/introducing-usdkaito/tokenomics) · [Посилання з каталогу — потребує перевірки](https://kaito.ai)

### 88. Superfluid

**Дата:** 2025-02-19 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Superfluid is a protocol enabling real-time financial transactions, allowing money to be streamed continuously over time.
**Статуси:** reported_alive_by_secondary_directory; claim_start_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Superfluid airdrop was based on the following requirements
- Ecosystem Campaign Participation
- Users must participate in Superfluid ecosystem campaigns.
- SUP tokens are earned through engagement with partner applications.
- Rewards are streamed continuously over time rather than a one-time claim.
- Recipients can choose a time preference for tokens, with longer commitments receiving higher bonuses.
- Example Campaign Types
- Social Subscriptions (e.g., AlfaFrens)
- DCA & Yield (e.g., SuperBoring XYZ)
- Streaming UBI (e.g., GoodDollar)
- Streaming Donations (e.g., Giveth, OctantApp, Flows.wtf)
- Streaming Quadratic Funding (e.g., Flowstate Coop)
- Community Activations & Superfluid Payments
- Additional campaigns to be announced in future seasons

**Фактори:** duration_consistency, real_product_usage, activity_diversity, points_quests, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 1 billion SUP minted at genesis. **Eligible:** 315,000+ wallets (active users). **Claimants:** невідомо.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/superfluid/) · [Посилання з каталогу — потребує перевірки](https://claim.superfluid.org) · [Посилання з каталогу — потребує перевірки](https://superfluid.org) · [Посилання з каталогу — потребує перевірки](https://superfluid.org/post/introducing-sup-the-superfluid-token) · [Посилання з каталогу — потребує перевірки](https://x.com/Superfluid_HQ/status/1892236026925773206)

### 89. Avalon Labs

**Дата:** 2025-02-15 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Avalon Labs is a blockchain-based platform focused on decentralized finance (DeFi) solutions.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Avalon Labs airdrop was based on the following requirements
- Minimum Reward
- Every eligible user who interacted with Avalon Labs contracts and completed airdrop registration is guaranteed at least 5 AVL.
- Avalonians (99.5% of total users)
- Immediate 100% unlock at Token Generation Event (TGE).
- AVL Whales (0.5% of users)
- Subject to linear vesting.
- IDO Whitelist Holders
- Fixed reward of 200 AVL.
- Calculation of AVL Airdrop Allocation
- Users with an AVL allocation of less than 5: no adjustments.
- Allocations between 5 and 50,000 AVL: adjusted amount calculated as (50,000 ^ 0.3 * AVL) ^ 0.77.
- Allocations exceeding 50,000 AVL: adjusted amount follows the formula: 50,000 + (AVL — 50,000) ^ 0.9.
- Sybil Attack Prevention
- For People Launchpool Users, Marketing Campaigns Participants, and CEX Campaigns Participants
- Addresses with batch transfers or cross-address transactions are limited to one counted address.

**Фактори:** snapshot_state, real_product_usage, points_quests, nft_or_asset_holding, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 20% of AVL’s total supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/avalon-labs/) · [Посилання з каталогу — потребує перевірки](https://forms.gle/S7eohBd2Myrxjv2j8) · [Посилання з каталогу — потребує перевірки](https://medium.com/@avalonlabs/avl-tge-claim-your-airdrop-now-6b09957af071) · [Посилання з каталогу — потребує перевірки](https://www.avalonfinance.xyz/) · [Посилання з каталогу — потребує перевірки](https://x.com/avalonfinance_/status/1889116096248308097)

### 90. Berachain

**Дата:** 2025-02-09 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Token Data
**Статуси:** source_checked_historical_product; allocation_or_rules_only.

**Умови/дії:**

- The following categories of users are eligible for the airdrop
- Testnet Users (Artio and bArtio)
- Users who interacted with Berachain’s testnets, including minting $HONEY, claiming fees, posting incentives, converting $BGT to $BERA, delegating $BGT, etc. Small boosts were given to Binance Web3Wallet users.
- Total Allocation
- 8,250,000 BERA (1.65%)
- Request for Brobosal (RFB) Recipients
- Request for Application (RFA)
- Teams that deployed dApps on Berachain testnets. 70% of allocation must go toward mainnet initiatives, up to 15% for protocol treasury, and 10-15% to testnet users.
- Request for Community (RFC)
- Contributors to the Berachain community (content creators, regional hubs, social networks, etc.).
- 11,730,000 BERA (2.35%)
- Boyco Depositors
- Users who deposited capital in the Boyco launch program. Rewards are based on market choice, asset type, and deposit duration (30/90 days).
- 10,000,000 BERA (2%)
- Social Airdrop
- Users who posted constructive content about Berachain on X or engaged in the Berachain/Bong Bears Discord communities.

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, developer_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 15.75% of total BERA supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Не переносити обов’язковий капітал Boyco на безкапітальну testnet-когорту; частки екосистеми не створюють окремі проєкти.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано.

**Джерела:** [Джерело 1](https://blog.berachain.com/blog/berachain-airdrop-overview) · [Джерело 2](https://airdrop.berachain.com/) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/bera-chain/) · [Посилання з каталогу — потребує перевірки](https://berachain.com/) · [Посилання з каталогу — потребує перевірки](https://checker.berachain.com/)

### 91. Venice AI

**Дата:** 2025-01-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Venice is a private, uncensored AI platform providing generative text, image, and code inference without centralized surveillance. It offers API access and staking-based AI inference.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Active Venice platform users from
- October 31, 2024
- onwards.
- Must have
- at least 25 points
- December 31, 2024 (23:59 UTC)
- AI community protocol members on Base blockchain, including
- VIRTUALS, AERO, DEGEN, AIXBT, GAME, LUNA, VADER, CLANKER, MOR.
- Some allocation for @NousResearch when their Psyche token launches.
- Roughly
- 200 registered Coinbase Agentkit Developers

**Фактори:** capital_exposure, points_quests, community_contribution, developer_contribution.
**Обсяг:** 50 million VVV (50% of total supply). **Eligible:** Over 100,000 Venice users + AI community protocol accounts. **Claimants:** невідомо.
**Урок:** Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Оцінювати якість і підтверджуваність внеску; масовий spam підвищує Sybil-ризик.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/venice-ai/) · [Посилання з каталогу — потребує перевірки](https://venice.ai) · [Посилання з каталогу — потребує перевірки](https://venice.ai/claim)

### 92. Solv Protocol

**Дата:** 2025-01-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Leading Bitcoin staking platform facilitating on-chain BTC reserves and DeFi integration.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Users eligible through Solv Points System Season 1 (7.25% of supply).
- Early supporters, including Vesting Voucher holders, KYC-ed users, and Seahorse Points holders (0.25% of supply).
- OKX Cryptopedia Campaign participants (0.15% of supply).
- Additional airdrops via Binance Web3 Wallet and OKX Bitcoin Mainnet Campaign.
- Top 1% of addresses have a 3-month lock-up with vesting conditions.
- Vesting conditions require maintaining average SOLV holdings from Season 1 in Season 2.

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, points_quests, nft_or_asset_holding, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 7.65% of total SOLV supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/solv-protocol/) · [Посилання з каталогу — потребує перевірки](https://solv.finance) · [Посилання з каталогу — потребує перевірки](https://solv.foundation/claim) · [Посилання з каталогу — потребує перевірки](https://solvprotocol.medium.com/solv-token-launch-a-step-towards-the-future-of-bitcoin-finance-5fb64a69220b) · [Посилання з каталогу — потребує перевірки](https://x.com/SolvProtocol/status/1879816281345663474)

### 93. SoSoValue

**Дата:** 2025-01-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A cryptocurrency data aggregator providing real-time data, market trends, and investment research.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Bybit Launchpool (4 million $SOSO)
- Users needed to stake assets (e.g., $SOSO or other supported tokens) in the Bybit Launchpool between January 25 and February 25, 2025, for an 11-day period.
- Eligibility
- Open to Bybit users who participated in the staking event. No EXP points were required; rewards were based on staking amounts.
- Proof of Work (PoW) - EXP Earning (15 million $SOSO)
- Users earned EXP points through platform interactions before a snapshot taken on January 17, 2025. A wallet connection was mandatory by January 22, 2025, 8:00 AM UTC.
- Tasks Included
- Signing up (10,000 EXP bonus with an invitation link)
- Daily check-ins
- Completing social media tasks (e.g., connecting Twitter/X)
- Downloading apps (225,000 EXP per desktop/mobile app)
- Inviting friends
- 200,000 users were eligible, with rewards distributed at the Token Generation Event (TGE). The maximum reward per user was valued at approximately $120,000 worth of $SOSO.
- Proof of Stake (PoS) Rewards (30 million $SOSO)
- Users participated in staking activities on the SoSoValue platform during the first season (January 25 to February 25, 2025).
- Open to users who staked $SOSO tokens on the platform. Rewards were based on the amount and duration of staking.

**Фактори:** snapshot_state, duration_consistency, capital_exposure, points_quests, community_contribution, ranking_or_tier.
**Обсяг:** 49 million SOSO tokens. **Eligible:** 200,000 users. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/sosovalue/) · [Посилання з каталогу — потребує перевірки](https://sosovalue.com) · [Посилання з каталогу — потребує перевірки](https://x.com/SoSoValueCrypto/status/1882719938043150485)

### 94. Antcore

**Дата:** 2025-01-24 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A multichain DeFi ecosystem built on the Aptos blockchain, utilizing the Move programming language to deliver robust and innovative DeFi solutions, focusing on liquidity provision, governance, and community engagement.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Exact airdrop criteria were not explicitly detailed in a single official list across all sources, the following points are inferred from announcements, posts on X, and related web content.
- To qualify for the Antcore Genesis Drop, wallet addresses must have contributed liquidity to supported decentralized protocols operating on the Aptos and Sui blockchains. These protocols include
- Cetus
- Aftermath
- Turbos
- FlowX
- Kriya
- Bluefin
- Users were directed to verify their wallet addresses through the official Antcore eligibility checker available at
- https://genesis.antcore.finance
- . Registration for the genesis drop was open until January 24, 2025, with 26,493 registrations recorded out of the total eligible pool of 889,678 addresses as of that date.

**Фактори:** early_participation, capital_exposure, activity_diversity, points_quests, community_contribution.
**Обсяг:** невідомо. **Eligible:** 889,678 wallet addresses. **Claimants:** 26,493 addresses registered as of January 24, 2025.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/antcore/) · [Посилання з каталогу — потребує перевірки](https://antcore.finance) · [Посилання з каталогу — потребує перевірки](https://genesis.antcore.finance) · [Посилання з каталогу — потребує перевірки](https://portal.antcore.finance) · [Посилання з каталогу — потребує перевірки](https://x.com/antcorefinance/status/1878069890008912020)

### 95. CreatorBid

**Дата:** 2025-01-23 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized platform that enables users to earn and engage with creators through CreatorPoints and token-based memberships.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- BinanceWallet Campaign
- Users who completed required tasks and quests in the @BinanceWallet campaign are eligible to claim from the
- 8,000,000 BID
- allocation (0.8% of total supply).
- CreatorPoints Campaign
- Users who accumulated CreatorPoints by locking agent tokens on memberships are eligible for a share of the
- 42,000,000 BID
- allocation (4.2% of total supply).
- Daily CreatorPoints distribution will
- increase exponentially
- until the campaign ends.
- Tokens will be
- 100% unlocked
- upon claiming after the campaign ends.

**Фактори:** capital_exposure, points_quests, claim_and_vesting.
**Обсяг:** 50,000,000 BID (5% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Стежити за початком/кінцем claim, vesting, unlock і поверненням невитребуваних токенів.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/creator-bid/) · [Посилання з каталогу — потребує перевірки](https://creator.bid/) · [Посилання з каталогу — потребує перевірки](https://x.com/CreatorBid/status/1882374039940792511)

### 96. Anime Azuki

**Дата:** 2025-01-23 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** ANIME coin is the gas token for Animechain, an L3 blockchain using Arbitrum Orbit to enable gasless transactions. Backed by Azuki
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Anime Azuki airdrop was based on the following requirements
- Core Criteria
- Azuki, Elementals, and Beanz NFTs
- Emblems Allocation
- Based on NFT “Collector Score,” viewable on
- azuki.com/gallery
- Multi-token Emblems
- Bonus points for holding multiple NFT types under defined emblems
- Gacha Grab & Time Held Allocation
- Bonuses awarded for gacha holdings and NFT holding duration
- Azuki ERC-1155s
- Certain ERC-1155 NFTs (e.g., Ambush x Azuki, Bobu) are assigned allocations via the primary wallet on Azuki Collector’s Profile
- Twin Tigers Jacket NFTs & “Chiru” Emblem
- Allocation distributed among all Azuki, Beanz, and Elemental NFTs
- Gacha Grab Bonus Quests
- Allocated to the primary wallet on Azuki Collector’s Profile

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** Eligible User information not available. **Claimants:** Number of Claimants information not available.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/anime-azuki/) · [Посилання з каталогу — потребує перевірки](https://azuki.com/gallery) · [Посилання з каталогу — потребує перевірки](https://dune.com/entropy_advisors/anime-airdrop-analysis) · [Посилання з каталогу — потребує перевірки](https://www.anime.xyz/) · [Посилання з каталогу — потребує перевірки](https://www.anime.xyz/faq#token-allocation-determination)

### 97. Not Pixel

**Дата:** 2025-01-22 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A pixel-based gaming ecosystem that integrates cryptocurrency rewards, player achievements, and NFT utilities.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Minimum Balance Requirement
- Users must have at least
- 100,000 PX points
- in their Not Pixel account. Any balance below this threshold was burned and is ineligible.
- Wallet Requirement
- Users must have connected a
- TON (The Open Network) wallet
- , such as
- TonKeeper
- , to their Not Pixel account.
- Time-Limited Check-In
- Users needed to complete a
- specific check-in task on December 16, 2024
- to confirm eligibility.
- Mining Period Ended
- PX point accumulation

**Фактори:** snapshot_state, activity_diversity, points_quests, nft_or_asset_holding, ranking_or_tier.
**Обсяг:** 200 billion PX tokens (80% of total supply) allocated to miners and the community. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/not-pixel/) · [Посилання з каталогу — потребує перевірки](https://telegra.ph/Not-Pixel-FAQs-01-07) · [Посилання з каталогу — потребує перевірки](https://x.com/notpixelx/status/1876711462611091511)

### 98. Timeswap

**Дата:** 2025-01-21 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized, oracle-less lending and borrowing protocol enabling permissionless money markets for any ERC-20 tokens.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Timeswap airdrop was based on the following requirements
- Premine (3.26% of total supply)
- Incentivized lenders, borrowers, and liquidity providers (LPs) from October 2023 to January 2025. Final snapshot taken on January 12, 2024.
- Rewards are non-transferrable TIME tokens, convertible 1:1 into liquid TIME at Token Generation Event (TGE).
- Distribution follows a linear decay model, favoring early contributors.
- Retroactive Airdrop (5.26% of total supply)
- Rewards for Timeswap V1 & V2 users based on holding duration, transaction volume, unique pools interacted with, and total transactions.
- V1 Users: Minimum $300 in total volume.
- V2 Users: Minimum $100 in total volume.
- Distribution utilizes a tiered system with a linear decay model, rewarding long-term, high-value contributors.
- Community Drop (0.96% of total supply)
- Rewards participants of past initiatives, including Timeswap NFT holders, Galxe, Zealy, QuestN campaigns, partners, ambassadors, and gamified testnet users.
- Hyperliquid Drop (0.56% of total supply)
- Recognizes contributions from the Hyperliquid ecosystem
- 0.50% for users staking HYPE with HypurrCo X Nansen Validator (snapshot taken on January 15, 2025).
- 0.06% for contributors supporting Timeswap deployment, such as developers @Shuri2060 and @Syavel, each allocated 500,000 TIME tokens.

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, developer_contribution, ranking_or_tier.
**Обсяг:** 10.03% of total supply (1,750,000,000 TIME), equating to 175,525,000 TIME tokens. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/timeswap/) · [Посилання з каталогу — потребує перевірки](https://linity.com/opportunities/timeswap) · [Посилання з каталогу — потребує перевірки](https://timeswap.io/) · [Посилання з каталогу — потребує перевірки](https://timeswap.medium.com/time-tokenomics-4e906fefe942)

### 99. Obol Collective

**Дата:** 2025-01-21 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A community dedicated to scaling Ethereum by enhancing the security, resiliency, and decentralization of the consensus layer through the development and deployment of distributed validators.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Members who have contributed to the development and support of the Obol ecosystem
- Individuals who have participated in staking and earned Obol Contributions
- Independent stakers and operators within the Rocketpool network
- Note: Tokens are locked (non-transferable NFT) until the completion of the first retroactive funding round, subject to a governance vote.
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha Airdrop
- Users with ≥ 153 Alpha Points received 165 OBOL tokens
- Users with 116-152 Alpha Points and UIDs ending in 6 received 165 OBOL tokens
- Distribution: Within 20 minutes after Alpha trade opens
- Trading opens: May 7, 2025, 10:00 AM UTC
- Futures trading opens: May 7, 2025, 10:30 AM UTC
- Additional Notes
- Governance Participation
- Recipients are encouraged to delegate their tokens or become delegates themselves to actively participate in the governance of the Obol Collective

**Фактори:** activity_volume, capital_exposure, activity_diversity, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, developer_contribution.
**Обсяг:** 7.5% of the total OBOL token supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/obol-collective/) · [Посилання з каталогу — потребує перевірки](https://blog.obol.org/airdrop/) · [Посилання з каталогу — потребує перевірки](https://claim.obol.org) · [Посилання з каталогу — потребує перевірки](https://obol.org) · [Посилання з каталогу — потребує перевірки](https://x.com/Obol_Collective/status/1920070181902225409) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1920047370839986444)

### 100. Orbiter

**Дата:** 2025-01-20 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Orbiter Finance is a ZK-tech-based interoperability blockchain infrastructure focused on security, seamless cross-chain interactions, and liquidity efficiency. It features a universal cross-chain protocol and Omni Account Abstraction to redefine the Web3 experience.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Users must have interacted with the Orbiter protocol (bridge/ecosystem) for at least 2 months since December 2021
- Users must have earned at least 40 OPoints through cross-chain transactions
- The maximum OPoints counted towards the airdrop is 5,000
- Additional airdrop eligibility is granted to
- Discord moderators
- Holders of Ace NFT and Expert NFT
- Users who attended specific offline events hosted by Orbiter Finance
- Anti-Sybil protections are in place, including Sybil detection methods from projects like Arbitrum
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha Airdrop
- Users with ≥ 200 Alpha Points eligible for 8,000 OBT tokens
- Claiming requires 15 Alpha Points
- Claim window: 24 hours from May 24, 2025, 8:00 UTC
- Trading competition with $640K prize pool announced

**Фактори:** snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 22% of total supply (2.2 billion OBT). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/orbiter/) · [Посилання з каталогу — потребує перевірки](https://orbiter-finance.medium.com/obtokenomics-and-airdrop-eligibility-guide-3549dd00807a) · [Посилання з каталогу — потребує перевірки](https://orbiter.finance) · [Посилання з каталогу — потребує перевірки](https://orbiter.finance/en/airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/Orbiter_Finance/status/1880195622286028893) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1926186427546566839)

### 101. Nodepay

**Дата:** 2025-01-17 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Nodepay is a decentralized AI infrastructure network that rewards contributors and secures the ecosystem through Nodecoin ($NC), supporting innovations in user-owned AI. Users earn rewards by sharing unused internet bandwidth, testing products, and contributing to the network.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participation in Nodepay network as an early adopter or active contributor
- Activities such as contributing bandwidth, proof of humanity, testing Nodepay products, or accumulating Node Points
- Each season has its own eligibility criteria
- Additional Airdrop Opportunities
- Tiered allocations within each season based on engagement level or contributions
- More active participants receive higher rewards
- Bonus allocation in December (S2)
- Claim Process
- Claiming details to be announced via official Nodepay channels
- Users must follow official updates for instructions
- Only trust official Nodepay channels for claiming
- Special Conditions
- Beware of scams: Nodepay team will never request private keys or direct token transfers to unknown addresses
- Airdrop One is part of the 42% of tokens allocated for community incentives
- 265,000,000 tokens remain for future rewards

**Фактори:** early_participation, duration_consistency, activity_diversity, points_quests, node_validator_work, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 115,000,000 NC (11.5% of total supply). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/nodepay/) · [Посилання з каталогу — потребує перевірки](https://claim.nodefoundation.ai/) · [Посилання з каталогу — потребує перевірки](https://docs.nodepay.ai/nodepay-introduction/nodecoin/nodepay-airdrop-one) · [Посилання з каталогу — потребує перевірки](https://nodepay.ai/) · [Посилання з каталогу — потребує перевірки](https://x.com/nodepay_ai/status/1880178328466067968)

### 102. Jupiter

**Дата:** 2025-01-15 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** A decentralized autonomous organization focused on enhancing the Jupiter ecosystem through community engagement and innovative trading solutions.
**Статуси:** source_checked_historical_product; issuer_reported_claims.

**Умови/дії:**

- The eligibility period for the JUPUARY 2025 airdrop spans from
- 2 Nov 2023 - 1 Nov 2024
- , with criteria focusing on
- Active Participation
- Engagement on platforms such as Twitter, Discord, Reddit, Jupiter Research Forum, and YouTube. Contributions are weighted, with original content creation receiving higher scores.
- Trading Activities
- Advanced trading functions (DCA, VA, LO, Perp, Ape) are prioritized. The impact of
- stable-stable swaps and sol-sol swaps
- is reduced.
- JUP DAO Involvement
- Stakers
- Eligibility is based on
- time-weighted staking
- . Users must have at least
- 10 JUP staked by 2 Nov 2024
- to qualify.

**Фактори:** real_product_usage, activity_volume, capital_exposure, community_contribution, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Віднімати повернення лише після узгодження пулів; сезонні правила зберігати окремо.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано.

**Джерела:** [Джерело 1](https://discuss.jup.ag/t/archived-grow-the-pie-update-1/21720) · [Джерело 2](https://discuss.jup.ag/t/jup-community-audit-feb-2025/34764) · [Джерело 3](https://discuss.jup.ag/t/jupuary-2025-overview-checker/32013) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/jupiter-jupuary/) · [Посилання з каталогу — потребує перевірки](https://jupuary.jup.ag) · [Посилання з каталогу — потребує перевірки](https://www.jupresear.ch/t/jupiter-airdrop-proposal-for-jupuary-january-2025/23119/1) · [Посилання з каталогу — потребує перевірки](https://x.com/JupiterExchange/status/1882089551726059548)

### 103. Derive

**Дата:** 2025-01-15 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized protocol offering on-chain options, perpetuals, and structured products.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- The airdrop rewards Derive users and LYRA holders based on various participation criteria
- Airdrop Program (May 8, 2024 – Jan 13, 2025)
- Trading
- Earn points based on trading fees, with boosts for specific trades.
- Depositing
- Earn points based on dollar-hours in exchange and vault deposits, with vault-specific boosts.
- Referrals
- Earn points from direct referrals and second-level referrals.
- Airdrop Bonus Rounds
- In round 6, four separate bonuses allocated 2.5% of the airdrop each to the first 1,000 eligible users.
- Migration Eligibility
- LYRA holders
- Over 100,000 LYRA holders could migrate their LYRA to DRV at a 1:1 ratio.
- Staked LYRA
- Users who staked LYRA before the May 8, 2024, snapshot earned a share of 2,529,958 DRV tokens.
- Prestaking Bonus

**Фактори:** snapshot_state, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, referrals, ranking_or_tier.
**Обсяг:** Up to 77,114,554 DRV tokens (7.71% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/derive/) · [Посилання з каталогу — потребує перевірки](https://derive.xyz) · [Посилання з каталогу — потребує перевірки](https://derive.xyz/airdrop) · [Посилання з каталогу — потребує перевірки](https://forums.derive.xyz/t/dip-drv-token-launch-and-functionality/233) · [Посилання з каталогу — потребує перевірки](https://x.com/derivexyz/status/1879334816136736887)

### 104. Loomlay

**Дата:** 2025-01-07 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Loomlay is a no-code platform that allows users to build, launch, and connect autonomous AI agents for collaboration.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Users must meet at least one of the following conditions
- Used the Trenches app within the past 6 months.
- Hold any of the following tokens: $sekoia, $vader, $aixbt, $luna, $game, $virtuals, or $DOP.

**Фактори:** duration_consistency, developer_contribution.
**Обсяг:** 300,000,000 LAY (30% of total supply). **Eligible:** невідомо. **Claimants:** 42,947,271 LAY already claimed.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Зберігати PR, commit, deployment і прийнятий результат, а не лише факт активності.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/loomlay/) · [Посилання з каталогу — потребує перевірки](http://loomlay.com/claim) · [Посилання з каталогу — потребує перевірки](https://dev.loomlay.com/tokens/lay-token) · [Посилання з каталогу — потребує перевірки](https://loomlay.com/) · [Посилання з каталогу — потребує перевірки](https://x.com/loomlayai/status/1874065758080180269)

### 105. BUCKET Protocol

**Дата:** 2025-01-07 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A next-generation Liquidity Layer on the Sui Network, allowing users to mint $BUCK stablecoin by locking assets as collateral, while unlocking opportunities for yield generation and leveraged liquidity.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Airdrop is allocated to early supporters of the BUCKET Protocol.
- Participants with whitelist access may receive a portion of the airdrop.
- Community members actively engaging with the ecosystem are rewarded.
- Specific eligibility details have not been disclosed.

**Фактори:** early_participation, real_product_usage, capital_exposure, activity_diversity, community_contribution, claim_and_vesting.
**Обсяг:** 10% of total supply (100,000,000 $BUT). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/bucket-protocol/) · [Посилання з каталогу — потребує перевірки](https://bucketprotocol.io/) · [Посилання з каталогу — потребує перевірки](https://medium.com/@bucketprotocol/bucket-token-but-tokenomics-3d19a3213b34) · [Посилання з каталогу — потребує перевірки](https://x.com/bucket_protocol/status/1874458007528251762)

### 106. BSX Labs

**Дата:** 2025-01-07 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Decentralized derivatives trading platform on Base, offering up to 1000x leverage and advanced trading features.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Airdrop Breakdown
- 8.65% to BSX Users
- Active traders and liquidity providers across all three pre-TGE seasons.
- Trading bonuses across multiple epochs.
- Referrers.
- 0.5% to Lilquid Holders
- 0.47% to Lilquid NFT Holders.
- 0.03% to Lilquid Traders.
- 4.7M BSX equally distributed among Lilquid NFT holders (except those listed on marketplaces).
- Each eligible NFT holder receives
- 947.25 BSX
- 0.3% to BSX Arena Users
- Users who connected wallets and traded on BSX Arena.
- Top 10,000 users on a leaderboard of 100,000+ participants.
- 0.52% to Community Contributors
- Trader alliance members ($100K+ in trading volume).

**Фактори:** snapshot_state, duration_consistency, activity_volume, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 100,000,000 BSX (10% of total supply). **Eligible:** ~33,000 wallets. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/bsx-labs/) · [Посилання з каталогу — потребує перевірки](https://airdrop.bsxlabs.xyz/en) · [Посилання з каталогу — потребує перевірки](https://bsxlabs.xyz) · [Посилання з каталогу — потребує перевірки](https://discord.com/invite/Jg7q3mV37Z) · [Посилання з каталогу — потребує перевірки](https://docs.bsx.exchange/bsx-docs/usdbsx/bsx-airdrop-complete-guide) · [Посилання з каталогу — потребує перевірки](https://x.com/bsx_labs/status/1879831023690907759)

### 107. Viction

**Дата:** 2025-01-05 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A blockchain ecosystem focused on governance, staking, and active user engagement.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility is determined based on interaction with the Viction ecosystem in the following categories
- 1. Governance Participants (30% Allocation – 375,000 VIC)
- General Allocation (11,305 Eligible Addresses - Equal Share Distribution)
- Addresses that have interacted with
- any
- of the following governance-related activities
- TomomasterDAO voting proposals
- Holding TDAO tokens
- Participating in Viction proposals on the Saigon Network
- Voting for Saigon Network Upgrade and VIP #1
- Bonus Allocation (4,258 Eligible Addresses - Weighted Share Distribution)
- Addresses that specifically
- voted for the Saigon Network Upgrade and VIP #1
- The
- number of VIC tokens delegated for voting
- determines the

**Фактори:** snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, nft_or_asset_holding, ranking_or_tier.
**Обсяг:** 1,250,000 VIC tokens. **Eligible:** 178,000+ unique wallet addresses. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/viction/) · [Посилання з каталогу — потребує перевірки](https://blog.viction.xyz/viction-retrodrop-season-1-by-the-community-for-the-community-2/) · [Посилання з каталогу — потребує перевірки](https://retrodrop.viction.xyz) · [Посилання з каталогу — потребує перевірки](https://viction.xyz)

### 108. Sonic Svm

**Дата:** 2025-01-03 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** The first SVM network extension on Solana, designed for games and applications. It powers the Web3 TikTok App Layer to onboard the next billion users.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligible participants include
- Sonic AVS Delegators
- Users who delegated SOL or eligible Liquid Staking Tokens (LSTs) to Sonic AVS via Solayer, including staking through Adrastea and Rate-X.
- Node Holders
- Holders of HyperFuse Observer Nodes receive $SONIC based on the number of nodes they own.
- Odyssey Participants
- Must meet all four conditions
- Completed tasks on at least 2 of the 3 networks: Origin, Frontier V0, or Frontier V1.
- Completed at least 14 check-in tasks.
- Accumulated at least 500 Rings.
- Hold a Sonic Odyssey Pass NFT.
- SonicX Users
- Players who logged in with TikTok accounts and played SonicX before or during the TikTok Airdrop Campaign.
- World Store Points Holders
- Top 500 users on the World Store leaderboard who bound their Solana wallet before the snapshot.
- Mirror NFT Holders

**Фактори:** snapshot_state, duration_consistency, capital_exposure, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 7% of total $SONIC supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/sonic-svm/) · [Посилання з каталогу — потребує перевірки](https://airdrop.sonic.game/) · [Посилання з каталогу — потребує перевірки](https://odyssey.sonic.game/) · [Посилання з каталогу — потребує перевірки](https://sonic.feather.blog/sonic-initial-claim-a-reward-for-the-community) · [Посилання з каталогу — потребує перевірки](https://www.sonic.game/) · [Посилання з каталогу — потребує перевірки](https://x.com/SonicSVM/status/1875069287028912627)

### 109. idriss

**Дата:** 2025-01-01 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** IDRISS offers applications that integrate cryptocurrency and AI to enhance user experiences, including browser extensions for crypto transactions and tools for creators to monetize content.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- IDRISS Users (13% of TTS – 22,418 addresses)
- Account Registration
- Paid Account
- Registered with a $10 fee; carries 10× weight over free accounts or extension use.
- Free Account
- Joined via allowlisting, campaigns, or giveaways.
- Browser Extension Use
- Made transfers on 2 unique days using the extension on any mainnet network.
- Early User Multiplier
- Multiplier = (Days since registration / Total days since 2022 launch) + 1.
- Referral Multiplier
- Multiplier = Cubic root of (Invites + 1). For example, 7 invites = Multiplier of 2.
- Gitcoin Donors (2.5% of TTS – 18,916 addresses)
- Donated a minimum of $20 to any project in Gitcoin open-source rounds from GR15 (Sept 2022) to GG20 (Apr 2024).
- Sale Participants (1% of TTS – 531 addresses)
- Purchased IDRISS tokens during the first 12 hours of the sale.

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, activity_volume, points_quests, nft_or_asset_holding, community_contribution, referrals, ranking_or_tier.
**Обсяг:** 20% of Total Token Supply (TTS). **Eligible:** 71,130. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/idriss/) · [Посилання з каталогу — потребує перевірки](https://docs.idriss.xyz/idriss-token/retroactive-distribution) · [Посилання з каталогу — потребує перевірки](https://idriss.xyz/) · [Посилання з каталогу — потребує перевірки](https://x.com/idriss_xyz/status/1884017261708730648)

### 110. Usual

**Дата:** 2024-12-18 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized stablecoin ecosystem designed to reward early adopters and liquidity providers through an innovative incentive structure.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Users earn eligibility for the airdrop based on their accumulation of
- Usual Pills
- , which are pre-launch points distributed through various activities within the Usual protocol. The more Pills a user collects, the greater their share of the $USUAL airdrop.
- Ways to Earn Pills
- Issuing USD0++
- on the primary market (5 Pills per USD0++)
- Holding USD0++
- (3 Pills daily)
- Providing Liquidity on Curve
- USD0/USD0++ LP (3 Pills daily)
- USD0/FXUSD LP (1 Pill daily)
- Providing Liquidity on Balancer & Maverick
- USD0/GHO LP (1 Pill daily)
- Using Morpho
- Posting USD0++ collateral (3 Pills daily)
- Holding USD0/USD0++ LP collateral (3 Pills daily)

**Фактори:** early_participation, snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, ranking_or_tier.
**Обсяг:** 7.5% of the Fully Diluted Valuation (FDV). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/usual/) · [Посилання з каталогу — потребує перевірки](https://app.usual.money) · [Посилання з каталогу — потребує перевірки](https://docs.usual.money/pre-launch-rules/usual-airdrop) · [Посилання з каталогу — потребує перевірки](https://usual.money) · [Посилання з каталогу — потребує перевірки](https://x.com/usualmoney/status/1865039758919159863) · [Посилання з каталогу — потребує перевірки](https://x.com/usualmoney/status/1869323792486642140)

### 111. Avalanche

**Дата:** 2024-12-18 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** The Avalanche Foundation is a non-profit entity that fosters the advancement and growth of the Avalanche platform for the world.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Community Airdrop Eligibility
- The airdrop targeted active and loyal Avalanche users, focusing on
- Memecoin Rush Participants
- Users who participated in the Memecoin Rush program.
- Diamond Hands
- Wallets that demonstrated loyalty to the Avalanche ecosystem.
- Historic Avalanche Users
- Wallets with a history of involvement in the Avalanche ecosystem.
- Data from Trader Joe identified Memecoin Rush participants and Diamond Hands. Non-Diamond Hands participants were ranked into tiers based on their historic on-chain activity, utilizing data from The Tie’s Frosty Metrics Chill Factor categorizations. Efforts were made to exclude non-qualifying wallets, such as exchange wallets, bots, and those involved in wash trading.
- Retrodrop Eligibility
- Participants who voted for projects on Retro9000 are eligible for the RETRODROP.

**Фактори:** activity_volume, activity_diversity, community_contribution, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Оцінювати якість і підтверджуваність внеску; масовий spam підвищує Sybil-ризик.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/avalanche/) · [Посилання з каталогу — потребує перевірки](https://avax.network) · [Посилання з каталогу — потребує перевірки](https://www.avax.network/blog/avalanche-foundation-the-community-airdrop) · [Посилання з каталогу — потребує перевірки](https://www.avax.network/blog/core-airdrop-tool-distribute-tokens-and-reward-your-community-on-avalanche) · [Посилання з каталогу — потребує перевірки](https://www.avax.network/blog/retro9000-a-40m-grant-program-rewards-developers-building-avalanche-l1s) · [Посилання з каталогу — потребує перевірки](https://x.com/AvalancheFDN/status/1869429830196048212)

### 112. Pudgy Penguins

**Дата:** 2024-12-17 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A popular NFT collection and ecosystem focused on Web3 and community-driven engagement, featuring digital collectibles, physical toys, and cross-chain initiatives.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Exact airdrop criteria were not explicitly detailed in a single official list across all sources, the following points are inferred from announcements, posts on X, and related web content.
- The airdrop is open to multiple categories of users
- Pudgy Penguins Ecosystem NFT Holders
- Pudgy Penguins NFT: ~1.7 million PENGU per NFT
- Lil Pudgys NFT: Over 188,000 PENGU per NFT
- Pudgy Rods: Between 105,000 and 195,000 PENGU, depending on rarity
- Pudgy Penguins SBTs: Eligible, but allocation details are unclear
- Pudgy Toys Owners
- Physical Pudgy Toys (sold at retailers) qualify, but claims will open once the Abstract Chain mainnet launches.
- OG Ethereum and Solana Users
- Active or early Ethereum and Solana users, with over 7 million wallets included.
- Exact qualification criteria are not specified.
- Other Web3 Communities
- 24.12% of the PENGU supply is allocated to various Web3 communities.
- Specific communities are not detailed, but the Abstract Discord “Elite” role is mentioned.
- FTT Token Holders

**Фактори:** early_participation, snapshot_state, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, claim_and_vesting.
**Обсяг:** 44.8 billion PENGU tokens (allocated to eligible users). **Eligible:** Over 7 million wallets across Ethereum, Solana, and Web3 communities. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/pudgy-penguins/) · [Посилання з каталогу — потребує перевірки](https://claim.pudgypenguins.com) · [Посилання з каталогу — потребує перевірки](https://pudgypenguins.com/) · [Посилання з каталогу — потребує перевірки](https://x.com/pudgypenguins/status/1869004989731160153)

### 113. Elys

**Дата:** 2024-12-17 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Elys Network is a NextGen decentralized perpetual trading and leverage LP platform built on a fast Layer 1 blockchain. It offers ultra-low fees, multi-token liquidity pools, a decentralized oracle for price aggregation, and an intuitive WebApp for seamless onboarding.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Elys Network airdrop was based on the following requirements
- Testnet Participation (Odyssey Testnet)
- Phase 1: 95+ on-chain interactions (Tier 2 NFT), 195+ on-chain interactions (Tier 1 NFT), snapshot July 1, 2024
- Phase 2: Combined with Phase 1, 485+ total interactions (Tier 1 NFT), lower threshold for Tier 2 NFT
- Participation required daily swaps, staking, and liquidity actions
- ATOM Staker Allocation
- ATOM stakers (Cosmos Hub) eligible
- Increased allocation for voting on Proposal 897 (ICS 2.0 integration), later simplified to staking ATOM
- NFT Holders & Community Roles
- Elysian Legend & Horde NFT holders
- ELYS Phase 1 & 2 NFT holders
- Cadet Role (Discord): 372 ELYS at mainnet launch + additional rewards
- Major Role (Discord): Special allocations
- Hydro Users & stATOM Holders: Pending confirmation
- Mainnet Incentive Program
- 50% of the airdrop allocated for post-mainnet activity (staking, liquidity, swaps)

**Фактори:** snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, testnet_participation, nft_or_asset_holding, community_contribution, ranking_or_tier.
**Обсяг:** 14% of total token supply (distributed over 2 years). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/elys/) · [Посилання з каталогу — потребує перевірки](https://airdrop.elys.network) · [Посилання з каталогу — потребує перевірки](https://app.elys.network) · [Посилання з каталогу — потребує перевірки](https://cosmos.leapwallet.io/airdrops) · [Посилання з каталогу — потребує перевірки](https://elys.network/) · [Посилання з каталогу — потребує перевірки](https://elysnetwork.medium.com/elys-networks-january-2024-update-testnet-airdrop-and-more-f842f7452a20) · [Посилання з каталогу — потребує перевірки](https://linktr.ee/elysnetwork)

### 114. Vana

**Дата:** 2024-12-16 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Vana is an EVM-compatible Layer 1 blockchain enabling users to tokenize, control, and monetize their data for AI model training through DataDAOs and privacy-preserving technologies.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participation in testnet (since July 2024)
- Data pre-mining via DataDAOs (Accelerator Program, until 2024-12-10)
- Builder community activity in Discord (snapshot 2024-12-13)
- Holding V on Vana NFT (snapshot 2024-12-13)
- Reddit DataDAO contributions (snapshot 2024-12-13)
- Early explorer activity on Data Hub
- Staking and DataDAO rewards (15% of supply for top DataDAOs by stake)
- DataDAO creation and builder rewards
- Community claim for testnet phase participants, DataDAO Pre-Miners, Discord leaders, NFT holders, and $RDAT holders (
- source
- Additional Airdrop Opportunities
- Ongoing and future community rewards for new DataDAO contributors, stakers, and builders
- Gas-free period for Aurora Cohort DataDAOs at mainnet launch
- 12 Days of DataDAOs: first 10,000 contributors can claim free $VANA to participate (
- Staking rewards: 400,000 $VANA distributed to top 16 DataDAOs every 21 days (

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, developer_contribution, claim_and_vesting.
**Обсяг:** Not specified (part of 44% community allocation; 400,000 VANA for initial staking rewards). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/vana/) · [Посилання з каталогу — потребує перевірки](http://datahub.vana.com) · [Посилання з каталогу — потребує перевірки](https://docs.vana.org/docs/vana-token-overview) · [Посилання з каталогу — потребує перевірки](https://usevana.typeform.com/to/lnvWJUhM) · [Посилання з каталогу — потребує перевірки](https://www.vana.org/) · [Посилання з каталогу — потребує перевірки](https://www.vana.org/posts/introducing-community-rewards) · [Посилання з каталогу — потребує перевірки](https://x.com/vana/status/1867038751979081923)

### 115. SwanChain

**Дата:** 2024-12-16 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A full toolset AI blockchain infrastructure accelerating AI adoption by merging Web3 with AI, providing comprehensive solutions across storage, computing, bandwidth, and payments.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the SwanChain airdrop was based on the following requirements
- Daily Tasks
- Complete daily tasks released on the platform.
- Tasks are updated regularly and contribute to Swan Points accumulation.
- Daily Combo Minigame
- Participate in the “Daily Combo” minigame.
- Successfully complete combinations to earn additional Swan Points.
- Referral Program
- Invite friends to participate in the SwanChain ecosystem.
- Earn 10% of the total points accumulated by your referrals.
- Referred friends receive a 20% point boost on their earned points.

**Фактори:** activity_diversity, points_quests, referrals, ranking_or_tier.
**Обсяг:** 20% of total token supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Зберігати season, формулу points, mandatory/bonus дії та версію правил. Вважати referral додатковим множником, якщо правила не визначають його обов’язковим.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/swanchain/) · [Посилання з каталогу — потребує перевірки](https://mission.swanchain.io/) · [Посилання з каталогу — потребує перевірки](https://swanchain.medium.com/swan-chain-mission-engage-and-earn-swan-airdrop-8a91d96f9ec7) · [Посилання з каталогу — потребує перевірки](https://twitter.com/swan_chain) · [Посилання з каталогу — потребує перевірки](https://www.swanchain.io)

### 116. Overprotocol

**Дата:** 2024-12-16 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** OverProtocol is a Layer 1 blockchain with lightweight nodes, allowing individuals to run validators on personal computers. It aims to create a decentralized, community-driven network.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the OverProtocol airdrop was based on the following requirements
- OverWallet Users
- Must pass Sybil Detection.
- Airdrop amount depends on OverWallet points, Friend Cards, and testnet activities.
- Sybil Detection is available until May 31, 2024, at 2:59 PM UTC.
- OverNode Testnet Participants
- Users must have participated in Open Beta Testnet Season 1 & 2.
- No Sybil detection required.
- No additional tasks needed.
- Season 1 Details
- Season 2 Details
- Nethers NFT Holders
- Must own a Nethers NFT and transfer it to OverProtocol’s chain.
- Airdrop varies based on total NFT sales
- If 20,000 NFTs are sold: 500 OVER per NFT.
- If fewer NFTs are sold: 10 million OVER tokens divided by total NFTs sold.

**Фактори:** snapshot_state, duration_consistency, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, anti_sybil_identity.
**Обсяг:** 10 million OVER tokens for Nethers NFT holders (distribution per NFT varies). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/overprotocol/) · [Посилання з каталогу — потребує перевірки](https://medium.com/overprotocol/overprotocol-who-is-eligible-for-airdrop-2-63a754909e50) · [Посилання з каталогу — потребує перевірки](https://overprotocol.io) · [Посилання з каталогу — потребує перевірки](https://web.archive.org/web/20240525195312/https://medium.com/overprotocol/overprotocol-who-is-eligible-for-the-airdrop-1dfaa5d3460c) · [Посилання з каталогу — потребує перевірки](https://web.archive.org/web/20240817231852/https://medium.com/overprotocol/overprotocol-who-is-eligible-for-airdrop-2-63a754909e50)

### 117. Odos Protocol

**Дата:** 2024-12-13 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A DeFi protocol optimizing token swaps and trades with advanced routing and aggregation mechanisms.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Odos Protocol airdrop was based on the following requirements
- Trading Volume Requirements
- Complete at least $100 of qualified trading volume on the Odos protocol.
- Trading must occur across at least three unique days.
- Activity period: March 11, 2022 – August 28, 2024.
- Allocation Factors
- The following factors influenced token allocation
- Total trading volume (weighted by pair type)
- Number of unique days with transactions
- Number of unique weeks with transactions
- Gas consumption during the period
- Participation in NFT campaigns
- Number of unique traded pairs
- Number of blockchain protocols used
- Loyalty Tier System
- Users who claim before December 31, 2024, will be placed directly into their respective Loyalty tier.

**Фактори:** duration_consistency, real_product_usage, activity_volume, points_quests, nft_or_asset_holding, claim_and_vesting, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** 532,590 wallets. **Claimants:** невідомо.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/odos-protocol/) · [Посилання з каталогу — потребує перевірки](https://app.odos.xyz/) · [Посилання з каталогу — потребує перевірки](https://docs.odos.xyz/home/loyalty/) · [Посилання з каталогу — потребує перевірки](https://www.odos.xyz/) · [Посилання з каталогу — потребує перевірки](https://x.com/odosdao/status/1867300703401914633)

### 118. Anzen

**Дата:** 2024-12-13 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A DeFi protocol focused on real-world yield and stablecoin adoption through its USDz stablecoin ecosystem.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Anzen airdrop was based on the following requirements
- USDz Ecosystem Engagement
- Minting USDz
- Converting stablecoins like USDC into USDz.
- Holding USDz
- Maintaining USDz in a wallet.
- Staking USDz
- Staking in pools to earn yields and points.
- Providing Liquidity
- Contributing to USDz-USDC LPs on Aerodrome or Uniswap.
- Z-Points System
- Users accumulated z-points by interacting with USDz.
- The campaign ended in early December 2024.
- 5% of the total $ANZ supply was allocated to z-points holders for the Season 1 airdrop.
- Tiered Distribution Model
- Top 500 Wallets

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, claim_and_vesting, ranking_or_tier.
**Обсяг:** 5% of the total 10 billion ANZ supply (500 million ANZ tokens). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/anzen/) · [Посилання з каталогу — потребує перевірки](https://anzen.finance) · [Посилання з каталогу — потребує перевірки](https://anzen.finance/anz-is-live) · [Посилання з каталогу — потребує перевірки](https://anzen.finance/anzen-airdrop-overview) · [Посилання з каталогу — потребує перевірки](https://app.fjordfoundry.com/token-sales/0x0Ce128bb5B1CBDc433f667905d0493eDc4ECEF80) · [Посилання з каталогу — потребує перевірки](https://app.sablier.com/?t=recipient) · [Посилання з каталогу — потребує перевірки](https://app.sablier.com/airstream/0x164cd04a5209cae95bb976aae8abd66ee207f43a-8453/)

### 119. Suilend

**Дата:** 2024-12-12 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Suilend is a decentralized lending protocol built on the Sui blockchain, aiming to provide efficient and scalable lending solutions for users.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- General Eligibility
- Active Participation on Suilend
- Before launch, users earned points by depositing or borrowing assets (SUI, USDC, USDT, ETH, SOL, DEEP).
- 20 million points were distributed daily (10M for deposits, 10M for borrowing).
- After August 17, 2024, points were awarded only for borrowing (10M points daily).
- The more points accumulated, the higher the potential $SEND token allocation.
- Post-Launch Airdrop Eligibility (Season 1 & Beyond)
- Season 1
- Airdrop followed the December 10, 2024 snapshot.
- Season 2 (ongoing as of March 24, 2025)
- Likely still based on lending/borrowing engagement, but exact criteria should be checked via official Suilend channels.
- Wallet Requirements
- A Sui-compatible wallet is required (e.g.,
- Sui Wallet, Nightly Wallet
- In Season 1, mobile wallets were emphasized for eligibility.
- Supported Assets

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding.
**Обсяг:** 40% of the $SEND supply (40M SEND). **Eligible:** Number of Claimants. **Claimants:** Timeline.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/suilend/) · [Посилання з каталогу — потребує перевірки](https://blog.suilend.fi/maturing-airdrop-7c8e508846b9) · [Посилання з каталогу — потребує перевірки](https://docs.suilend.fi/send/tokenomics-and-mdrops) · [Посилання з каталогу — потребує перевірки](https://suilend.fi)

### 120. KIP

**Дата:** 2024-12-10 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** KIP Protocol is a decentralized AI framework enabling owners of AI apps, models, and knowledge bases to deploy, connect, and monetize their AI assets in Web3. It empowers developers and contributors through a robust, battle-tested infrastructure and community-driven incentives.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Uprising Users: Accumulate over 2000 Uprising Points (including Season 1), link wallet and Discord, complete all basic tasks before snapshot
- Genesis Pass NFT Holders: Hold revealed Genesis Pass NFT (Legendary, Rare, Uncommon tiers receive more); NFT must be delisted from secondary markets before claim
- Node Early Buyers: Verified node holders, fully unlocked at TGE
- KIP 100X SBT Holders: SBT holders, fully unlocked at TGE
- Anti-Sybil measures: Automated detection, community feedback, internal checks
- Additional Airdrop Opportunities
- Additional node operator rewards for active participation (to be announced)
- Staking incentives from the Airdrop & Staking pool
- Additional Notes
- Uprising Users and SBT Holders: 30% unlocked at TGE, 70% released in 14% monthly increments over 5 months
- Node Early Buyers and SBT Holders: 100% unlocked at TGE
- Genesis Pass NFT Holders: 30% unlocked at TGE, 70% released in 14% monthly increments over 5 months; must delist NFT to claim
- Uprising/SBT claim deadline: 14 days after TGE (unclaimed 70% forfeited)
- Node claim deadline: 180 days after TGE
- Genesis Pass NFT claims tied to NFT, no specific deadline but must be delisted

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, developer_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 850,000,000 KIP (8.5% of total supply). **Eligible:** Not disclosed. **Claimants:** Not disclosed.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kip/) · [Посилання з каталогу — потребує перевірки](https://kip.pro) · [Посилання з каталогу — потребує перевірки](https://uprising.kip.pro/claim) · [Посилання з каталогу — потребує перевірки](https://uprising.kip.pro/nft) · [Посилання з каталогу — потребує перевірки](https://www.kip.pro/blog-posts/kip-tokenomics) · [Посилання з каталогу — потребує перевірки](https://x.com/KIPprotocol/status/1866076757478310285?lang=en)

### 121. Movement

**Дата:** 2024-12-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A modular blockchain ecosystem designed for scalability, efficiency, and developer-friendly innovation.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Movement airdrop was based on the following requirements
- Road to Parthenon
- Completed at least two transactions on two apps on the Porto or Suzuka Movement Testnet (capped at 300 transactions).
- Completed quests in the Road to Parthenon campaign. Rewards depend on the number of quests completed.
- Anti-sybil protection
- Wallets that made testnet transactions but did not claim from a faucet are ineligible.
- Battle of Olympus Hackathon
- 10 winners and 53 runners-up receive allocations.
- Hackathon period: May - September 2024.
- Gmove Campaign
- Users who tweeted “gmove” were selected at random.
- #gmovechallenge participants, whose submissions were screened, receive larger allocations.
- Selected Communities
- Movement Discord
- Holders of select roles earned through completing tasks.
- Centurions

**Фактори:** snapshot_state, real_product_usage, activity_diversity, points_quests, testnet_participation, nft_or_asset_holding, community_contribution, developer_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 1,000,000,000 MOVE (10% of maximum supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/movement/) · [Посилання з каталогу — потребує перевірки](https://www.movementnetwork.xyz) · [Посилання з каталогу — потребує перевірки](https://www.movementnetwork.xyz/article/movement-network-foundation-movedrop-move-token) · [Посилання з каталогу — потребує перевірки](https://x.com/movementfdn/status/1861472760138211786)

### 122. Streamflow

**Дата:** 2024-12-07 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized protocol focused on digital asset management, including token streaming, vesting, and incentive alignment.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligible participants include
- Streamflow Users
- Users who interacted with Streamflow over the past three years, particularly those who generated protocol revenue, contributed to Total Value Locked (TVL), Total Value Deposited (TVD), and engaged in economic activity.
- Odyssey Mission Participants
- Participants in the Odyssey campaign received up to a 10% bonus to their allocation score, depending on mission completion and whether they earned the Hero Bonus.
- DROPZ Content Creators
- Individuals who contributed content under the DROPZ program.
- Ecosystem Supporters
- Including all
- Superteam
- members.
- Launch Campaign Participants
- Additional recipients from undisclosed launch campaigns (more details were supposed to be announced).
- Users who met these criteria are encouraged to check their eligibility at
- Streamflow Foundation’s official website

**Фактори:** real_product_usage, capital_exposure, activity_diversity, points_quests, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** Not Known (Total token supply: 1 billion STREAM). **Eligible:** Approximately 100,000 addresses. **Claimants:** невідомо.
**Урок:** Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/streamflow/) · [Посилання з каталогу — потребує перевірки](https://docs.streamflow.foundation/en/articles/10174556-dynamic-vested-airdrop) · [Посилання з каталогу — потребує перевірки](https://streamflow.foundation) · [Посилання з каталогу — потребує перевірки](https://x.com/StreamflowFDN/status/1865039981208846633)

### 123. SynFutures

**Дата:** 2024-12-06 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** SynFutures is a decentralized protocol for perpetual futures, enabling users to trade any asset and create arbitrary futures contracts, with a unified AMM and on-chain order book model.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Trading or providing liquidity on SynFutures v1, v2, or v3
- Participation in Oyster Odyssey (O_O) campaign (March 1, 2024 – November 25, 2024)
- Long-term engagement and activity across multiple protocol versions
- Community engagement (social channels, campaign leaderboards, trading competitions)
- Snapshot date: 2024-11-25
- Additional Airdrop Opportunities
- Season 2 airdrop and staking boost: Details TBA; users can boost future rewards by staking F tokens and engaging in ecosystem development
- Verification Methods
- On-chain activity and campaign participation tracked by protocol
- Exclusion of addresses flagged for Sybil, wash trading, or suspicious activity
- Claim Process
- Claim portal
- synfutures.foundation/airdrop
- Claim window: 2024-12-06 10:00 UTC to 2025-03-06 10:00 UTC
- 100% of airdrop unlocked at TGE

**Фактори:** snapshot_state, duration_consistency, real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 750,000,000 F (7.5% of total supply, Season 1). **Eligible:** Not specified. **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/synfutures/) · [Посилання з каталогу — потребує перевірки](http://synfutures.foundation/airdrop) · [Посилання з каталогу — потребує перевірки](https://medium.com/synfutures/introducing-synfutures-foundation-and-the-f-token-207bf843f0eb) · [Посилання з каталогу — потребує перевірки](https://medium.com/synfutures/synfutures-f-airdrop-5a849c464ffb) · [Посилання з каталогу — потребує перевірки](https://superbridge.app/) · [Посилання з каталогу — потребує перевірки](https://www.synfutures.com/) · [Посилання з каталогу — потребує перевірки](https://x.com/SynFuturesDefi/status/1863908060722581640)

### 124. Lumoz

**Дата:** 2024-12-06 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Lumoz is a modular compute layer and ZK-RaaS platform, enabling one-click Layer 2 deployment, zkVerifier nodes, and a dual-token model for scalable, privacy-focused infrastructure.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Early Lumoz Participants: Historical activities snapshot (Lumoz Point holders, bonus for >500 points)
- Lumoz PoW Testnet Users: PoW snapshot (ZK mining, Nov 5–Dec 5, 2024)
- Lumoz Node Holders: Node ownership snapshot (zkVerifier License, Oct 26, 2024)
- Lumoz Ecosystem Users: Activity snapshot & participation (Merlin Chain, ZKFair, Ultiverse, Matr1X, etc.)
- ETH Ecosystem Users: Snapshot (active DeFi users on Ethereum, Polygon, Arbitrum in past 6 months)
- Celestia & Move Ecosystem Users: Snapshot (Celestia stakers, Aptos/Sui DeFi users in past 6 months)
- Other Ecosystem Partners: To be announced
- Additional Airdrop Opportunities
- OG NFT Campaign: Claim OG NFTs to unlock/convert esMOZ to MOZ at 1:1 ratio (NFTs can bypass vesting)
- Partner/Community Airdrops: CARV, UXLINK, and other project communities
- High-quality project partners and ecosystem contributors
- Verification Methods
- On-chain activity and snapshot verification for all groups
- Airdrop query portal
- lumoz.org/airdrop

**Фактори:** early_participation, snapshot_state, duration_consistency, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, developer_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 1,000,000,000 esMOZ (10% of total supply, ~$30M value). **Eligible:** Over 3 million airdrop queries; 100,000+ OG NFTs claimed. **Claimants:** Not specified.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/lumoz/) · [Посилання з каталогу — потребує перевірки](https://lumoz.org/) · [Посилання з каталогу — потребує перевірки](https://lumoz.org/airdrop) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/lumozoLumoz) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/lumozorg.eth/pKVKnZxtqR2IhcEsZ2wfShvX8kOz0-Q8VdyboiNGeNo) · [Посилання з каталогу — потребує перевірки](https://node.lumoz.org/) · [Посилання з каталогу — потребує перевірки](https://x.com/LumozOrg/status/1864216862218965470)

### 125. Burnt (XION)

**Дата:** 2024-12-05 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** XION is the first walletless Layer 1 blockchain focused on making Web3 accessible to everyone. It facilitates network usage fees, governance, proof-of-stake security, liquidity, and serves as a medium of exchange.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the XION airdrop was based on the following requirements
- XION Community (69%)
- Testnet users (top leaderboard ranks, active participants in EarnOS, BlockX, XionEverywhere, Galxe campaigns, and more)
- Blaze Syndicate members (various ranks, regional moderators, Inner Syndicate, weekly game winners, content contributors)
- Builders who transitioned to the mainnet
- Ecosystem Communities
- A portion of the airdrop is allocated to significant communities that have contributed to Web3 culture and innovation, including
- SPX6900, Gigachad, Based Brett, Mocaverse, Berachain, Monad, Pyth, Milady & Remilio, Injective, Tensorian
- Special Recognitions
- Nota-BALD Believers, People Whose Name Sounds Like XION, Murad (memecoin culture)
- Exclusions & Anti-Sybil Measures
- XION core team and partner project wallets were excluded.
- Sybil attacks were mitigated using machine learning models analyzing clustering behaviors, asset transfers, and known sybil addresses.
- Users who believe they were mistakenly excluded may submit an appeal.

**Фактори:** duration_consistency, capital_exposure, activity_diversity, points_quests, testnet_participation, community_contribution, developer_contribution, anti_sybil_identity, ranking_or_tier.
**Обсяг:** 10,000,000 XION (5% of total supply). **Eligible:** Hundreds of thousands of wallets across 10+ ecosystems. **Claimants:** невідомо.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/burnt-xion/) · [Посилання з каталогу — потребує перевірки](https://believe.xion.burnt.com) · [Посилання з каталогу — потребує перевірки](https://xion.burnt.com) · [Посилання з каталогу — потребує перевірки](https://xion.burnt.com/blog/xion-airdrop-believe-in-something-the-first-spark)

### 126. ORA Coin

**Дата:** 2024-12-01 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** ORA is a World Intelligence Network connecting all intelligence, pioneering verifiable onchain AI with products like opML, OAO, and RMS. It enables decentralized, trustless AI computation and infrastructure across multiple blockchains.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Participate in the ORA Points Program
- Snapshot already taken (date not specified)
- Claim via ORA Airdrop Portal: sign wallet message, update Twitter handle, submit receiving address
- $ORA distributed on Base chain (contract: 0x333333C465a19C85f85c6CfbED7B16b0B26E3333)
- Personal wallet required (not exchange address)
- Additional Airdrop Opportunities
- Future airdrop seasons and ecosystem incentives may be announced
- Additional Notes
- $ORA claim process: tokens arrive in ~10 minutes after claim
- Security: always verify URLs and never share private keys
- $ORA utility: access to IMO, node operations, governance, future ecosystem features
- ORA enables verifiable AI computation and decentralized intelligence

**Фактори:** early_participation, snapshot_state, duration_consistency, activity_diversity, points_quests, node_validator_work, claim_and_vesting.
**Обсяг:** 10% of total supply. **Eligible:** Not disclosed. **Claimants:** Not disclosed.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/ora-coin/) · [Посилання з каталогу — потребує перевірки](https://foundation.ora.io) · [Посилання з каталогу — потребує перевірки](https://foundation.ora.io/app/airdrop) · [Посилання з каталогу — потребує перевірки](https://ora.io) · [Посилання з каталогу — потребує перевірки](https://research.ora.io/t/ora-airdrop-10-of-ora-to-points-program-participants/65)

### 127. Kontos

**Дата:** 2024-12-01 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Kontos is a zk-powered, AI-enhanced chain-abstraction infrastructure by Zecrey Labs, enabling account, asset, chain, and action abstraction for seamless multi-chain user experience. It offers gasless, assetless, and keyless operations with a single account for multiple blockchains.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Create or recover a Kontos wallet via the official website
- Connect your wallet and check eligibility on the airdrop portal
- Complete specific tasks (e.g., follow Kontos on X, retweet campaign posts)
- Deposit a minimum amount (e.g., 10 MNT) to Kontos account
- Perform at least one bridge transaction (min $1) using /bridge command
- Optionally, use /trade command for additional rewards
- For Bybit Airdrop Arcade: deposit tokens (e.g., 10 MNT) to Kontos account for OATs or share of 400,000 KOS pool
- Use a personal wallet (not exchange address) to receive airdrop
- Pay small transaction fee (Base ETH required for EVM claims)
- Additional Airdrop Opportunities
- Referral bonuses for inviting friends (e.g., invite 3 friends for OATs/points)
- Community engagement in Discord for potential extra rewards
- Ongoing campaigns and new tasks announced via official channels
- Additional Notes
- Airdrop campaign remains open with no time limit for claims

**Фактори:** real_product_usage, activity_volume, capital_exposure, activity_diversity, points_quests, community_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** Not disclosed. **Eligible:** Not disclosed. **Claimants:** Not disclosed.
**Урок:** Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kontos/) · [Посилання з каталогу — потребує перевірки](https://airdrop.kontos.io) · [Посилання з каталогу — потребує перевірки](https://docs.kontos.io/explore-kontos/events/kontos-airdrop) · [Посилання з каталогу — потребує перевірки](https://kontosio.medium.com/kontos-december-2024-roundup-a-month-of-milestones-kos-launches-ecosystem-growth-and-bold-7ff1134f6f78) · [Посилання з каталогу — потребує перевірки](https://www.kontos.io) · [Посилання з каталогу — потребує перевірки](https://x.com/Kontosio/status/1868854933795356981) · [Посилання з каталогу — потребує перевірки](https://x.com/Kontosio/status/1869256478185738267)

### 128. Hyperliquid

**Дата:** 2024-11-29 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** A decentralized trading platform offering high-performance perpetual futures trading and innovative DeFi solutions.
**Статуси:** source_checked_historical_product; published_distribution_analysis.

**Умови/дії:**

- Eligibility for the Hyperliquid airdrop was based on the following requirements
- Points Accumulation
- Users needed to earn points by March 26, 2024.
- Points were the key determinant for airdrop eligibility, with volume traded being the primary factor in earning points.
- Acceptance of Terms
- Users were required to accept the new Terms & Conditions on the website before the token launch in April 2024.
- Those who failed to accept the Terms & Conditions in time missed out on the airdrop.
- Users who accepted the T&Cs late (during the fourth reopening) received a 50% slashed airdrop due to the inability to run sybil detection on the final batch of participants.
- Distribution
- The airdrop was distributed directly to users’ Hyperliquid accounts.
- There was speculation about a tiered distribution based on user league rankings.

**Фактори:** activity_volume, points_quests, referrals, anti_sybil_identity, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Points не мають універсального сталого курсу конвертації; фази й умови зберігати окремо.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано. Офіційний підсумковий genesis dataset та точний фактичний обсяг.

**Джерела:** [Джерело 1](https://hyperliquid.gitbook.io/hyperliquid-docs/points) · [Джерело 2](https://www.sec.gov/Archives/edgar/data/2090011/000121390026016539/ea0276878-s1a1_21shares.htm) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/hyperliquid/) · [Посилання з каталогу — потребує перевірки](https://app.hyperliquid.xyz/trade) · [Посилання з каталогу — потребує перевірки](https://hyperfoundation.org/) · [Посилання з каталогу — потребує перевірки](https://x.com/HyperliquidX/status/1862402701705060486)

### 129. Bluefin

**Дата:** 2024-11-28 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized spot and derivatives trading platform built on the Sui blockchain.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Existing Bluefin participants and long-standing community members were prioritized.
- Eligibility included
- Members of Bluefin Trader Alliance, Firefly Pioneers, Bluefin Ambassadors, and Bluefin Leagues.
- Users from the Sui ecosystem and external partners (Jupiter, Aerodrome, Wormhole, Pyth, Elixir).
- NFT communities (Pudgy Penguins, MadLads, Azuki, Prime Machin).
- Specific allocations per user were determined by project partners.
- Users must provide liquidity to any Bluefin pool to claim their airdrop at TGE.

**Фактори:** early_participation, activity_volume, capital_exposure, activity_diversity, nft_or_asset_holding, community_contribution, claim_and_vesting.
**Обсяг:** 19.68% of total BLUE supply (Exact token count not specified). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/bluefin/) · [Посилання з каталогу — потребує перевірки](https://bluefin.io) · [Посилання з каталогу — потребує перевірки](https://docs.google.com/document/d/1lP4nuyVlzW8UzM1kfjsj3Q-GuXBV9Oe3/edit) · [Посилання з каталогу — потребує перевірки](https://learn.bluefin.io/bluefin/bluefin-airdrop/bluefin-airdrop-explained) · [Посилання з каталогу — потребує перевірки](https://trade.bluefin.io/liquidity-pools) · [Посилання з каталогу — потребує перевірки](https://x.com/bluefinapp/status/1862158394733252648) · [Посилання з каталогу — потребує перевірки](https://x.com/bluefinapp/status/1878078200372236462)

### 130. Worldcoin

**Дата:** 2024-11-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized protocol aiming to provide a universal digital identity (World ID) and a global currency (WLD) to promote financial inclusion and verify human uniqueness.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- To participate in the Worldcoin Airdrop Program, users must
- Obtain a World ID verified account
- Complete at least one form of verification—either Orb Verification or Passport Verification.
- Orb Verification
- Provides a high level of certainty that a user is a unique human and offers the highest amount of WLD tokens that a user can claim.
- Passport Verification
- Offers more convenience by verifying a passport as a credential in the World App but provides a lower level of certainty about the user’s uniqueness, resulting in fewer tokens than Orb Verification. This method is subject to eligibility and availability.
- Enroll in the airdrop
- Once verified, eligible users can sign up for the airdrop within the World App to see the amount of WLD they are eligible to claim.
- Be non-U.S. persons and not located in the U.S.
- The Airdrop Program is only available to World ID users who meet the eligibility requirements set forth in Worldcoin’s Terms and are not U.S. persons or located in the United States.
- Completing both Orb and Passport Verifications demonstrates the highest level of assurance that a user is a unique human, making them eligible to claim the largest token amount available when combined.

**Фактори:** anti_sybil_identity, claim_and_vesting.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Не автоматизувати дублікати особистостей; перевіряти правила адрес, кластерів, KYC і географії. Стежити за початком/кінцем claim, vesting, unlock і поверненням невитребуваних токенів.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/worldcoin/) · [Посилання з каталогу — потребує перевірки](https://support.world.org/hc/en-us/articles/16075438470547-When-can-I-start-claiming-WLD) · [Посилання з каталогу — потребує перевірки](https://support.world.org/hc/en-us/articles/22200067310739-How-much-WLD-can-I-claim) · [Посилання з каталогу — потребує перевірки](https://support.world.org/hc/en-us/articles/30969185598739-Updates-to-the-Airdrop-Program) · [Посилання з каталогу — потребує перевірки](https://worldcoin.org)

### 131. WalletConnect

**Дата:** 2024-11-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized communication protocol that connects wallets and dApps across multiple blockchain networks.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Users must meet the following minimum requirements to qualify
- Created a profile through
- airdrop.walletconnect.network
- Authenticated with at least one wallet using the WalletConnect Network.
- Demonstrated activity by making at least one connection or signature via WalletConnect before September 12, 2024.
- No linked addresses appearing in the OFAC SDN list.
- Additional eligibility is determined by a
- scoring system
- based on
- Network Activity
- Number of interactions, connections, and signatures via WalletConnect.
- On-Chain Presence
- Activity across Ethereum, BNB Smart Chain, Polygon, Avalanche, Arbitrum, Base, Linea, Optimism, zkSync Era, and Blast (evaluated between June 12 - September 12, 2024).
- Airdrop Behavior
- Users with a history of long-term holding receive up to a 5% bonus, while quick sellers may face an 80% reduction.
- Additional Allocations

**Фактори:** activity_diversity, nft_or_asset_holding, developer_contribution, ranking_or_tier.
**Обсяг:** 50M WCT tokens. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання. Фіксувати contract, collection, token ID, snapshot і мінімальний строк володіння. Зберігати PR, commit, deployment і прийнятий результат, а не лише факт активності.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/walletconnect/) · [Посилання з каталогу — потребує перевірки](https://airdrop.walletconnect.network) · [Посилання з каталогу — потребує перевірки](https://docs.walletconnect.network/airdrop-season-1/) · [Посилання з каталогу — потребує перевірки](https://walletconnect.com) · [Посилання з каталогу — потребує перевірки](https://x.com/WalletConnect) · [Посилання з каталогу — потребує перевірки](https://x.com/WalletConnect/status/1859225191580385728)

### 132. DexGuru

**Дата:** 2024-11-27 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Guru Network is a decentralized platform focused on creating a fair and transparent ecosystem for users, offering various applications and AI-powered tools to enhance user experience within the blockchain space.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Users must hold at least one of the following NFTs to be eligible for the initial sign-up reward
- Guru Season Passes
- Themed Guru NFTs (e.g., Spooky Guru)
- Guru Network DAO NFTs
- The reward amount is influenced by several factors
- Type of NFT Possessed
- Each type of NFT provides a multiplier that increases the reward amount. For example, Season Passes 1 and 2 have a multiplier of 2, while Themed collections and Guru DAO NFTs have a multiplier of 1. If users hold more than one type of NFT, the multipliers are combined.
- Governance Participation
- Users who participated in Guru Network Snapshot voting receive an additional reward of 200 GURU tokens.
- Accumulated Testnet Points
- Points accumulated during the testnet phase (e.g., Burns in Burning Meme, tGuru in Guru Network app) are converted into GURU tokens based on a conversion rate determined by the total value locked (TVL) ratio between mainnet and testnet.
- App-Specific Rewards
- Applications within the ecosystem may provide additional rewards based on app-specific criteria.
- The initial sign-up reward is calculated using the following formula
- Sign Up Reward = Base Sign Up Reward * Pass Multiplier + Governance Participation Reward + Accumulated Testnet Points * Conversion Rate + App-Specific Rewards
- Where

**Фактори:** snapshot_state, duration_consistency, capital_exposure, activity_diversity, points_quests, testnet_participation, nft_or_asset_holding, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/dexguru/) · [Посилання з каталогу — потребує перевірки](https://docs.gurunetwork.ai/getting-started/ultimate-guide-to-guru-network-for-community-users) · [Посилання з каталогу — потребує перевірки](https://gov.gurunetwork.ai/t/proposal-003-guru-ecosystem-incentivization-airdrop-mechanism/34) · [Посилання з каталогу — потребує перевірки](https://gurunetwork.ai) · [Посилання з каталогу — потребує перевірки](https://x.com/xgurunetwork/status/1859608300100182152)

### 133. Side Protocol

**Дата:** 2024-11-26 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A fully Bitcoin-compatible Layer 1 blockchain built on CometBFT and the Cosmos SDK.
**Статуси:** reported_alive_by_secondary_directory; claim_start_reported_by_secondary_source.

**Умови/дії:**

- Bitcoin Active Users
- Must have spent over 0.005 BTC
- in network fees between
- January 1, 2023 – November 1, 2024
- 30% of the total Genesis Drop allocated
- Cap
- 50,000 claimable addresses out of
- 764,909 eligible
- Each address can claim
- 600 SIDE
- tokens.
- NFT Communities
- 10.50% of the airdrop allocated.
- Covers NFT holders across
- Bitcoin, Cosmos, Solana, and Ethereum
- ecosystems.

**Фактори:** early_participation, snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 100,000,000 SIDE tokens. **Eligible:** 764,909 Bitcoin addresses identified in the snapshot (only Bitcoin category mentioned). **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/side-protocol/) · [Посилання з каталогу — потребує перевірки](https://discord.gg/sideprotocol) · [Посилання з каталогу — потребує перевірки](https://genesis.side.one) · [Посилання з каталогу — потребує перевірки](https://medium.com/%40SideProtocol/side-genesis-drop-3e0989d74628) · [Посилання з каталогу — потребує перевірки](https://side.one) · [Посилання з каталогу — потребує перевірки](https://t.me/SideProtocolOfficial) · [Посилання з каталогу — потребує перевірки](https://twitter.com/SideProtocol)

### 134. Piggy Superform

**Дата:** 2024-11-25 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A DeFi yield marketplace optimizing on-chain wealth by providing users access to diverse yield opportunities across multiple blockchains.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Users must have participated in the
- Superform Safari campaign
- , with a focus on
- Final Boosted Superform Safari XP
- and
- Community Score
- as key metrics for distribution (measured via Guild).
- Users who
- remained deposited
- during the
- Find My Frens event (Nov 7 - Nov 21, 2024)
- received additional PIGGY through a bonus allocation modifier.
- No team, VC, or insider allocations
- —100% of tokens are for the community.
- Claim Process
- Visit

**Фактори:** snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 69,000,000,000 PIGGY. **Eligible:** невідомо. **Claimants:** 178 (as of initial collection data).
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/piggy-superform/) · [Посилання з каталогу — потребує перевірки](https://basescan.org/address/0xe3CF8dBcBDC9B220ddeaD0bD6342E245DAFF934d) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/superform.eth/hOj0XuCCurUYQXpXVFwFs7rWSC_0FmCHTVy0x2a2i5c) · [Посилання з каталогу — потребує перевірки](https://www.superform.xyz/) · [Посилання з каталогу — потребує перевірки](https://www.superform.xyz/piggy/claim/) · [Посилання з каталогу — потребує перевірки](https://x.com/superformxyz/status/1861092778408865956)

### 135. Sui Name Service (SuiNS)

**Дата:** 2024-11-14 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** SuiNS is a decentralized name service protocol on Sui, providing human-readable names for Sui addresses and enabling on-chain governance through the NS token.
**Статуси:** reported_alive_by_secondary_directory; claimants_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Must hold a SuiNS (NS) Airdrop NFT (distributed to 183,369 eligible users)
- NFT airdrop targeted at community members who actively contributed to or interacted with SuiNS services
- NFT can be unwrapped for NS tokens at TGE via the claim site
- Additional Airdrop Opportunities
- Future governance rewards: 5% of total supply allocated to users who participate in on-chain voting
- Additional community engagements and treasury distributions may be proposed and voted on by NS holders
- Claim Process
- Claim site
- claim.suins.io
- (opens 2024-11-14 at 10:55am UTC)
- Users connect wallet and claim NS tokens by unwrapping their SuiNS Airdrop NFT
- Claim site will be shared publicly on TGE day for a smooth experience
- Special Conditions
- Only SuiNS Airdrop NFT holders are eligible for the initial airdrop
- Governance rewards distributed to users who vote on proposals, proportional to voting power and participation

**Фактори:** snapshot_state, duration_consistency, capital_exposure, nft_or_asset_holding, community_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 50,000,000 NS (10% of total supply, community airdrop). **Eligible:** 183,369 (Airdrop NFT holders). **Claimants:** Not specified.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/suins/) · [Посилання з каталогу — потребує перевірки](http://claim.suins.io) · [Посилання з каталогу — потребує перевірки](https://suins.io/) · [Посилання з каталогу — потребує перевірки](https://token.suins.io/) · [Посилання з каталогу — потребує перевірки](https://x.com/SuiNSdapp/status/1821923674196148480) · [Посилання з каталогу — потребує перевірки](https://x.com/SuiNSdapp/status/1853861215161766297) · [Посилання з каталогу — потребує перевірки](https://x.com/SuiNSdapp/status/1854584664633032903)

### 136. Supra

**Дата:** 2024-11-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A vertically integrated Layer 1 blockchain platform offering oracles, verifiable randomness, automation, bridges, and multiple virtual machines.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Account Registration and KYC Verification
- Sign up on the official Supra website (
- supra.com
- ) or the designated airdrop page. Completing Know Your Customer (KYC) verification is typically required to ensure compliance with regulatory standards and confirm eligibility.
- Wallet Requirements
- A compatible cryptocurrency wallet is necessary, such as the StarKey wallet recommended by Supra for claiming tokens. Connecting your wallet to the Supra platform may be required to facilitate token distribution. Ensure the wallet is active and not newly created, as some airdrops exclude brand-new wallets to prevent abuse.
- Community Engagement and Tasks
- Participation in community activities is often a key criterion. This can include completing specific tasks like joining Supra’s social media channels (e.g., Twitter, Telegram, or Discord), sharing content, or referring friends. Tasks might reward you with “Stars” or points, which can later be redeemed for SUPRA tokens. The more tasks you complete, the higher your potential rewards.
- Token Holding Requirements (if applicable)
- Some phases of the Supra airdrop may require holding a minimum amount of specific tokens, such as GateTokens (GT). For instance, holding at least 10 GT and maintaining an average of 10 GT throughout the campaign has been mentioned in certain contexts. However, this may not apply to all participants or phases.
- Geographic Eligibility
- Participation is generally open globally, but regulatory restrictions may exclude residents of certain countries (e.g., the USA or China in some cases). It’s advisable to check the official airdrop page for an updated list of excluded regions.
- Gas Fee Preparation
- To claim tokens, a small amount of SUPRA may be needed in your wallet to cover gas fees. This can be obtained from exchanges like KuCoin, Bybit, or Gate.io and sent to your StarKey wallet.
- Timing and Activity Level
- The airdrop often rewards early or active participants. For instance, the first 500,000 users to join might receive a larger allocation (e.g., 350 SUPRA tokens via community goals). Completing weekly missions or expeditions (e.g., educational quizzes or trading games) can also increase your rewards.

**Фактори:** early_participation, duration_consistency, real_product_usage, activity_volume, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, anti_sybil_identity, claim_and_vesting.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/supra/) · [Посилання з каталогу — потребує перевірки](https://hub.supra.com/supraspartans) · [Посилання з каталогу — потребує перевірки](https://supra.com) · [Посилання з каталогу — потребує перевірки](https://supra.com/blastoff/token-claim/en) · [Посилання з каталогу — потребує перевірки](https://supra.com/news/countdown-to-blast-off-airdrop-updates/)

### 137. Swell Network

**Дата:** 2024-11-07 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Swell is a leading L2 restaking protocol offering native liquid staking and restaking for Ethereum and Bitcoin. It enables governance and infrastructure security via restaking protocols like EigenLayer and Symbiotic.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility was determined based on participation in the Swell Voyage campaign.
- Users earned “White Pearls” based on their staking and liquidity provision.
- 7% of the total SWELL allocation was distributed linearly based on White Pearls.
- An additional 1.5% was distributed as a Loyalty Bonus to the most dedicated users.
- Users with less than 10 White Pearls were not eligible for the Loyalty Bonus.
- Anti-sybil measures were implemented to prevent manipulation.
- Top 250 wallets were subject to vesting conditions.

**Фактори:** early_participation, capital_exposure, points_quests, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 850,000,000 SWELL (8.5% of total supply) allocated to the Voyage campaign. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/swell-network/) · [Посилання з каталогу — потребує перевірки](https://app.swellnetwork.io/dao/voyage) · [Посилання з каталогу — потребує перевірки](https://www.swellnetwork.io) · [Посилання з каталогу — потребує перевірки](https://www.swellnetwork.io/post/swell-token) · [Посилання з каталогу — потребує перевірки](https://x.com/swellnetworkio/status/1854449625606001044)

### 138. NX Finance

**Дата:** 2024-11-01 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A yield layer on Solana offering leveraged strategies for enhanced returns.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- To qualify for the Season 1 airdrop, participants were required to
- Deposit and Leverage Assets
- Users needed to deposit assets such as SOL, vSOL, or JLP tokens into NX Finance’s vaults (e.g., Lending Vault or Leverage Vault) and utilize leveraged strategies. For example, lending $1 worth of assets might have earned users a set number of points per day (e.g., 3 points/day in past seasons)
- Total Value Locked (TVL) Points
- Points were awarded based on the amount and duration of assets deposited or lent. The more deposited and leveraged, the higher the points, which determined airdrop eligibility or allocation
- Staking NX Tokens
- Holding and staking NX tokens was a requirement or a booster for airdrop rewards. For instance, staking NX provided a 50% boost to points earned in subsequent airdrop seasons (e.g., Season 2)
- Referral System
- Users could earn additional points by referring others to the platform. Each participant received a unique referral code upon joining, and referring friends granted bonus points (e.g., 10% of the points earned by referred users in some campaigns)
- Team Participation
- Joining or creating a team within the “Nadventure” campaign enhanced rewards. Teams pooled efforts, and collective deposits increased individual point totals, impacting airdrop eligibility
- Active Engagement
- Interacting with NX Finance’s ecosystem, such as using their strategies (e.g., 10x leverage on JLP or farming points for other Solana projects like Jupiter or Kamino), contributed to eligibility. Historical activity was also considered for retroactive airdrops
- Wallet Connection
- A Solana-compatible wallet (e.g., Phantom or Backpack) needed to be connected to the NX Finance platform to participate, claim points, or receive tokens
- The claim period ended on November 30, 2024, with unclaimed NX tokens burned

**Фактори:** duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, developer_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома. Повний обсяг роздачі невідомий.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/nx-finance/) · [Посилання з каталогу — потребує перевірки](https://nx-finance.gitbook.io/nx-finance-whitepaper/welcome-to-nx-finance/airdrop) · [Посилання з каталогу — потребує перевірки](https://x.com/NX_Finance/status/1849782971479519637)

### 139. Kroma

**Дата:** 2024-10-30 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A Layer 2 solution built on the Superchain, leveraging OP Stack rollup with an active fault-proof system utilizing zkEVM. Kroma aims to transition into a universal ZK Rollup for improved scalability and cost-efficiency.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility is based on multiple contribution categories
- Ownership of SBTs/NFTs (Mixed Types)
- Owning 2 kinds of SBTs/NFTs: 250 KRO
- Owning 3 kinds: 750 KRO
- Owning all 4 kinds: 1,500 KRO
- Specific Trophy NFTs
- Diamond Trophy NFT: 250 KRO
- Gold Trophy NFT: 200 KRO
- Silver Trophy NFT: 150 KRO
- Bronze Trophy NFT: 50 KRO
- Conqueror NFT: 50 KRO per NFT
- Kroma Quest and Galxe Points
- Owning Kroma Quest Master NFT: 500 KRO per KQM NFT
- Having more than 100 Galxe points: 1 KRO per 5 points over 100
- Having more than 540 Galxe points: 10 KRO per 5 points over 540
- WCP (Wrapped Crypto Points)

**Фактори:** snapshot_state, real_product_usage, capital_exposure, activity_diversity, points_quests, nft_or_asset_holding, community_contribution, ranking_or_tier.
**Обсяг:** 49,150,177.42 KRO (5% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/kroma/) · [Посилання з каталогу — потребує перевірки](https://blog.kroma.network/kromas-first-airdrop-a-token-of-appreciation-for-our-community-65f8acaf8776) · [Посилання з каталогу — потребує перевірки](https://kcu.kroma.network/?dialog=airdrop) · [Посилання з каталогу — потребує перевірки](https://kroma.network) · [Посилання з каталогу — потребує перевірки](https://x.com/kroma_network/status/1849345785496006732) · [Посилання з каталогу — потребує перевірки](https://x.com/kroma_network/status/1851429690395034053)

### 140. The Arena

**Дата:** 2024-10-29 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** The Arena is a SocialFi platform on the Avalanche blockchain that integrates social engagement with financial opportunities. It rewards users with $ARENA tokens based on platform activity and governance participation.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- X (Twitter) Account Login
- Users must log in to The Arena platform via their X (Twitter) account.
- Profile Completion
- A profile bio and picture must be added.
- Avalanche Wallet Connection
- Users must connect an AVAX-compatible wallet with AVAX tokens for gas fees.
- Activity-Based Engagement
- Points are earned through engagement, including liking, commenting, creating content, tipping, trading, and referral activity.
- Referral System
- Additional points are granted for successful referrals.
- Weekly Distribution
- Points are typically distributed every Monday at 2:00 PM EST.
- Claiming Process
- Users receive an initial 15% of allocated tokens at launch.
- The remaining 85% is distributed monthly over 12 months.
- Continued activity is required for future claims

**Фактори:** duration_consistency, activity_volume, capital_exposure, points_quests, community_contribution, referrals, claim_and_vesting, ranking_or_tier.
**Обсяг:** 2.56 billion $ARENA (initially allocated for distribution). **Eligible:** Over 100,000 users. **Claimants:** невідомо.
**Урок:** Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/the-arena/) · [Посилання з каталогу — потребує перевірки](https://arena.social/) · [Посилання з каталогу — потребує перевірки](https://medium.com/@TheArena_App/arena-is-coming-22fa6f6ee010) · [Посилання з каталогу — потребує перевірки](https://x.com/TheArenaApp/status/1851405478930116918)

### 141. Talent Protocol

**Дата:** 2024-10-29 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized protocol designed to help crypto builders gain recognition and rewards based on verifiable reputation data.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- The $TALENT Summer Airdrop rewards early adopters and active members of the Talent Protocol ecosystem. Eligibility is determined by three main categories
- Talent Protocol OG Members
- (5 different criteria)
- Ecosystem Members
- (12 different criteria)
- $TALENT Community Round Participants
- Each category is independent, meaning an address can qualify under multiple categories and receive a combined allocation accordingly.
- Additionally
- No vesting or lock-up periods apply to airdropped tokens.
- Community Round participants can increase their allocation by purchasing $TALENT tokens.
- Builderdrop
- Join the Community Round
- Purchase a ticket to access Builderdrop and receive an initial $TALENT allocation.
- Boost Your Builder Score
- Earn more tokens by increasing your Builder Score before the snapshot.
- Receive a Builder Bonus

**Фактори:** early_participation, snapshot_state, activity_diversity, points_quests, community_contribution, developer_contribution, anti_sybil_identity, claim_and_vesting, ranking_or_tier.
**Обсяг:** 10,000,000 $TALENT tokens. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Покривати кілька справжніх функцій продукту, якщо правила прямо винагороджують ширину використання.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/talent-protocol/) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/talentprotocol.eth/nmvM9HDRHuBox9nZh0RBREc-qA6BL1T6WWEdCrHTynQ) · [Посилання з каталогу — потребує перевірки](https://talentprotocol.com) · [Посилання з каталогу — потребує перевірки](https://x.com/TalentProtocol)

### 142. Grass

**Дата:** 2024-10-28 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** Поіменне історичне досьє з матеріалами про умови та подію винагороди.
**Статуси:** source_checked_historical_product; completed_program_reported.

**Умови/дії:**

- Розподіл за points і дев’ятьма рівнями, окремо GigaBuds та Desktop/Saga.
- Прив’язка гаманця до 14.10.2024 20:00 UTC.
- Документ містить неоднозначність >500 проти 500+ points;
- точний оператор потребує додаткового доказу.

**Фактори:** points_quests.
**Обсяг:** невідомо. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Не нормалізувати суперечливі оператори порога мовчки. Фіксувати час прив’язки гаманця та завершення claim окремо.

**Прогалини:** Незалежний перерахунок переказів і фінальних одержувачів не виконано. Витрати учасників і поточну працездатність продукту окремо не перевірено.

**Джерела:** [Джерело 1](https://grass-foundation.gitbook.io/grass-docs/introduction/grass-airdrop-one)

### 143. AlienX

**Дата:** 2024-10-23 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized AI-powered blockchain network designed for scalability, governance, and AI-node incentives.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligible users for the airdrop include
- AI Node Holders
- (Network rewards and node incentives)
- Staking Pre-Season Participants
- Social Airdrop Participants
- AGP & AEP Holders
- HAL Testnet Quest Participants
- Mainnet Voyage Supreme NFT Holders
- Mainnet Voyage Participants
- AlienSwap Campaign Participants
- (Phase 1)
- AlienSwap Score Holders
- (Phase 2)
- AlienSwap ALIENX Points Holders
- (Phase 3)
- ALIENX Pets Telegram Bot Participants

**Фактори:** early_participation, snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, testnet_participation, node_validator_work, nft_or_asset_holding, community_contribution, ranking_or_tier.
**Обсяг:** 98,800,000 AIX (out of 125,000,000 TGE release). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/alienx/) · [Посилання з каталогу — потребує перевірки](https://alienxchain.io) · [Посилання з каталогу — потребує перевірки](https://alienxchain.io/claim-aix) · [Посилання з каталогу — потребує перевірки](https://mirror.xyz/0xA1e3989D59ECCE840c64286B19D50F319b50a82f/HdaSSaC4SWkjuBPm5E4zQQTijzOyFcqy-xnhb7ZrkU4) · [Посилання з каталогу — потребує перевірки](https://x.com/ALIENXchain/status/1845441702800261399)

### 144. Scroll

**Дата:** 2024-10-22 (exact_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** A decentralized rollup platform focused on scalable and secure blockchain infrastructure.
**Статуси:** source_checked_historical_product; completed_program_reported.

**Умови/дії:**

- Scroll’s first airdrop was announced on October 19, 2024, with a snapshot taken at 00:00 UTC that day. It distributed 7% of the total SCR token supply (1 billion tokens) to reward early contributors and community members. Here’s how eligibility worked
- Scroll Sessions Program (Marks System)
- Users earned “Marks” by participating in on-chain activities within the Scroll ecosystem during Session 1.
- A minimum of 200 Marks was required to qualify for the airdrop.
- Out of 5.5% of the supply (55 million SCR), 4% was allocated to users with 200+ Marks, rewarding active participation.
- Over 570,000 wallets qualified, with the majority being active contributors who accumulated Marks.
- On-Chain Activity
- Bridging assets (e.g., ETH or wstETH) from Ethereum mainnet to Scroll Layer-2 using the official Scroll bridge or recommended bridges like Rhino.fi.
- Interacting with decentralized applications (dApps) on Scroll, such as providing liquidity on DeFi platforms (e.g., Ambient, Aave), swapping tokens, or minting NFTs like the Scroller NFT.
- Holding assets on Scroll over time increased Marks, with boosts for specific actions like using smart contract wallets.
- Community and Ecosystem Contributions
- Beyond regular users, rewards went to developers building on Scroll, researchers, event organizers, and global community members who supported Ethereum’s ecosystem.
- Specific allocations weren’t tied to Marks but to contributions like TVL (total value locked) in projects or hackathon participation.
- Additional Airdrop Allocations
- Flat Boost
- 1% of total supply equally distributed among all eligible on-chain participants.

**Фактори:** early_participation, snapshot_state, real_product_usage, capital_exposure, activity_diversity, nft_or_asset_holding, community_contribution, developer_contribution, claim_and_vesting, ranking_or_tier.
**Обсяг:** 70,000,000 SCR (7% of total supply). **Eligible:** Over 570,000 wallets. **Claimants:** невідомо.
**Урок:** Не переносити bonus-умови на основну eligibility; відстежувати завершення claim.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано.

**Джерела:** [Джерело 1](https://chain.scroll.io/blog/introducing-scrolls-first-airdrop-a-celebration-of-the-global-community) · [Джерело 2](https://claim.scroll.io/?lang=en-US) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/scroll/) · [Посилання з каталогу — потребує перевірки](https://scroll.io) · [Посилання з каталогу — потребує перевірки](https://scroll.io/blog/introducing-scrolls-first-airdrop-a-celebration-of-the-global-community) · [Посилання з каталогу — потребує перевірки](https://scroll.io/blog/scr-token)

### 145. deBridge

**Дата:** 2024-10-17 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A cross-chain interoperability protocol designed to enable seamless asset transfers and messaging between blockchains.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Users eligible for the airdrop must have obtained points through the deBridge points program before the snapshot date. Eligible participants include
- Users who earned points through cross-chain bridging activity on deBridge and its integration partners.
- Referral points granted to active community members and integration partners.
- Solvers who initiated unlock messages on deBridge Liquidity Network (DLN) after providing liquidity.
- Users and projects utilizing deBridge’s cross-chain asset custody solution (dePort).
- LPs to deSwap v1 pools on Curve before the transition to a zero TVL model.
- Messaging referral points granted to projects and addresses referring users for deBridge messaging.
- IaaS subscription initiators.
- Unclaimed tokens may be used for future airdrops or related activities.

**Фактори:** snapshot_state, real_product_usage, capital_exposure, points_quests, community_contribution, referrals, claim_and_vesting.
**Обсяг:** 6% of DBR supply (600,000,000 DBR). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/debridge/) · [Посилання з каталогу — потребує перевірки](https://debridge.finance/) · [Посилання з каталогу — потребує перевірки](https://debridge.finance/learn/blog/debridge-introduces-dbr/) · [Посилання з каталогу — потребує перевірки](https://debridge.foundation) · [Посилання з каталогу — потребує перевірки](https://docs.debridge.foundation/)

### 146. Puffer Finance

**Дата:** 2024-10-14 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Puffer Finance is a decentralized Ethereum infrastructure protocol focused on liquid restaking (LRT) and preconfirmation services, including Puffer UniFi and UniFi AVS.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Primary Requirements
- Users must have participated in the
- Crunchy Carrot Quest Season One
- campaign
- A snapshot of eligible users was taken on
- October 5, 2024
- 50% of the airdrop is available immediately
- Remaining 50% vests over 6 months for larger depositors
- Additional Airdrop Opportunities
- Exchange Airdrops
- Binance Alpha Airdrop
- Users with ≥ 186 Alpha Points received 362 PUFFER tokens
- Users with 147-185 Alpha Points and UIDs ending in 5 received 362 PUFFER tokens
- Distribution date: May 12, 2024
- Additional Notes
- Total PUFFER Supply: 1,000,000,000 tokens

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, points_quests, nft_or_asset_holding, claim_and_vesting.
**Обсяг:** 75 million PUFFER (7.5% of total supply). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/puffer-finance/) · [Посилання з каталогу — потребує перевірки](https://claims.puffer.fi) · [Посилання з каталогу — потребує перевірки](https://medium.com/puffer-fi/puffer-tokenomics-utility-c789352629e6) · [Посилання з каталогу — потребує перевірки](https://quest.puffer.fi) · [Посилання з каталогу — потребує перевірки](https://www.puffer.fi/) · [Посилання з каталогу — потребує перевірки](https://x.com/binance/status/1921849600484294946) · [Посилання з каталогу — потребує перевірки](https://x.com/puffer_finance)

### 147. DeepBook

**Дата:** 2024-10-14 (secondary_directory_catalog_date). **Докази:** `primary_source_checked_partial`.
**Проєкт:** DeepBook is Sui’s first native liquidity layer, designed to provide wholesale liquidity for DeFi applications. It facilitates seamless transactions, incentivizes liquidity provision, and supports governance within its trading pools.
**Статуси:** source_checked_historical_product; live_claim_program.

**Умови/дії:**

- Users who received a
- DBClaimNFT
- March 28, 2024
- , were eligible.
- NFTs were distributed to ~100,000 early adopters based on
- Early interaction with DeepBook or the Sui ecosystem (e.g., trading on DeepBook’s order book, providing liquidity on DEXs like Cetus or Turbos).
- Staking SUI tokens or holding assets on Sui since
- January 2024
- (speculated but not fully detailed in the official release).
- Claim process
- NFT holders unwrapped tokens at
- claim.deepbook.tech
- starting
- October 14, 2024
- , with no vesting.

**Фактори:** early_participation, snapshot_state, activity_volume, capital_exposure, activity_diversity, nft_or_asset_holding, claim_and_vesting.
**Обсяг:** 1,000,000,000 DEEP (10% of total supply). **Eligible:** ~100,000 early adopters (DBClaimNFT recipients). **Claimants:** невідомо.
**Урок:** NFT-посвідчення майбутньої винагороди не дорівнює отриманому fungible-токену.

**Прогалини:** Незалежний підрахунок усіх переказів і фактичних витрат не виконано. Повний відбір NFT-одержувачів та фінальні погашення.

**Джерела:** [Джерело 1](https://www.sui.io/blog/deepbook-deep-token-launch) · [Джерело 2](https://www.sui.io/blog/deepbook-version3-deep-token) · [Джерело 3](https://www.sui.io/blog/deep-token-deepbook-governance) · [Crypto Airdrop Archive](https://airdroparchive.com/projects/deepbook/) · [Посилання з каталогу — потребує перевірки](https://blog.sui.io/deepbook-deep-token-launch/) · [Посилання з каталогу — потребує перевірки](https://claim.deepbook.tech) · [Посилання з каталогу — потребує перевірки](https://deepbook.tech/deep-token)

### 148. Carv.io

**Дата:** 2024-10-11 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** CARV is a decentralized AI-powered data network that prioritizes user sovereignty and digital identity.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Carv.io (CARV) airdrop was based on the following requirements
- Minting a CARV ID
- Create a CARV ID (self-sovereign digital identity) by connecting a Web3 wallet and minting on supported chains (opBNB, Ronin, zkSync, or Linea).
- Pay a small gas fee (e.g., ~0.02 BNB on opBNB).
- Active Participation in the Ecosystem
- Engage in CARV’s gaming platform (Infinite Play Participation).
- .Play Name Service: Shorter .play names and active users receive higher rewards.
- Link Steam, Twitter, Discord, and wallets to increase $SOUL mining rate and airdrop eligibility.
- Log in daily to mine $SOUL tokens via the CARV platform.
- Snapshot Eligibility
- Snapshot for Season 1 was taken on October 1, 2024 (00:00 AM UTC).
- Eligibility based on participation in the Loyalty Program, Infinite Play, and holding specific assets (e.g., .Play Name Service NFTs, CARV Nodes).
- Holding Specific Assets
- Owning CARV or partnered nodes (e.g., Aethir nodes) qualifies users for the airdrop.
- Holders of Play Name Service, Dragon Treasure NFTs, or other CARV ecosystem NFTs may be eligible.
- veCARV holders from the Loyalty Program or key contributors (KOLs, partners) with vested CARV (veCARV) were included in Season 1.

**Фактори:** snapshot_state, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, node_validator_work, nft_or_asset_holding, community_contribution, referrals, anti_sybil_identity, claim_and_vesting.
**Обсяг:** 40 million CARV (for Season 1). **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Вести часові ряди балансу й ролей; одна транзакція перед snapshot може не пройти фільтри. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/carv.io/) · [Посилання з каталогу — потребує перевірки](https://carv.io) · [Посилання з каталогу — потребує перевірки](https://medium.com/%40Carv/carv-s1-airdrop-frequently-asked-question-a10a73757706) · [Посилання з каталогу — потребує перевірки](https://x.com/carv_official/status/1844206212180738472)

### 149. Thruster

**Дата:** 2024-10-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** A decentralized liquidity and governance platform integrated with Blast, enabling users to earn and vote on emissions through veToken mechanics.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- To qualify for the THRUST airdrop, users must have
- Provided liquidity in eligible and productive pools on Thruster
- Traded either WETH or USDB tokens into an eligible pool on Thruster
- Participated in sponsored credits campaigns on Thruster
- Passed Sybil resistance checks

**Фактори:** activity_volume, capital_exposure, points_quests, anti_sybil_identity.
**Обсяг:** 35,000,000 THRUST (7% of total supply). **Eligible:** >135,000 users. **Claimants:** невідомо.
**Урок:** Оптимізувати чисту корисність після fees; не створювати wash-volume або штучні цикли. Встановити ліміт капіталу, строку та ризику; рахувати impermanent loss, slashing і зміну ціни. Зберігати season, формулу points, mandatory/bonus дії та версію правил.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/thruster/) · [Посилання з каталогу — потребує перевірки](https://app.thruster.finance/credits) · [Посилання з каталогу — потребує перевірки](https://blog.thruster.finance/Introducing-THRUST-ffd9f3c7897d4cfdae9c1d8e722f2bb5) · [Посилання з каталогу — потребує перевірки](https://foundation.thruster.finance) · [Посилання з каталогу — потребує перевірки](https://thruster.finance) · [Посилання з каталогу — потребує перевірки](https://x.com/ThrusterFi/status/1843924366540845296)

### 150. Fyde

**Дата:** 2024-10-09 (secondary_directory_catalog_date). **Докази:** `secondary_directory_screened`.
**Проєкт:** Fyde is a decentralized finance platform offering liquid staking and yield optimization through its Liquid Vault and additional financial products.
**Статуси:** reported_alive_by_secondary_directory; reward_event_reported_by_secondary_source.

**Умови/дії:**

- Eligibility for the Fyde ($FYDE) airdrop was based on the following requirements
- Liquid Vault Participation
- Users who deposited and staked assets in the Fyde Liquid Vault were eligible.
- Allocation was based on deposit size and staking duration, with a cap of 5% of the total airdrop amount per user.
- Community Engagement
- Discord Activity: Earned 0.5% of the airdrop allocation based on a points system (minimum post requirement, non-deleted comments).
- Zealy Quests: Participation in Zealy campaigns contributed 0.25% of the airdrop allocation.
- Telegram Mini App: Engagement in the Telegram Mini App was rewarded with 0.25% of the airdrop allocation, with a per-user cap of 0.01%.
- Eligibility Periods
- The airdrop was split into two phases
- Phase 1 (OG Members): Ended January 2, 2024, rewarding early depositors.
- Phase 2 (Growth Phase): Continued beyond this date, with rewards based on product usage.
- Vesting
- 30-day linear vesting schedule to mitigate sell pressure.

**Фактори:** early_participation, duration_consistency, real_product_usage, capital_exposure, activity_diversity, points_quests, community_contribution, claim_and_vesting.
**Обсяг:** 7% of the total $FYDE token supply. **Eligible:** невідомо. **Claimants:** невідомо.
**Урок:** Заходити після перевірки офіційного домену; зберігати першу дату взаємодії та tx hash. Розподіляти реальні дії по тижнях/епохах і не пропускати активні фази. Використовувати основну функцію продукту природно та зберігати маршрут, актив, мережу й результат.

**Прогалини:** Запуск, правила та перекази не звірені з усіма першоджерелами. Кількість фактичних одержувачів невідома.

**Джерела:** [Crypto Airdrop Archive](https://airdroparchive.com/projects/fyde/) · [Посилання з каталогу — потребує перевірки](https://app.fyde.fi) · [Посилання з каталогу — потребує перевірки](https://app.fyde.fi/verify-airdrop) · [Посилання з каталогу — потребує перевірки](https://docs.fyde.fi/overview/usdfyde-season-2-airdrop) · [Посилання з каталогу — потребує перевірки](https://game.fyde.fi)
