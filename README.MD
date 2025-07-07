# Практика: Добавление фильтров для сниппетов

## Описание
Добавление функционала фильтрации позволит пользователям быстро находить нужные сниппеты по определённым критериям, 
таким как **автор** и **язык программирования**. Это значительно улучшит навигацию и удобство использования платформы.

## Цель
Реализовать механизм фильтрации списка сниппетов на странице.

## Задачи

### 1. Определите критерии фильтрации
Выберем, по каким полям будет осуществляться фильтрация:
* **По автору**
* **По языку сниппета**

### 2. Шаблон для отображения фильтра

Добавим фильтры на странице `Просмотр сниппетов`, используя следующий макет:

```html
<form action="" method="get">
    <div class="d-flex flex-wrap align-items-end gap-3 mb-3">

        <div class="d-flex align-items-center gap-2 flex-grow-1">
            <label class="form-label mb-0 text-nowrap">
                <i class="fas fa-code me-1"></i> Язык:
            </label>
            <select class="form-select">
                <option value="" selected>Все языки</option>
                <option value="Python">Python</option>
                <option value="C++">C++</option>
                <option value="Java">Java</option>
                <option value="JavaScript">JavaScript</option>
            </select>
        </div>

        <div class="d-flex align-items-center gap-2 flex-grow-1">
            <label for="authorFilter" class="form-label mb-0 text-nowrap">
                <i class="fas fa-user me-1"></i> Автор:
            </label>
            <select class="form-select">
                <option value="" selected>Все авторы</option>
                <option value="1">user-1</option>
                <option value="2">user-2</option>
                <option value="3">user-3</option>
            </select>
        </div>

        <div>
            <button type="submit" class="btn btn-primary">Применить фильтры</button>
        </div>
    </div>
</form>
```

#### 2.1. Доработка фильтров

[ ] Сейчас в полях фильтра используются заглушки, замените их реальными данными вашего приложения.
[ ] Исправите форму фильтра, чтобы при нажатии на кнопку `Применить фильтры` данные формы передавались в качестве GET-параметров.

### 3. Модификация View для обработки фильтров

В представлении, которое отображает список сниппетов (например, `snippet_list`), необходимо обработать параметры фильтрации из GET-запроса.

[ ] **Получение параметров:** Извлекайте значения фильтров из `request.GET`.
    Например: `lang_filter = request.GET.get('lang_filter')`.
[ ] **Применение фильтров к QuerySet:** Используйте метод `.filter()` для QuerySet.

### 4. Визуализация фильтров

[ ] После обновления страницы, выбранные параметры фильтра должны отображаться в поле фильтра. \
**Пояснение**: если выбран фильтр по языку, то в поле языка должен отображаться выбранный язык.

[ ] Добавьте возможность удобного сброса фильтра