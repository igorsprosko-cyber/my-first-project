# SITE MAP

Версия: 1.0

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

Фактический пользовательский CSS сейчас сосредоточен в `media/theme.scss`.

Основные зоны внутри файла:

1. настройки редактора InSales;
2. шапка и мобильная боковая панель;
3. логотип и навигация;
4. поиск;
5. подвал;
6. SEO-скрытие дублирующего H1;
7. ссылки, стилизованные как кнопки категорий;
8. резервный класс `.vl-category-btn`.

Отдельных рабочих файлов `styles/*.css` в `main` сейчас нет. Поэтому создание дополнительных CSS-файлов без отдельной задачи запрещено: сначала нужно определить границы модулей и способ их подключения через InSales.

## 4. JavaScript-карта

`media/theme.js` существует, но сейчас пустой.

Следовательно, отдельной пользовательской JS-архитектуры в репозитории пока нет. Нельзя создавать её самостоятельно только на основании этого факта.

## 5. Карта виджетов

По текущей структуре тема использует стандартные InSales widget-механизмы и системные виджеты. Наиболее явно это видно в `media/theme.scss`, где стили адресуются к классам и селекторам вида:

- `.widget-type_text`;
- `.widget-type_menu`;
- `.widget-type_html`;
- `.widget-type_system_widget_v4_catalog_4`;
- `[data-fixed-panels]`;
- `[data-widget-add]`.

Полный перечень конкретных виджетов требует анализа конфигурации `config/settings.json` и `config/setup.json`, а не догадки по CSS-классам.

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

### JavaScript

`media/theme.js` пуст. Любая новая JS-логика должна сначала получить отдельную задачу и архитектурное место.

### Конфигурация

`config/settings.json`, `config/settings_data.json`, `config/setup.json` являются источниками конфигурации темы. Их нельзя менять без отдельной задачи.
