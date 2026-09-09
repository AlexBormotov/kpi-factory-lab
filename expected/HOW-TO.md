# Как заполнить expected/kpi.csv

Не запускайте `python generate.py` после заполнения: он перезапишет этот файл пустым шаблоном.

## Разрез

Одна строка = одна `campaign` + один `day`. Не сумма по всем кампаниям.

## Фильтры

Из `fixtures/clicks.csv`: берите строки этой кампании и дня, где `is_bot` = `false`. Сложите `cost`.

Из `fixtures/conversions.csv`: сумма `payout` только при `type` = `purchase`. `lead` и `click` не входят.

Нет валидных кликов — `cost` = 0. Нет покупок — `revenue` = 0.

Profit и ROI не заполняйте.

## Колонки шаблона

```
campaign,day,cost,revenue
```
