# SITE MAP

Версия: 1.1

Этот документ фиксирует фактическую структуру темы InSales после анализа репозитория `main`.

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

- `templates/cart.liquid:1`;
- `templates/collection.liquid:7`;
- `templates/product.liquid:2`;
- `templates/article.liquid:94`;
- другие шаблоны с inline `<style>`.

`media/theme.scss` содержит общие пользовательские стили, включая:

1. настройки редактора InSales;
2. шапку и мобильную боковую панель;
3. логотип и навигацию;
4. поиск;
5. подвал;
6. SEO-скрытие дублирующего H1;
7. ссылки, стилизованные как кнопки категорий;
8. резервный класс `.vl-category-btn`.

Поэтому полный CSS-аудит должен учитывать как `media/theme.scss`, так и inline CSS в Liquid-шаблонах. Нельзя объявлять CSS-карту полной, пока эти источники не проверены.

## 4. JavaScript-карта

`media/theme.js` существует, но сейчас пустой. Это **не означает отсутствия пользовательской JavaScript-логики**.

Inline JavaScript уже присутствует, в частности:

- `templates/index.liquid` — обработчики hero/request/calculator;
- `templates/layouts.layout.liquid` — код, запускаемый через `DOMContentLoaded`, включая SEO/A11Y-преобразования;
- `templates/product.liquid` — обработчики управления элементами карточки товара.

Следовательно, фактический JS-аудит должен учитывать inline `<script>` в Liquid-шаблонах наряду с `media/theme.js`. Нельзя создавать вторую JS-архитектуру или считать пользовательский JS отсутствующим только потому, что `media/theme.js` пуст.

## 5. Карта виджетов

По текущей структуре тема использует стандартные InSales widget-механизмы и системные виджеты. CSS-классы дают только частичное представление о них.

Авторитетным источником конкретного инвентаря является `config/setup.json`, где находится `theme_widgets.widget_lists`. Например, в конфигурации присутствуют записи с handle вроде `article-list` и другие системные/тематические виджеты.

Поэтому статус widget map должен оставаться **частичным**, пока `config/setup.json` не проанализирован полностью. Нельзя объявлять карту виджетов завершённой на основании только CSS-селекторов.

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

## 7. Найденные технические особенности

### SEO

`snippets/head.liquid` уже содержит canonical, title/description и Organization JSON-LD. Поэтому следующий этап SEO должен начинаться с аудита существующей реализации, а не с создания второй Schema/SEO-системы.

### CSS

`media/theme.scss` содержит много глобальных селекторов и несколько блоков с `!important`. Особенно широкий селектор для ссылок виджетов (`.widget-type_text a`, `.widget-type_menu a`, `.widget-type_html a`) влияет сразу на несколько областей сайта. Это потенциальная зона риска при дальнейшем изменении кнопок.

Inline CSS в Liquid-шаблонах также входит в фактический каскад и должен учитываться при любом дальнейшем CSS-аудите.

### JavaScript

`media/theme.js` пуст, но inline JavaScript присутствует в Liquid-шаблонах. Любая новая JS-логика должна сначала получить отдельную задачу и архитектурное место.

### Конфигурация

`config/settings.json`, `config/settings_data.json`, `config/setup.json` являются источниками конфигурации темы. Их нельзя менять без отдельной задачи.
