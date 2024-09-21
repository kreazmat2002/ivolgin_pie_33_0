import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Функция, которая возвращает значения для интерфейса
def get_values():
    return (
        (
            "value_img1.png",
            "100",
            "value_img2.png",
            "200",
        ),  # Первое значение для первой части экрана
        "Средняя длина очереди: 2.0 \nДоход супермаркета за неделю: 1432810.72 рублей",  # Значение для второй части экрана
        [
            ("Кассир 1 обслужил 1847 покупателей.", 13.27),
            ("Кассир 2 обслужил 1819 покупателей.", 11.60),
        ],
        "Общее среднее время ожидания: 12.44 минут",
    )


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Supermarket Statistics")
        self.geometry("1300x800")
        self.configure(bg="white")

        self.setup_UI()

    def display_values(self, frame, values):
        img1_path, val1, img2_path, val2 = values

        # Первая часть
        img1 = Image.open(img1_path)
        img1 = img1.resize((100, 100), Image.LANCZOS)
        img1 = ImageTk.PhotoImage(img1)

        img_label1 = tk.Label(frame, image=img1, bg="white")
        img_label1.image = img1
        img_label1.pack()

        val_label1 = tk.Label(
            frame, text=val1, font=("Arial", 12), fg="black", bg="white"
        )
        val_label1.pack()

        # Вторая часть
        img2 = Image.open(img2_path)
        img2 = img2.resize((100, 100), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)

        img_label2 = tk.Label(frame, image=img2, bg="white")
        img_label2.image = img2
        img_label2.pack()

        val_label2 = tk.Label(
            frame, text=val2, font=("Arial", 12), fg="black", bg="white"
        )
        val_label2.pack()

    def setup_UI(self):
        # Создать стили
        style = ttk.Style()
        style.configure(
            "TLabel", font=("Arial", 12), background="white", foreground="black"
        )

        # Основное окно разделено на три вертикальных части
        main_paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="white")
        main_paned_window.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(
            main_paned_window,
            borderwidth=1,
            relief="solid",
            bg="white",
            highlightbackground="blue",
        )
        center_frame = tk.Frame(
            main_paned_window,
            borderwidth=1,
            relief="solid",
            bg="white",
            highlightbackground="blue",
        )
        right_frame = tk.Frame(
            main_paned_window,
            borderwidth=1,
            relief="solid",
            bg="white",
            highlightbackground="blue",
        )

        main_paned_window.add(left_frame, stretch="always")
        main_paned_window.add(center_frame, stretch="always")
        main_paned_window.add(right_frame, stretch="always")

        # Кнопка начать симуляцию
        start_button = tk.Button(
            self,
            text="Начать продавать",
            command=lambda: self.show_values(left_frame, center_frame, right_frame),
        )
        start_button.pack(pady=10)
        start_button = tk.Button(
            self,
            text="С чистого листа",
            command=lambda: self.delete_values(left_frame, center_frame, right_frame),
        )
        start_button.pack(pady=10)

    def delete_values(self, left_frame, center_frame, right_frame):
        # Очистка фреймов
        for widget in left_frame.winfo_children():
            widget.destroy()
        for widget in center_frame.winfo_children():
            widget.destroy()
        for widget in right_frame.winfo_children():
            widget.destroy()

    def show_values(self, left_frame, center_frame, right_frame):
        # Очистка фреймов
        for widget in left_frame.winfo_children():
            widget.destroy()
        for widget in center_frame.winfo_children():
            widget.destroy()
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Левая часть окна - Первое значение и изображение
        left_contents = get_values()[0]
        self.display_values(left_frame, left_contents)

        # Средняя часть окна - Значение и условие для вывода текста
        center_value = get_values()[1]
        center_label = tk.Label(
            center_frame,
            text=str(center_value),
            font=("Arial", 12),
            fg="black",
            bg="white",
            anchor=tk.CENTER,
        )
        center_label.pack(fill=tk.BOTH, expand=True)

        if center_value < 50:
            conditional_label = tk.Label(
                center_frame,
                text="Значение меньше 50.",
                font=("Arial", 12),
                fg="black",
                bg="white",
            )
            conditional_label.pack()

        # Правая часть окна - текст и круговая диаграмма
        bottom_values = get_values()[2]
        footer_text = get_values()[3]

        right_texts = [text for text, _ in bottom_values]

        for text in right_texts:
            text_label = tk.Label(
                right_frame,
                text=text,
                font=("Arial", 12),
                fg="black",
                bg="white",
                anchor=tk.W,
            )
            text_label.pack(anchor=tk.W)

        # Построение круговой диаграммы
        fig, ax = plt.subplots()

        labels = ["Кассир 1", "Кассир 2"]
        sizes = [val for _, val in bottom_values]
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)

        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        footer_label = tk.Label(
            right_frame,
            text=footer_text,
            font=("Arial", 12),
            fg="black",
            bg="white",
            anchor=tk.W,
        )
        footer_label.pack(fill=tk.X, padx=10, pady=5)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
