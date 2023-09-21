import tkinter as tk
from tkinter import messagebox

# from tkinter import ttk
from SqlAlchemy import Product, Session, Dish, DishProduct
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageFilter  # Импортируем ImageFilter

# window = tk.Tk()
window = ttk.Window(themename='journal')
window.title("Apps")
window.geometry("510x670+500+50")
window.resizable(False, False)

# Устанавливаем стиль для окна с помощью ttkbootstrap
style = ttk.Style()
window.configure(background="#EEEEEE")  # Замените "your_color_here" на желаемый цвет фона
text_color = "#005453"
fon_color = "#EEEEEE"
session = Session()

# Открываем изображение
# Устанавливаем новые размеры изображения
image = Image.open("Dinner.png")
new_width = 100  # Ширина
new_height = 100  # Высота

# Изменяем размер изображения
resized_image = image.resize((new_width, new_height))

# Создаем объект PhotoImage изображения
tk_image = ImageTk.PhotoImage(resized_image)


def on_entry_click(event, entry_widget, placeholder_text):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")  # Удалите начальный текст при клике


def on_focusout(event, entry_widget, placeholder_text):
    if entry_widget.get() == '':
        entry_widget.insert(0, placeholder_text)


# Function
def add_product():
    product_name = entry_product.get()
    new_product = Product(ProductName=product_name)
    session.add(new_product)
    session.commit()
    print(f"Продукт {product_name} добавлен")
    update_product_listbox()


def add_dish():
    dish_name = entry_dish.get()
    new_dish = Dish(DishName=dish_name)
    session.add(new_dish)
    session.commit()
    print(f"Блюдо {dish_name} добавлен")
    update_dish_listbox()
    display_products_for_dish()
    update_dish_combobox()


def delete_product():
    # Получите индекс выбранного элемента из Listbox
    selected_index = product_listbox.curselection()

    if selected_index:
        # Получите текст выбранного элемента
        selected_product = product_listbox.get(selected_index)

        # Найдите продукт в базе данных по имени (предполагая, что ProductName уникально)
        product = session.query(Product).filter_by(ProductName=selected_product).first()

        if product:
            # Если продукт найден, удаляем его из сессии и коммитим изменения
            session.delete(product)
            session.commit()
            print(f"Продукт '{selected_product}' удален")
            # Удаляем выбранный элемент из Listbox
            product_listbox.delete(selected_index)
        else:
            print(f"Продукт '{selected_product}' не найден")


def delete_dish():
    # Получите индекс выбранного элемента из Listbox
    selected_index = dish_listbox.curselection()

    if selected_index:
        # Получите текст выбранного элемента
        selected_dish = dish_listbox.get(selected_index)

        # Найдите блюдо в базе данных по имени (предполагая, что ProductName уникально)
        dish = session.query(Dish).filter_by(DishName=selected_dish).first()

        if dish:
            # Если продукт найден, удаляем его из сессии и коммитим изменения
            session.delete(dish)
            session.commit()

            print(f"Блюдо> '{selected_dish}' удалено")
            # Удаляем выбранный элемент из Listbox
            dish_listbox.delete(selected_index)
            display_products_for_dish()
            update_dish_combobox()
        else:
            print(f"Блюдо '{selected_dish}' не найдено")


def ask_question_delete_dish():
    result = messagebox.askquestion("Подтверждение", "Удалить?")
    if result == "yes":
        # Выбран вариант "Да"
        print("Вы выбрали 'Да'")
        delete_dish()
    else:
        # Выбран вариант "Нет"
        print("Вы выбрали 'Нет'")
        return


def ask_question_delete_product():
    result = messagebox.askquestion("Подтверждение", "Удалить?")
    if result == "yes":
        # Выбран вариант "Да"
        print("Вы выбрали 'Да'")
        delete_product()
    else:
        # Выбран вариант "Нет"
        print("Вы выбрали 'Нет'")
        return


def update_product_listbox():
    # Очистите текущее содержимое Listbox
    product_listbox.delete(0, tk.END)

    # Извлеките список продуктов из базы данных с помощью сессии SQLAlchemy
    products = session.query(Product).all()

    # Добавьте каждый продукт в Listbox
    for product in products:
        product_listbox.insert(tk.END, product.ProductName)


def update_dish_listbox():
    # Очистите текущее содержимое Listbox
    dish_listbox.delete(0, tk.END)

    # Извлеките список продуктов из базы данных с помощью сессии SQLAlchemy
    dishes = session.query(Dish).all()

    # Добавьте каждый продукт в Listbox
    for dish in dishes:
        dish_listbox.insert(tk.END, dish.DishName)


def update_dish_combobox():
    # Очистите текущий список блюд в dish_combobox
    dish_combobox['values'] = ()

    # Получите список всех блюд из базы данных
    all_dishes = session.query(Dish).all()

    # Извлеките только имена блюд и обновите значения в dish_combobox
    dish_names = [dish.DishName for dish in all_dishes]
    dish_combobox['values'] = tuple(dish_names)


def on_dish_select():
    selected_dish = dish_combobox.get()

    # Очистите текущее содержимое листбокса
    product_listbox.delete(0, tk.END)

    # Получите блюдо из базы данных
    dish = session.query(Dish).filter_by(DishName=selected_dish).first()

    if dish:
        # Получите продукты, связанные с выбранным блюдом
        products = session.query(Product).join(DishProduct).filter_by(dish_id=dish.id).all()

        # Добавьте каждый продукт в листбокс
        for product in products:
            product_listbox.insert(tk.END, product.ProductName)


def display_products_for_dish():
    # Очистите текущее содержимое Treeview
    tree.delete(*tree.get_children())  # Удалить все строки из Treeview

    selected_dish = dish_combobox.get()
    # selected_dish = dish_listbox.get(dish_listbox.curselection())

    # Получите блюдо из базы данных
    dish = session.query(Dish).filter_by(DishName=selected_dish).first()

    if dish:
        # Получите записи DishProduct, связанные с выбранным блюдом
        dish_products = session.query(DishProduct).filter_by(dish_id=dish.id).all()

        # Добавьте каждую запись в Treeview
        for dish_product in dish_products:
            product = session.query(Product).filter_by(id=dish_product.product_id).first()
            tree.insert("", "end", values=(product.ProductName, dish_product.gramm))


def add_products_to_dish():
    selected_dish = dish_combobox.get()
    selected_gramm = entry_gramm.get()
    if selected_gramm == 'введите граммы':
        messagebox.showinfo("ПРЕДУПРЕЖДЕНИЕ", "Введите количество грамм продукта!")
    # Получите блюдо из базы данных
    dish = session.query(Dish).filter_by(DishName=selected_dish).first()

    if dish:
        selected_products = product_listbox.curselection()  # Получите индексы выбранных продуктов

        if selected_products:
            # Получите текст выбранных продуктов
            selected_product_names = [product_listbox.get(index) for index in selected_products]

            # Получите объекты продуктов из базы данных
            products = session.query(Product).filter(Product.ProductName.in_(selected_product_names)).all()

            # Создайте записи в таблице DishProduct для связи продуктов с блюдом

            for product in products:
                dish_product = DishProduct(dish_id=dish.id, product_id=product.id, gramm=selected_gramm)
                session.add(dish_product)

            session.commit()

            # Обновите список продуктов для выбранного блюда
            display_products_for_dish()
            print(f"Продукты добавлены к блюду: {selected_dish}")
        else:
            print("Выберите продукты для добавления к блюду.")

    else:
        print("Выберите блюдо для добавления продуктов.")


def remove_products_from_dish():
    # Получите выбранные элементы в Treeview
    selected_items = tree.selection()

    if selected_items:
        for item in selected_items:
            # Получите данные из выбранной строки
            values = tree.item(item, 'values')

            if values:
                selected_product = values[0]  # Первое значение - название продукта
                selected_dish = dish_combobox.get()

                # Найдите блюдо в базе данных по имени
                dish = session.query(Dish).filter_by(DishName=selected_dish).first()

                if dish:
                    # Найдите продукт в базе данных по имени
                    product = session.query(Product).filter_by(ProductName=selected_product).first()

                    if product:
                        # Удалите связь продукта с блюдом, если она существует
                        dish_product = session.query(DishProduct).filter_by(dish_id=dish.id,
                                                                            product_id=product.id).first()
                        if dish_product:
                            session.delete(dish_product)
                            session.commit()
                            print(f"Продукт '{selected_product}' удален из блюда '{selected_dish}'")
                        else:
                            print(f"Продукт '{selected_product}' не связан с блюдом '{selected_dish}'")
                    else:
                        print(f"Продукт '{selected_product}' не найден")
                else:
                    print(f"Блюдо '{selected_dish}' не найдено")
    else:
        print("Выберите продукты для удаления из блюда")
        messagebox.showinfo("ПРЕДУПРЕЖДЕНИЕ", "Выберите продукты для удаления из блюдая")

    # Обновите список продуктов в product_dish_listbox после удаления
    display_products_for_dish()


# Widgets Product
label_image = tk.Label(window, image=tk_image)
label_image.place(x=310, y=312)

main_label = ttk.Label(window, text="ДОБАВИТЬ ПРОДУКТ", font="arial 12 bold", background=fon_color, bootstyle="danger")
# main_label.config(foreground=text_color)

main_label.place(x=30, y=10)

entry_product = ttk.Entry(window, width=20)
entry_product.place(x=10, y=40)
entry_product.insert(0, 'введите продукт')
entry_product.bind("<FocusIn>", lambda event: on_entry_click(event, entry_product, 'введите продукт'))
entry_product.bind("<FocusOut>", lambda event: on_focusout(event, entry_product, 'введите продукт'))

product_list_label = ttk.Label(window, text="СПИСОК ПРОДУКТОВ", font="arial 9", background=fon_color)
product_list_label.config(foreground=text_color)
product_list_label.place(x=40, y=130)
dish_list_label = ttk.Label(window, text="СПИСОК БЛЮД", font="arial 9", background=fon_color)
dish_list_label.config(foreground=text_color)
dish_list_label.place(x=300, y=130)

entry_calories = ttk.Entry(window, width=20)
entry_calories.place(x=10, y=80)
entry_calories.insert(0, 'введите калории')
entry_calories.bind("<FocusIn>", lambda event: on_entry_click(event, entry_calories, 'введите калории'))
entry_calories.bind("<FocusOut>", lambda event: on_focusout(event, entry_calories, 'введите калории'))

add_button = ttk.Button(window, text="+", command=add_product, width=6)
add_button.place(x=143, y=40)
delete_button = ttk.Button(window, text="УДАЛИТЬ ПРОДУКТ", command=ask_question_delete_product, width=23)
delete_button.place(x=10, y=268)

product_listbox = tk.Listbox(window, width=25, height=7)
product_listbox.place(x=10, y=150)

# Widgets Dish
main_label = ttk.Label(window, text="ДОБАВИТЬ БЛЮДО", font="arial 12 bold", background=fon_color)
main_label.config(foreground=text_color)
main_label.place(x=275, y=10)

entry_dish = ttk.Entry(window, width=20)
entry_dish.place(x=270, y=40)
entry_dish.insert(0, 'введите блюдо')
entry_dish.bind("<FocusIn>", lambda event: on_entry_click(event, entry_dish, 'введите блюдо'))
entry_dish.bind("<FocusOut>", lambda event: on_focusout(event, entry_dish, 'введите блюдо'))

add_dish_button = ttk.Button(window, text="+", command=add_dish, width=5)
add_dish_button.place(x=400, y=40)
delete_dish_button = ttk.Button(window, text="УДАЛИТЬ БЛЮДО", command=ask_question_delete_dish, width=23)
delete_dish_button.place(x=270, y=270)

dish_listbox = tk.Listbox(window, width=25, height=7)
dish_listbox.place(x=270, y=150)

add_to_dish_button = ttk.Button(window, text="ДОБАВИТЬ", command=add_products_to_dish, width=11)
add_to_dish_button.place(x=10, y=620)

remove_to_dish_button = ttk.Button(window, text="УДАЛИТЬ", command=remove_products_from_dish, width=10)
remove_to_dish_button.place(x=135, y=620)

## Запросите блюда из базы данных
dishes = session.query(Dish).all()

# Создаем список имен блюд
dish_names = [dish.DishName for dish in dishes]

# Создаем Combobox и устанавливаем список блюд
dish_combobox = ttk.Combobox(window, values=dish_names, width=29)
dish_combobox.set("Выберите блюдо")
dish_combobox.place(x=10, y=335)

entry_gramm = ttk.Entry(window, width=31)
entry_gramm.place(x=10, y=372)
entry_gramm.insert(0, 'введите граммы')
entry_gramm.bind("<FocusIn>", lambda event: on_entry_click(event, entry_gramm, 'введите граммы'))
entry_gramm.bind("<FocusOut>", lambda event: on_focusout(event, entry_gramm, 'введите_граммы'))

# _______________Tree_____________________________
tree = ttk.Treeview(window, columns=("Column1", "Column2"))

# Установка заголовков колонок
tree.heading("#1", text="Название")
tree.heading("#2", text="Граммы")

# Установка ширины колонок
tree.column("#0", width=0)
tree.column("#1", width=300, anchor='w')
tree.column("#2", width=100, anchor='e')

tree.place(x=10, y=420)

dish_combobox.bind("<<ComboboxSelected>>", on_dish_select)
dish_combobox.bind("<<ComboboxSelected>>", lambda event=None: display_products_for_dish())

display_products_for_dish()

update_product_listbox()
update_dish_listbox()

window.mainloop()
