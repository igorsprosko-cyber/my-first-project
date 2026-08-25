# SITE MAP

Версия: 1.2

Этот документ фиксирует фактическую структуру темы InSales после анализа репозитория `main` и текущего рабочего стандарта V2.3.

## 1. Карта шаблонов

| Шаблон | Назначение |
|---|---|
| `templates/layouts.layout.liquid` | основной layout сайта |
| `templates/layouts.checkout2.liquid` | layout оформления заказа |
| `templates/layouts.client_account.liquid` | layout личного кабинета |
| `templates/index.liquid` | главная страница |
| `templates/collection.liquid` | каталог/коллекция |
| `templates/product.liquid` | карточка товара |
| `templates/cart.liquid` | корзина |
| `templates/search.liquid` | поиск |
| `templates/compare.liquid` | сравнение товаров |
| `templates/favorite.liquid` | избранное |
| `templates/page.liquid` | обычные информационные страницы |
| `templates/page_404.liquid` | страница 404 |
| `templates/blog.liquid` | список записей блога |
| `templates/article.liquid` | отдельная запись блога |
| `templates/shared_cart.liquid` | общая корзина |

## 2. Системные Liquid-включения

- `snippets/head.liquid` — meta, canonical, title/description, Schema.org и системные SEO-включения.
- `snippets/styles.liquid` — подключение стилей.
- `snippets/system_*` — системные включения InSales, вызываемые из темы.

## 3. CSS-карта

Пользовательский CSS нельзя считать сосредоточенным только в `media/theme.scss`: в шаблонах также присутствуют inline `<style>`-блоки, которые являются частью фактического каскада.

Известные inline CSS-поверхности включают:

- `templates/cart.liquid`;
- `templates/collection.liquid`;
- `templates/product.liquid`;
- `templates/article.liquid`;
- другие шаблоны с inline `<style>`.

В рабочем стандарте V2.3 дополнительно зафиксировано, что системные InSales-виджеты могут генерировать собственные DOM-элементы уже после загрузки шаблона. Поэтому CSS-аудит должен учитывать одновременно:

1. общий `theme.scss`;
2. inline CSS конкретного шаблона;
3. CSS/стили системного виджета;
4. фактический DOM и Computed Style на живой странице.

Нельзя исправлять конфликт только по имени предполагаемого класса.

## 4. JavaScript-карта

`theme.js` является рабочим общим слоем V2.3 для задач стандартизации, которые должны применяться сразу к нескольким страницам.

Текущая рабочая версия учитывает:

- same-origin навигацию;
- корректировку известных внутренних URL;
- footer-каталог;
- восстановление Hero на главной без изменения эталонного `V2.1_HOME_APPEND.liquid`;
- визуальную нормализацию `add-cart-counter` на всех страницах, где его рендерит InSales.

Inline JavaScript остаётся в Liquid-шаблонах, в частности:

- `templates/index.liquid` — обработчики hero/request/calculator;
- `templates/layouts.layout.liquid` — код `DOMContentLoaded`, включая SEO/A11Y-преобразования;
- `templates/product.liquid` — локальные обработчики страницы товара;
- `templates/cart.liquid` — логика НДС/инвойса и динамических элементов корзины.

Следовательно, фактический JS-аудит должен учитывать и общий `theme.js`, и inline `<script>` в Liquid-шаблонах.

## 5. Карта виджетов

Тема использует стандартные InSales widget-механизмы и системные виджеты.

CSS-классы дают только частичное представление о них.

Авторитетным источником конкретного инвентаря остаётся `config/setup.json`, где находится `theme_widgets.widget_lists`.

Для runtime-проблем обязательна проверка реального DOM системного виджета.

## 6. Карта компонентов

На текущем этапе компоненты логически группируются так:

- Header / navigation;
- Search;
- Catalog;
- Product card;
- Product page;
- Cart;
- Checkout;
- Customer account;
- Compare;
- Favorites;
- Blog / article;
- Footer;
- SEO / Schema;
- InSales system widgets.

Это логическая карта, а не разрешение создавать новые файлы. Физическое выделение компонентов выполняется только отдельной задачей после анализа существующих повторов.

## 7. V2.3 standardization baseline

Рабочая тестовая ветка:

`insales-test-copy:v2.3-page-standardization`

Синхронизированный проверенный набор:

- `product.liquid`;
- `cart.liquid`;
- `theme.js`;
- `theme.scss`.

Эталон главной страницы:

`V2.1_HOME_APPEND.liquid`.

Эталон не изменяется ради стандартизации остальных страниц.

## 8. Найденные технические особенности

### SEO

`snippets/head.liquid` уже содержит canonical, title/description и Organization JSON-LD. Поэтому следующий этап SEO должен начинаться с аудита существующей реализации, а не с создания второй Schema/SEO-системы.

### CSS

`theme.scss` содержит глобальные селекторы и `!important`. Особенно опасны широкие селекторы для `.button`, `.btn`, widget-ссылок и других общих классов. Любое изменение таких правил требует проверки фактического DOM компонентов, на которые они распространяются.

### JavaScript

Нельзя считать пользовательский JS отсутствующим только потому, что логика распределена между `theme.js` и inline `<script>` в Liquid-шаблонах.

### Конфигурация

`config/settings.json`, `config/settings_data.json`, `config/setup.json` являются источниками конфигурации темы. Их нельзя менять без отдельной задачи.

## 9. Правило runtime-диагностики

Если визуальная проблема сохраняется после изменения общего CSS/JS, следующий шаг — не новый патч, а фактическая трассировка:

`DOM → класс/структура → Computed Style → источник CSS/JS → сравнение с main → точечное исправление`.

Это обязательное правило для дальнейшей стабилизации V2.3.
