import tkinter as tk
from tkinter import ttk, messagebox
from password_generator import generate_password
from history_manager import load_history, save_history

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("600x400")
        
        self.history = load_history()
        
        self.create_widgets()
        self.update_history_table()
    
    def create_widgets(self):
        # --- Настройки ---
        settings_frame = ttk.LabelFrame(self.root, text="Настройки генерации")
        settings_frame.pack(pady=10, fill='x', padx=10)
        
        # Длина пароля (Ползунок)
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.length_var = tk.IntVar(value=12)
        self.length_slider = ttk.Scale(settings_frame, from_=4, to=32, variable=self.length_var, orient='horizontal')
        self.length_slider.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='we')
        
        # Чекбоксы символов
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_letters_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(settings_frame, text="Цифры", variable=self.use_digits_var).grid(row=1, column=0, sticky='w')
        ttk.Checkbutton(settings_frame, text="Буквы", variable=self.use_letters_var).grid(row=1, column=1, sticky='w')
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.use_special_var).grid(row=1, column=2, sticky='w')
        
        # Кнопка генерации
        self.generate_btn = ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate_and_update)
        self.generate_btn.pack(pady=5)
        
        # Поле вывода пароля
        self.password_entry = ttk.Entry(self.root, width=50)
        self.password_entry.pack(pady=5)
        
        # Кнопка копирования (опционально)
        copy_btn = ttk.Button(self.root, text="Копировать", command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)
        
        # --- История ---
        history_frame = ttk.LabelFrame(self.root, text="История")
        history_frame.pack(pady=10, fill='both', expand=True, padx=10)
        
        self.history_tree = ttk.Treeview(history_frame, columns=("id", "password"), show='headings')
        self.history_tree.heading("id", text="ID")
        self.history_tree.heading("password", text="Пароль")
        
        self.history_tree.column("id", width=50)
        self.history_tree.column("password", width=400)
        
        self.history_tree.pack(fill='both', expand=True)
    
    def generate_and_update(self):
        """Генерирует пароль и обновляет интерфейс."""
        try:
            length = self.length_var.get()
            password = generate_password(
                length=length,
                use_digits=self.use_digits_var.get(),
                use_letters=self.use_letters_var.get(),
                use_special=self.use_special_var.get()
            )
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            
            # Сохраняем в историю (ID + Пароль + Настройки + Время можно добавить)
            entry = {
                "id": len(self.history) + 1,
                "password": password,
                "length": length,
                "digits": self.use_digits_var.get(),
                "letters": self.use_letters_var.get(),
                "special": self.use_special_var.get()
            }
            self.history.append(entry)
            save_history(self.history)
            self.update_history_table()
            
            messagebox.showinfo("Готово", "Пароль сгенерирован!")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def update_history_table(self):
        """Обновляет таблицу истории."""
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        
        for item in self.history:
            self.history_tree.insert("", 'end', values=(item['id'], item['password']))
    
    def copy_to_clipboard(self):
        """Копирует пароль в буфер обмена."""
        password = self.password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Скопировано", "Пароль скопирован в буфер обмена.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
