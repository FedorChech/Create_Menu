import tkinter as tk
from SqlAlchemy import Product, Session, Dish, DishProduct
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox

window = ttk.Window(themename='superhero')
window.title("Кулинарный справочник")
window.geometry("600x700+500+50")
window.resizable(False, False)

frame_add_dish = ttk.Labelframe(window, text='Добавление блюд', style='info.TLabelframe', padding=5)
frame_add_dish.place(x=10, y=10)

frame_add_prod = ttk.Labelframe(window, text='Добавление продуктов', style='info.TLabelframe', padding=5)
frame_add_prod.place(x=300, y=10)

style = Style()
button_style = (OUTLINE, WARNING)

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
        entry_widget.configure(foreground='white')  # Восстановите обычный стиль при клике


def on_focusout(event, entry_widget, placeholder_text):
    if entry_widget.get() == '':
        entry_widget.insert(0, placeholder_text)
        entry_widget.configure(foreground='gray')  # Установите стиль для тусклого текста


# Function
def add_product():
    if entry_product.get() == "введите продукт":
        Messagebox.show_info(message="Введите продукт", title="Введите продукт")
    else:
        product_name = entry_product.get()
        new_product = Product(ProductName=product_name)
        session.add(new_product)
        session.commit()
        print(f"Продукт {product_name} добавлен")
        update_product_listbox()
        update_product_combobox()


def add_dish():
    if entry_dish.get() == "введите блюдо":
        Messagebox.show_info(message="Введите блюдо", title="Введите блюдо")
    else:
        dish_name = entry_dish.get()
        new_dish = Dish(DishName=dish_name)
        session.add(new_dish)
        session.commit()
        print(f"Блюдо {dish_name} добавлен")
        update_dish_listbox()
        display_products_for_dish()
        update_dish_listbox()


def delete_product():
    # Получите индекс выбранного элемента из Listbox
    selected_index = product_listbox.curselection()

    if selected_index:
        # Получите текст выбранного элемента
        selected_product = product_listbox.get(selected_index)

        # Найдите продукт в базе данных по имени (предполагая, что ProductName уникально)
        product = session.query(Product).filter_by(ProductName=selected_product).first()

        if product:
            # Удалите связи продукта с блюдами в таблице dish_product
            session.query(DishProduct).filter_by(product_id=product.id).delete()

            # Затем удалите сам объект Product
            session.delete(product)
            session.commit()
            print(f"Продукт '{selected_product}' удален вместе со связями")

            # Удаляем выбранный элемент из Listbox
            product_listbox.delete(selected_index)

            update_product_combobox()
            # update_dish_listbox()
            display_products_for_dish()

        else:
            print(f"Продукт '{selected_product}' не найден")
    else:
        print("Выберите продукт для удаления")



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
            update_dish_listbox()
            display_products_for_dish()
        else:
            print(f"Блюдо '{selected_dish}' не найдено")


def ask_question_delete_dish():
    result = Messagebox.show_question("Удалить", buttons=['Нет: primary', 'Да: secondary'], alert=True,
                                      parent=frame_add_dish)
    if result == "Да":
        # Выбран вариант "Да"
        print("Вы выбрали 'Да'")
        delete_dish()
    else:
        # Выбран вариант "Нет"
        print("Вы выбрали 'Нет'")
        return


def ask_question_delete_product():
    result = Messagebox.show_question("Удалить", buttons=['Нет: primary', 'Да: secondary'], alert=True,
                                      parent=frame_add_dish)
    if result == "Да":
        print("Вы выбрали 'Да'")
        delete_product()
    else:
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


def update_product_combobox():
    # Очистите текущий список блюд в dish_combobox
    product['values'] = ()

    # Получите список всех блюд из базы данных
    all_dishes = session.query(Dish).all()

    # Извлеките только имена блюд и обновите значения в dish_combobox
    dish_name = [dish.DishName for dish in all_dishes]
    product_combobox['values'] = tuple(dish_name)


def on_product_select():
    selected_product = product_listbox.get()

    # Получите блюдо из базы данных
    products = session.query(Product).filter_by(ProductName=selected_product).first()

    if products:

        # Добавьте каждый продукт в листбокс
        for product in products:
            product_listbox.insert.combobox


def update_product_combobox():
    # Получите все продукты из product_listbox
    all_products = [product_listbox.get(i) for i in range(product_listbox.size())]
    # Обновите значения product_combobox с продуктами
    product_combobox['values'] = tuple(all_products)


def on_dish_select(event=None):
    selected_index = dish_listbox.curselection()

    if selected_index:
        selected_item = dish_listbox.get(selected_index[0])  # Получаем выбранный элемент

        # Очищаем текущее содержимое Treeview
        tree.delete(*tree.get_children())  # Удаляем все строки из Treeview

        # Получаем блюдо из базы данных по имени
        dish = session.query(Dish).filter_by(DishName=selected_item).first()

        if dish:
            # Получаем записи DishProduct, связанные с выбранным блюдом
            dish_products = session.query(DishProduct).filter_by(dish_id=dish.id).all()

            # Добавляем каждую запись в Treeview
            for dish_product in dish_products:
                # Получаем продукт по ID из DishProduct
                product = session.query(Product).filter_by(id=dish_product.product_id).first()
                if product:
                    # Проверяем, что продукт не является None
                    tree.insert("", "end", values=(product.ProductName, dish_product.gramm))
                else:
                    print(f"Продукт с ID {dish_product.product_id} не найден")



def display_products_for_dish():
    # print(dish_listbox.curselection())
    # Очистите текущее содержимое Treeview
    tree.delete(*tree.get_children())  # Удалить все строки из Treeview

    selected_index = dish_listbox.curselection()

    if selected_index:
        selected_dish = dish_listbox.get(selected_index[0])
        print(selected_dish)

        dish = session.query(Dish).filter_by(DishName=selected_dish).first()

        if dish:
            # Получите записи DishProduct, связанные с выбранным блюдом
            dish_products = session.query(DishProduct).filter_by(dish_id=dish.id).all()

            # Добавьте каждую запись в Treeview
            for dish_product in dish_products:
                product = session.query(Product).filter_by(id=dish_product.product_id).first()
                tree.insert("", "end", values=(product.ProductName, dish_product.gramm))


# def add_products_to_dish():
#
#     selected_index = dish_listbox.curselection()
#
#     if selected_index:
#         selected_dish = dish_listbox.get(selected_index[0])
#         print(selected_dish)
#         selected_gramm = entry_gramm.get()
#
#         dish = session.query(Dish).filter_by(DishName=selected_dish).first()
#
#         if dish:
#
#             selected_products = dish_combobox.get()  # Получите индексы выбранных продуктов
#
#             if selected_products:
#                 # Получите текст выбранных продуктов
#                 # selected_product_names = [product_listbox.get(index) for index in selected_products]
#
#                 # Получите объекты продуктов из базы данных
#                 products = session.query(Product).filter_by(ProductName=selected_products).first()
#                 # products = session.query(Product).filter(Product.ProductName.in_(selected_product_names)).all()
#
#                 # Создайте записи в таблице DishProduct для связи продуктов с блюдом
#
#                 for product in products:
#                     dish_product = DishProduct(dish_id=dish.id, product_id=product.id, gramm=selected_gramm)
#                     session.add(dish_product)
#
#                 session.commit()
#
#                 # Обновите список продуктов для выбранного блюда
#                 display_products_for_dish()
#                 print(f"Продукты добавлены к блюду: {selected_dish}")
#             else:
#                 print(f"Выберите продукты для добавления к блюду - {dish.DishName}")
#
#         else:
#             print("Выберите блюдо для добавления продуктов.")

def add_products_to_dish():
    selected_product = product_combobox.get()  # Получите выбранный продукт из product_combobox
    selected_gramm = entry_gramm.get()

    if selected_product == "Выберите продукт":
        print("Выберите продукт для добавления к блюду.")
        return

    if selected_gramm == 'введите граммы':
        print("Введите количество грамм.")
        return

    selected_index = dish_listbox.curselection()

    if selected_index:
        selected_dish = dish_listbox.get(selected_index[0])
        print(selected_dish)

        dish = session.query(Dish).filter_by(DishName=selected_dish).first()

        if dish:
            # Получите объект продукта из базы данных
            product = session.query(Product).filter_by(ProductName=selected_product).first()

            if product:
                # Создайте запись в таблице DishProduct для связи продукта с блюдом
                dish_product = DishProduct(dish_id=dish.id, product_id=product.id, gramm=selected_gramm)
                session.add(dish_product)
                session.commit()

                # Обновите список продуктов для выбранного блюда
                display_products_for_dish()
                print(f"Продукт '{selected_product}' добавлен к блюду: {selected_dish}")
            else:
                print(f"Продукт '{selected_product}' не найден.")
        else:
            print("Выберите блюдо для добавления продуктов.")
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
                selected_dish = dish_listbox.get(dish_listbox.curselection()[0])

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
    on_dish_select()


# Widgets Product
label_image = tk.Label(window, image=tk_image)
label_image.place(x=310, y=312)

# _________________FRAME____________________________________
entry_product = ttk.Entry(frame_add_prod, width=20, foreground='gray')
# entry_product.place(x=10, y=40)
entry_product.grid(row=0, column=0)
entry_product.insert(0, 'введите продукт')

add_product_button = ttk.Button(frame_add_prod, text="+", command=add_product, width=5, style=(OUTLINE, WARNING))
add_product_button.grid(row=0, column=1)

entry_calories = ttk.Entry(frame_add_prod, width=20, foreground='gray')
entry_calories.grid(row=1, column=0, pady=10)
entry_calories.insert(0, 'введите калории')
entry_calories.bind("<FocusIn>", lambda event: on_entry_click(event, entry_calories, 'введите калории'))
entry_calories.bind("<FocusOut>", lambda event: on_focusout(event, entry_calories, 'введите калории'))

entry_dish = ttk.Entry(frame_add_dish, width=20, foreground='gray')
entry_dish.grid(row=0, column=3)
entry_dish.insert(0, 'введите блюдо')
entry_dish.bind("<FocusIn>", lambda event: on_entry_click(event, entry_dish, 'введите блюдо'))
entry_dish.bind("<FocusOut>", lambda event: on_focusout(event, entry_dish, 'введите блюдо'))

add_dish_button = ttk.Button(frame_add_dish, text="+", command=add_dish, width=6, style=(OUTLINE, WARNING))
add_dish_button.grid(row=0, column=4)

entry_product.bind("<FocusIn>", lambda event: on_entry_click(event, entry_product, 'введите продукт'))
entry_product.bind("<FocusOut>", lambda event: on_focusout(event, entry_product, 'введите продукт'))

product_list_label = ttk.Label(window, text="Список продуктов", font="play 14")
product_list_label.place(x=320, y=125)
dish_list_label = ttk.Label(window, text="Список блюд", font="play 14")
dish_list_label.place(x=45, y=125)

delete_button = ttk.Button(window, text="УДАЛИТЬ ПРОДУКТ", command=ask_question_delete_product, width=28,
                           style=button_style)
delete_button.place(x=300, y=275)

product_listbox = tk.Listbox(window, width=30, height=7)
product_listbox.place(x=300, y=150)

# Widgets Dish
delete_dish_button = ttk.Button(window, text="УДАЛИТЬ БЛЮДО", command=ask_question_delete_dish, width=28,
                                style=button_style)
delete_dish_button.place(x=10, y=275)

dish_listbox = tk.Listbox(window, width=30, height=7)
dish_listbox.place(x=10, y=150)
dish_listbox.bind("<<ListboxSelect>>", on_dish_select)

add_to_dish_button = ttk.Button(window, text="ДОБАВИТЬ", command=add_products_to_dish, width=11, style=button_style)
add_to_dish_button.place(x=10, y=620)

remove_to_dish_button = ttk.Button(window, text="УДАЛИТЬ", command=remove_products_from_dish, width=10,
                                   style=button_style)
remove_to_dish_button.place(x=135, y=620)

# Запросите блюда из базы данных
products = session.query(Product).all()

# Создаем список имен блюд
dish_names = [product.ProductName for product in products]

# Создаем Combobox и устанавливаем список блюд
product_combobox = ttk.Combobox(window, values=dish_names, width=29, foreground='gray')
product_combobox.set("Выберите продукт")
product_combobox.place(x=10, y=335)

# Привяжите обновление product_combobox к изменениям в product_listbox
product_listbox.bind("<<ListboxSelect>>", lambda event=None: update_product_combobox())

entry_gramm = ttk.Entry(window, width=31, foreground='gray')
entry_gramm.place(x=10, y=372)
entry_gramm.insert(0, 'введите граммы')
entry_gramm.bind("<FocusIn>", lambda event: on_entry_click(event, entry_gramm, 'введите граммы'))
entry_gramm.bind("<FocusOut>", lambda event: on_focusout(event, entry_gramm, 'введите граммы'))

# _______________Tree_____________________________
tree = ttk.Treeview(window, columns=("Column1", "Column2"), style="SUCCESS")

# Установка заголовков колонок
tree.heading("#1", text="Название")
tree.heading("#2", text="Граммы")

# Установка ширины колонок
tree.column("#0", width=0)
tree.column("#1", width=300, anchor='w')
tree.column("#2", width=100, anchor='e')

tree.place(x=10, y=420)

display_products_for_dish()

update_product_listbox()


# dish_combobox.bind("<<ComboboxSelected>>", on_dish_select)
# dish_combobox.bind("<<ComboboxSelected>>", lambda event=None: display_products_for_dish())
print(dish_listbox.curselection())
# Привязываем обработчик события к выбору элемента в dish_listbox
display_products_for_dish()
update_dish_listbox()
window.mainloop()
