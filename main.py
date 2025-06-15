import random
import math
from abc import ABC, abstractmethod


class task(ABC):
    """
    Абстрактный базовый класс для математической задачи.
    Определяет общий интерфейс для генерации, отображения и проверки.   
    """

    def __init__(self, difficulty):
        if difficulty not in [1, 2, 3]:
            raise ValueError("Уровень сложности должен быть 1, 2 или 3.")
        self.difficulty = difficulty
        self.prompt_text = ""
        self.solution = None
        self.explanation = ""
        self.hint = ""
        self.generate()

    @abstractmethod
    def generate(self):
        """Генерирует параметры задачи, текст, решение и объяснение."""
        pass

    def get_prompt(self):
        """Возвращает текст задачи для пользователя."""
        return self.prompt_text

    def check_answer(self, user_answer):
        """
        Проверяет ответ пользователя. Возвращает кортеж (bool, str).
        Базовая реализация для строкового сравнения.
        """
        user_answer_cleaned = str(user_answer).strip().replace(" ", "")
        solution_cleaned = str(self.solution).strip().replace(" ", "")

        if user_answer_cleaned == solution_cleaned:
            return True, "🎉 Верно!"

        # Анализ общих ошибок
        if user_answer_cleaned.startswith("-") and not solution_cleaned.startswith("-"):
            hint = "💡 Подсказка: Проверьте знаки!"
        elif not user_answer_cleaned.startswith("-") and solution_cleaned.startswith("-"):
            hint = "💡 Подсказка: Проверьте знаки!"
        else:
            hint = f"Подсказка: {self.explanation}"

        error_message = f"❌ Неверно.\n   Правильный ответ: {self.solution}\n   {hint}"
        return False, error_message


class Derivativetask(task):
    """Задача: Нахождение производной функции."""

    def generate(self):
        if self.difficulty == 1:
            # f(x) = a*x + b
            a = random.randint(2, 10)
            b = random.randint(1, 10)
            self.prompt_text = f"Найдите производную функции f(x) = {a}*x + {b}"
            self.solution = str(a)
            self.hint = f"Вспомните правило: производная от ax + b равна a"
            self.explanation = f"Производная от линейной функции f(x) = ax + b равна 'a'"

        elif self.difficulty == 2:
            # f(x) = a * x^b
            a = random.randint(2, 5)
            b = random.randint(2, 5)
            self.prompt_text = f"Найдите производную функции f(x) = {a}*x^{b}"
            self.solution = f"{a * b}*x^{b - 1}"
            self.hint = "Используйте правило степени: (C*x^n)' = C*n*x^(n-1)"
            self.explanation = "Примените правило степени: (C*x^n)' = C*n*x^(n-1). Умножьте коэффициент на степень и уменьшите степень на 1."

        elif self.difficulty == 3:
            # f(x) = a * sin(b*x + c) или f(x) = a * cos(b*x + c)
            a = random.randint(2, 5) * random.choice([-1, 1])
            b = random.randint(2, 5)
            c = random.randint(1, 5)
            trig_func = random.choice(['sin', 'cos'])
            
            if trig_func == 'sin':
                self.prompt_text = f"Найдите производную функции f(x) = {a}*sin({b}*x + {c})\n(ответ дайте в формате, например: 10*cos(2*x+3))"
                self.solution = f"{a * b}*cos({b}*x+{c})"
                self.hint = "Используйте правило цепочки и помните, что производная от sin(u) равна cos(u)*u'"
                self.explanation = "Примените правило цепочки (f(g(x)))' = f'(g(x))*g'(x). Производная от sin(u) равна cos(u)*u'. Здесь u = bx + c, поэтому u' = b."
            else:  # cos
                self.prompt_text = f"Найдите производную функции f(x) = {a}*cos({b}*x + {c})\n(ответ дайте в формате, например: -10*sin(2*x+3))"
                self.solution = f"{-a * b}*sin({b}*x+{c})"
                self.hint = "Используйте правило цепочки и помните, что производная от cos(u) равна -sin(u)*u'"
                self.explanation = "Примените правило цепочки (f(g(x)))' = f'(g(x))*g'(x). Производная от cos(u) равна -sin(u)*u'. Здесь u = bx + c, поэтому u' = b."

    def check_answer(self, user_answer):
        """Специальная проверка для производных, принимающая разные форматы записи."""
        user_answer_cleaned = str(user_answer).strip().replace(" ", "")
        solution_cleaned = str(self.solution).strip().replace(" ", "")
        
        # Прямое сравнение
        if user_answer_cleaned == solution_cleaned:
            return True, "🎉 Верно!"
        
        # Нормализация выражений для сравнения
        def normalize_expression(expr):
            """Нормализует математическое выражение для сравнения."""
            # Убираем лишние пробелы и приводим к нижнему регистру
            expr = expr.lower().replace(" ", "")
            
            # Заменяем x^1 на x (степень 1 можно опустить)
            expr = expr.replace("^1", "")
            
            # Заменяем *x на x (умножение на x можно записать без *)
            expr = expr.replace("*x", "x")
            
            # Заменяем x* на x (x в начале можно записать без *)
            if expr.startswith("x*"):
                expr = expr[1:]
            
            # Обрабатываем случаи типа 6x -> 6*x
            import re
            # Находим паттерны типа "числоx" и заменяем на "число*x"
            expr = re.sub(r'(\d+)x', r'\1*x', expr)
            
            return expr
        
        # Сравниваем нормализованные выражения
        user_normalized = normalize_expression(user_answer_cleaned)
        solution_normalized = normalize_expression(solution_cleaned)
        
        if user_normalized == solution_normalized:
            return True, "🎉 Верно!"
        
        # Анализ общих ошибок
        if user_answer_cleaned.startswith("-") and not solution_cleaned.startswith("-"):
            hint = "💡 Подсказка: Вы поставили лишний минус. Проверьте знаки."
        elif not user_answer_cleaned.startswith("-") and solution_cleaned.startswith("-"):
            hint = "💡 Подсказка: Кажется, вы забыли минус. Проверьте знаки."
        else:
            hint = f"Подсказка: {self.explanation}"

        error_message = f"❌ Неверно.\n   Правильный ответ: {self.solution}\n   {hint}"
        return False, error_message


class LinearSystemtask(task):
    """Задача: Решение систем линейных уравнений."""

    def generate(self):
        if self.difficulty == 1:
            # ax + b = c
            a = random.randint(2, 10)
            x = random.randint(-10, 10)
            b = random.randint(-20, 20)
            c = a * x + b
            self.prompt_text = f"Решите уравнение: {a}x + {b} = {c}"
            self.solution = str(x)
            self.hint = f"Перенесите {b} в правую часть и разделите на {a}"
            self.explanation = f"Чтобы найти x, перенесите {b} в правую часть (получится {c - b}) и разделите всё на {a}. x = ({c - b}) / {a} = {x}."
        else:
            x, y = random.randint(-5, 5), random.randint(-5, 5)
            coeff_range = (1, 5) if self.difficulty == 2 else (2, 10)
            a1, b1, a2, b2 = [random.randint(*coeff_range) for _ in range(4)]

            while a1 * b2 - a2 * b1 == 0:  # Гарантируем единственность решения
                a2, b2 = random.randint(*coeff_range), random.randint(*coeff_range)

            c1 = a1 * x + b1 * y
            c2 = a2 * x + b2 * y
            self.prompt_text = (f"Решите систему уравнений и введите ответ для x и y через запятую (например: 5,-3):\n"
                                f"  {a1}x + {b1}y = {c1}\n"
                                f"  {a2}x + {b2}y = {c2}")
            self.solution = f"{x},{y}"
            self.hint = "Используйте метод подстановки или сложения уравнений"
            self.explanation = "Систему можно решить методом подстановки или сложения. Выразите одну переменную через другую из первого уравнения и подставьте во второе."

    def check_answer(self, user_answer):
        """Специальная проверка для систем, чтобы ловить перепутанные x и y."""
        user_answer_cleaned = str(user_answer).strip().replace(" ", "")
        if user_answer_cleaned == self.solution:
            return True, "🎉 Верно!"

        hint = f"Подсказка: {self.explanation}"
        # Попытка анализа типичных ошибок для систем
        try:
            user_x, user_y = map(int, user_answer_cleaned.split(','))
            sol_x, sol_y = map(int, self.solution.split(','))

            if user_x == sol_y and user_y == sol_x:
                hint = "💡 Подсказка: Похоже, вы перепутали местами x и y. Ответ ожидается в формате 'x,y'."
            elif user_x == sol_x and user_y != sol_y:
                hint = "💡 Подсказка: 'x' найден верно! Проверьте вычисления для 'y'."
            elif user_x != sol_x and user_y == sol_y:
                hint = "💡 Подсказка: 'y' найден верно! Проверьте вычисления для 'x'."
        except (ValueError, IndexError):
            pass  # Если формат ответа не 'число,число', используем общую подсказку

        error_message = f"❌ Неверно.\n   Правильный ответ: {self.solution}\n   {hint}"
        return False, error_message


class Probabilitytask(task):
    """Задача: Теория вероятностей."""

    def generate(self):
        if self.difficulty == 1:
            total = random.randint(10, 20)
            success = random.randint(2, total - 2)
            self.prompt_text = f"В корзине {total} шаров, из них {success} красных. Какова вероятность вынуть красный шар? (ответ округлите до 2 знаков после запятой)"
            self.solution = str(round(success / total, 2))
            self.hint = "Вероятность = (Количество благоприятных исходов) / (Общее количество исходов)"
            self.explanation = f"Вероятность = {success} / {total} = {round(success / total, 2)}. Это отношение количества красных шаров к общему количеству шаров."
        elif self.difficulty == 2:
            sides = 6
            outcome = random.randint(1, 6)
            self.prompt_text = f"Игральный кубик (6 граней) бросают дважды. Какова вероятность, что оба раза выпадет число {outcome}? (ответ округлите до 3 знаков после запятой)"
            self.solution = str(round((1 / sides) * (1 / sides), 3))
            self.hint = "Вероятность двух независимых событий равна произведению их вероятностей"
            self.explanation = f"Вероятность двух независимых событий P(A и B) равна произведению их вероятностей P(A) * P(B). P = (1/6) * (1/6) = {round((1/sides)**2, 3)}."
        elif self.difficulty == 3:
            total = random.randint(10, 15)
            red = random.randint(5, total - 2)
            self.prompt_text = (
                f"В урне {red} красных и {total - red} синих шаров. Из урны последовательно достают два шара. "
                f"Какова вероятность, что оба шара окажутся красными? (ответ округлите до 3 знаков после запятой)")
            p1 = red / total
            p2 = (red - 1) / (total - 1)
            self.solution = str(round(p1 * p2, 3))
            self.hint = "Это зависимые события. P(A и B) = P(A) * P(B|A)"
            self.explanation = f"Это зависимые события. P(A и B) = P(A) * P(B|A), где P(B|A) - вероятность второго события после первого. P = ({red}/{total}) * ({(red-1)}/{(total-1)}) = {round(p1 * p2, 3)}."

    def check_answer(self, user_answer):
        """Специальная проверка для чисел с плавающей точкой."""
        try:
            user_val = float(str(user_answer).replace(',', '.'))
            solution_val = float(self.solution)

            if math.isclose(user_val, solution_val, rel_tol=1e-3):
                return True, "🎉 Верно!"

            hint = f"Подсказка: {self.explanation}"
            if user_val > 1 or user_val < 0:
                hint = "💡 Подсказка: Вероятность не может быть больше 1 или меньше 0."
            elif math.isclose(user_val, 1 - solution_val):
                hint = "💡 Подсказка: Похоже, вы нашли вероятность противоположного события."

            error_message = f"❌ Неверно.\n   Правильный ответ: {self.solution}\n   {hint}"
            return False, error_message

        except ValueError:
            error_message = f"❌ Неверно.\n   Правильный ответ: {self.solution}\n   💡 Подсказка: Ответ должен быть числом."
            return False, error_message


class Combinatoricstask(task):
    """Задача: Комбинаторика."""

    def generate(self):
        if self.difficulty == 1:
            n = random.randint(4, 7)
            self.prompt_text = f"Сколькими способами можно расставить {n} разных книг на полке?"
            self.solution = str(math.factorial(n))
            self.hint = f"Это число перестановок, которое равно n! ({n}!)"
            self.explanation = f"Это число перестановок, которое равно n! ({n}!). {n}! = {math.factorial(n)}."
        elif self.difficulty == 2:
            n = random.randint(5, 10)
            k = random.randint(2, 4)
            self.prompt_text = f"Сколькими способами можно выбрать {k} человека на {k} разные должности из {n} кандидатов?"
            self.solution = str(math.perm(n, k))
            self.hint = "Порядок важен, поэтому используем размещения: A(n, k) = n! / (n-k)!"
            self.explanation = f"Порядок важен, поэтому используем размещения: A(n, k) = n! / (n-k)!. A({n}, {k}) = {n}! / ({n}-{k})! = {math.perm(n, k)}."
        elif self.difficulty == 3:
            n = random.randint(10, 15)
            k = random.randint(3, 5)
            self.prompt_text = f"Сколькими способами можно выбрать команду из {k} человек из группы в {n} человек?"
            self.solution = str(math.comb(n, k))
            self.hint = "Порядок не важен, поэтому используем сочетания: C(n, k) = n! / (k! * (n-k)!)"
            self.explanation = f"Порядок не важен, поэтому используем сочетания: C(n, k) = n! / (k! * (n-k)!). C({n}, {k}) = {n}! / ({k}! * ({n}-{k})!) = {math.comb(n, k)}."
            self.n, self.k = n, k  # Сохраняем для анализа ответа

    def check_answer(self, user_answer):
        """Специальная проверка, чтобы отличить сочетания от размещений."""
        user_answer_cleaned = str(user_answer).strip().replace(" ", "")
        if user_answer_cleaned == self.solution:
            return True, "🎉 Верно!"

        hint = f"Подсказка: {self.explanation}"
        # Анализ путаницы между сочетаниями и размещениями
        if self.difficulty == 3:
            try:
                user_val = int(user_answer_cleaned)
                # Если пользователь посчитал размещения вместо сочетаний
                if user_val == math.perm(self.n, self.k):
                    hint = "💡 Подсказка: Вы посчитали размещения (A), а нужны сочетания (C). Порядок в команде не важен, поэтому нужно разделить на k!."
            except (ValueError, AttributeError):
                pass

        error_message = f"❌ Неверно.\n   Правильный ответ: {self.solution}\n   {hint}"
        return False, error_message


class Sequencetask(task):
    """Задача: Числовые последовательности."""

    def generate(self):
        start = random.randint(1, 10)
        if self.difficulty == 1:
            # Арифметическая
            step = random.randint(2, 10)
            seq = [start + i * step for i in range(4)]
            self.prompt_text = f"Найдите следующий член в последовательности: {', '.join(map(str, seq))}, ..."
            self.solution = str(seq[-1] + step)
            self.hint = f"Это арифметическая прогрессия с шагом {step}"
            self.explanation = f"Это арифметическая прогрессия с шагом {step}. Каждый следующий член получается прибавлением {step} к предыдущему. Следующий член: {seq[-1]} + {step} = {seq[-1] + step}."
        elif self.difficulty == 2:
            # Геометрическая
            ratio = random.randint(2, 3)
            seq = [start * (ratio ** i) for i in range(4)]
            self.prompt_text = f"Найдите следующий член в последовательности: {', '.join(map(str, seq))}, ..."
            self.solution = str(seq[-1] * ratio)
            self.hint = f"Это геометрическая прогрессия, каждый член умножается на {ratio}"
            self.explanation = f"Это геометрическая прогрессия, каждый член умножается на {ratio}. Следующий член: {seq[-1]} * {ratio} = {seq[-1] * ratio}."
        elif self.difficulty == 3:
            # Квадратичная
            a = random.randint(2, 4)
            b = random.randint(1, 5)
            seq = [a * (n ** 2) + b for n in range(1, 5)]
            self.prompt_text = f"Найдите следующий член в последовательности: {', '.join(map(str, seq))}, ..."
            self.solution = str(a * (5 ** 2) + b)
            self.hint = f"Последовательность задана формулой a*n^2 + b, где n - номер члена"
            self.explanation = f"Последовательность задана формулой a*n^2 + b, где n - номер члена. Здесь a={a}, b={b}. Следующий член (n=5): {a}*5^2 + {b} = {a * 25} + {b} = {a * (5 ** 2) + b}."


# --- Основной цикл программы ---

def main():
    """Главная функция для взаимодействия с пользователем."""
    task_map = {
        "1": ("Производная функции", Derivativetask),
        "2": ("Решение системы уравнений", LinearSystemtask),
        "3": ("Теория вероятностей", Probabilitytask),
        "4": ("Комбинаторика", Combinatoricstask),
        "5": ("Числовые последовательности", Sequencetask)
    }

    print("Добро пожаловать в систему решения математических задач!")
    while True:
        print("\n" + "=" * 30)
        print("Выберите тип задачи:")
        for key, (name, _) in task_map.items():
            print(f"  {key}. {name}")

        task_choice = input("Введите номер задачи (или 'q' для выхода): ").strip()
        if task_choice.lower() == 'q':
            print("До встречи!")
            break
        if task_choice not in task_map:
            print("🚨 Неверный номер задачи. Попробуйте снова.")
            continue

        try:
            difficulty_choice = int(input("Выберите уровень сложности (1-3): ").strip())
            if difficulty_choice not in [1, 2, 3]: raise ValueError
        except ValueError:
            print("🚨 Пожалуйста, введите число от 1 до 3.")
            continue

        task_name, task_class = task_map[task_choice]
        current_task = task_class(difficulty=difficulty_choice)

        print("\n--- ЗАДАЧА ---")
        print(current_task.get_prompt())
        print("-" * 14)
        
        # Первая попытка
        user_answer = input("Ваш ответ (1-я попытка): ")
        is_correct, message = current_task.check_answer(user_answer)
        
        if is_correct:
            print("🎉 Отлично! Вы решили задачу с первой попытки!")
        else:
            # Показываем только подсказку без правильного ответа
            print("❌ Неверно.")
            print(f"💡 Подсказка: {current_task.hint}")
            
            # Вторая попытка
            print("\n💡 У вас есть еще одна попытка!")
            user_answer = input("Ваш ответ (2-я попытка): ")
            is_correct, message = current_task.check_answer(user_answer)
            print(message)

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()