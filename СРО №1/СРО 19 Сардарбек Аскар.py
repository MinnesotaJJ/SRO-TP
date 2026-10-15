"""
Тема №19: Управление спортивными тренировками
Дисциплина: «Языки и технология программирования»
Консольное приложение для ведения базы упражнений, планирования тренировок
и расчета тоннажа (объема выполненной работы).
"""

import datetime

# Структуры данных для хранения информации
# База данных упражнений (словарь: название -> описание/категория)
EXERCISE_DATABASE = {
    "Приседания со штангой": "Базовое упражнение для ног и ягодиц",
    "Жим лежа": "Базовое упражнение для грудных мышц и трицепсов",
    "Становая тяга": "Базовое комплексное упражнение для спины и ног",
    "Подтягивания": "Упражнение с собственным весом для мышц спины",
    "Планка": "Статическое упражнение для укрепления кора",
}

# Журнал тренировок (список словарей)
WORKOUT_LOG = []


def display_header():
    """Вывод заголовка приложения."""
    print("=" * 50)
    print("   СИСТЕМА УПРАВЛЕНИЯ СПОРТИВНЫМИ ТРЕНИРОВКАМИ")
    print("=" * 50)


def show_exercises():
    """Функция 1: Просмотр доступных упражнений (работа со словарями и строками)."""
    print("\n--- БАЗА УПРАЖНЕНИЙ ---")
    if not EXERCISE_DATABASE:
        print("База данных упражнений пуста.")
        return

    # Цикл и обработка строк
    for idx, (name, description) in enumerate(EXERCISE_DATABASE.items(), 1):
        print(f"{idx}. {name.capitalize()} — {description}")


def add_exercise():
    """Добавление нового упражнения в справочник с проверкой ввода."""
    print("\n--- ДОБАВЛЕНИЕ НОВОГО УПРАЖНЕНИЯ ---")
    name = input("Введите название упражнения: ").strip()

    if not name:
        print("[ОШИБКА] Название упражнения не может быть пустым!")
        return

    # Проверка на дубликаты (регистронезависимо)
    if any(ex.lower() == name.lower() for ex in EXERCISE_DATABASE):
        print(
            f"[ПРЕДУПРЕЖДЕНИЕ] Упражнение '{name}' уже существует в базе."
        )
        return

    description = input("Введите описание или целевую группу мышц: ").strip()
    if not description:
        description = "Без описания"

    EXERCISE_DATABASE[name] = description
    print(f"[УСПЕХ] Упражнение '{name}' успешно добавлено в базу!")


def record_workout():
    """Функция 2: Регистрация результатов тренировки (списки, циклы, числа)."""
    print("\n--- РЕГИСТРАЦИЯ ТРЕНИРОВКИ ---")

    if not EXERCISE_DATABASE:
        print("[ОШИБКА] Сначала добавьте упражнения в базу!")
        return

    date_str = (
        input(
            "Введите дату тренировки (ГГГГ-ММ-ДД) или нажмите Enter для текущей: "
        )
        .strip()
    )
    if not date_str:
        date_str = datetime.date.today().isoformat()
    else:
        # Простая проверка формата даты
        try:
            datetime.date.fromisoformat(date_str)
        except ValueError:
            print("[ОШИБКА] Неверный формат даты! Используйте ГГГГ-ММ-ДД.")
            return

    show_exercises()
    ex_list = list(EXERCISE_DATABASE.keys())

    try:
        choice = int(
            input("Выберите номер упражнения для записи подхода: ")
        )
        if choice < 1 or choice > len(ex_list):
            print("[ОШИБКА] Неверный номер упражнения.")
            return
        selected_exercise = ex_list[choice - 1]
    except ValueError:
        print("[ОШИБКА] Пожалуйста, введите числовое значение.")
        return

    # Ввод параметров подхода с проверкой (цикл для валидации)
    sets_data = []
    print(f"Запись подхода для: {selected_exercise}")

    while True:
        try:
            weight_input = input(
                "Введите рабочий вес (кг) [0 для завершения ввода]: "
            )
            weight = float(weight_input)
            if weight < 0:
                print("Вес не может быть отрицательным.")
                continue
            if weight == 0:
                break

            reps_input = input("Введите количество повторений: ")
            reps = int(reps_input)
            if reps <= 0:
                print("Количество повторений должно быть больше 0.")
                continue

            # Сохраняем подход (структура данных: словарь)
            sets_data.append({"weight": weight, "reps": reps})
            print(
                f"  -> Добавлено: {weight} кг × {reps} повт."
            )

        except ValueError:
            print("[ОШИБКА] Введите корректные числовые данные.")

    if not sets_data:
        print("[ИНФО] Подходы не были добавлены.")
        return

    # Сохраняем тренировку в общий журнал
    workout_entry = {
        "date": date_str,
        "exercise": selected_exercise,
        "sets": sets_data,
    }
    WORKOUT_LOG.append(workout_entry)
    print(f"[УСПЕХ] Тренировка сохранена в журнал! Всего записей: {len(WORKOUT_LOG)}")


def view_workout_history():
    """Функция 3: Просмотр истории и расчет статистики (тоннаж)."""
    print("\n--- ИСТОРИЯ ТРЕНИРОВОК И СТАТИСТИКА ---")
    if not WORKOUT_LOG:
        print("Журнал тренировок пуст.")
        return

    total_tonnage_all = 0

    for idx, record in enumerate(WORKOUT_LOG, 1):
        print(f"\n{idx}. Дата: {record['date']} | Упражнение: {record['exercise']}")
        exercise_tonnage = 0
        for set_idx, s in enumerate(record["sets"], 1):
            set_tonnage = s["weight"] * s["reps"]
            exercise_tonnage += set_tonnage
            print(
                f"     Подход {set_idx}: {s['weight']} кг × {s['reps']} повт. (Тоннаж: {set_tonnage} кг)"
            )
        print(f"   Общий тоннаж по упражнению: {exercise_tonnage} кг")
        total_tonnage_all += exercise_tonnage

    print("-" * 40)
    print(f"Суммарный тоннаж за все тренировки: {total_tonnage_all} кг")


def search_workouts():
    """Функция 4: Поиск тренировок по названию упражнения или дате."""
    print("\n--- ПОИСК В ЖУРНАЛЕ ---")
    if not WORKOUT_LOG:
        print("Журнал пуст, искать нечего.")
        return

    query = input("Введите ключевое слово для поиска (дата или упражнение): ").strip().lower()
    if not query:
        print("[ОШИБКА] Поисковый запрос не может быть пустым.")
        return

    found = False
    for idx, record in enumerate(WORKOUT_LOG, 1):
        if query in record["date"].lower() or query in record["exercise"].lower():
            found = True
            print(f"\n[Найдено №{idx}] Дата: {record['date']} | Упражнение: {record['exercise']}")
            for s in record["sets"]:
                print(f"  - {s['weight']} кг × {s['reps']} повт.")

    if not found:
        print("По вашему запросу ничего не найдено.")


def main():
    """Главный цикл программы (меню)."""
    while True:
        display_header()
        print("1. Посмотреть базу упражнений")
        print("2. Добавить новое упражнение")
        print("3. Зарегистрировать тренировку (подходы)")
        print("4. Просмотреть историю и статистику (тоннаж)")
        print("5. Поиск по журналу")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите пункт меню (0-5): ").strip()

        if choice == "1":
            show_exercises()
        elif choice == "2":
            add_exercise()
        elif choice == "3":
            record_workout()
        elif choice == "4":
            view_workout_history()
        elif choice == "5":
            search_workouts()
        elif choice == "0":
            print("\nВыход из программы. Успешной защиты проекта!")
            break
        else:
            print("\n[ОШИБКА] Неверный выбор. Пожалуйста, введите цифру от 0 до 5.")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()