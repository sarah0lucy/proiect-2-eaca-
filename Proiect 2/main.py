import tkinter as tk
from tkinter import ttk
import math


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proiect 2")
        self.iconbitmap('draw.ico')

        # Frame pentru zona verticala 1
        frame1 = ttk.Frame(self)
        frame1.grid(row=0, column=0, padx=10, pady=10)

        self.listbox1 = tk.Listbox(frame1, height=10)
        self.listbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox2 = tk.Listbox(frame1, height=10)
        self.listbox2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame pentru zona 2 (desenul figurii selectate)
        frame_draw1 = ttk.Frame(self)
        frame_draw1.grid(row=0, column=1, padx=10, pady=10)

        self.canvas1 = tk.Canvas(frame_draw1, width=200, height=200, bg="white")
        self.canvas1.pack(fill=tk.BOTH, expand=True)

        # Frame pentru zona vericala 3 (rezultatul)
        frame_draw2 = ttk.Frame(self)
        frame_draw2.grid(row=0, column=2, padx=10, pady=10)

        self.canvas2 = tk.Canvas(frame_draw2, width=200, height=200, bg="white")
        self.canvas2.pack(fill=tk.BOTH, expand=True)

        # Frame pentru zona orizontala (de text)
        self.frame_text = ttk.Frame(self)
        self.frame_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.entry1_label = ttk.Label(self.frame_text, text="dx:")
        self.entry1_label.grid(row=0, column=0, padx=5, pady=5)
        self.entry1 = tk.Entry(self.frame_text)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        self.entry2_label = ttk.Label(self.frame_text, text="dy:")
        self.entry2_label.grid(row=1, column=0, padx=5, pady=5)
        self.entry2 = tk.Entry(self.frame_text)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        self.button = ttk.Button(self.frame_text, text="Aplică", command=self.apply_transformation)
        self.button.grid(row=2, column=0, columnspan=2, pady=10)

        self.reset_button = ttk.Button(self.frame_text, text="Reset", command=self.reset_canvas)
        self.reset_button.grid(row=3, column=0, columnspan=2, pady=10)


        self.populate_list()
        self.current_figure_coords = None

    def populate_list(self):
        items = ["Segment", "Triunghi", "Patrat", "Hexagon", "Cerc", "Dreptunghi", "Semiplan Superior", "Ngon"]
        items2 = ["Translatie", "Omotetie", "Rotatie"]

        for item in items:
            self.listbox1.insert(tk.END, item)

        self.listbox1.bind('<<ListboxSelect>>', self.draw_figure)

        for item in items2:
            self.listbox2.insert(tk.END, item)

        self.listbox2.bind('<<ListboxSelect>>', self.show_parameters)

    def draw_figure(self, event):
        selection = self.listbox1.get(tk.ACTIVE)
        self.canvas1.delete("all")
        self.current_figure_coords = None

        # Desenează reperul xOy
        self.draw_axes(self.canvas1)

        if selection == "Segment":
            self.current_figure_coords = self.draw_segment(self.canvas1)
        elif selection == "Patrat":
            self.current_figure_coords = self.draw_square(self.canvas1)
        elif selection == "Cerc":
            self.current_figure_coords = self.draw_circle(self.canvas1)
        elif selection == "Triunghi":
            self.current_figure_coords = self.draw_itriangle(self.canvas1)
        elif selection == "Hexagon":
            self.current_figure_coords = self.draw_hexagon(self.canvas1)
        elif selection == "Dreptunghi":
            self.current_figure_coords = self.draw_dreptunghi(self.canvas1)
        elif selection == "Semiplan Superior":
            self.current_figure_coords = self.draw_plan_superior(self.canvas1)
        elif selection == "Ngon":
            self.ngon_label = ttk.Label(self.frame_text, text="Număr de laturi:")
            self.ngon_label.grid(row=3, column=0, padx=5, pady=5)
            self.ngon_entry = tk.Entry(self.frame_text)
            self.ngon_entry.grid(row=3, column=1, padx=5, pady=5)

            # Crearea unui buton pentru a începe desenarea poligonului
            self.ngon_button = ttk.Button(self.frame_text, text="Desenează Ngon", command=self.draw_ngon)
            self.ngon_button.grid(row=4, column=0, columnspan=2, pady=10)

            # Inițializarea unei variabile pentru a stoca numărul de laturi introdus de utilizator
            self.ngon_sides = None

    def draw_axes(self, canvas):
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.create_line(width // 2, 0, width // 2, height, fill="gray")  # Axa Y
        canvas.create_line(0, height // 2, width, height // 2, fill="gray")  # Axa X

    def draw_segment(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        return canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="blue")

    def draw_square(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        return canvas.create_rectangle(center_x - 50, center_y - 50, center_x + 50, center_y + 50, outline="blue")

    def draw_circle(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        return canvas.create_oval(center_x - 50, center_y - 50, center_x + 50, center_y + 50, outline="blue")

    def draw_itriangle(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        x1, y1 = center_x - 50, center_y + 25
        x2, y2 = center_x, center_y - 50
        x3, y3 = center_x + 50, center_y + 25
        return canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="", outline="blue")

    def draw_hexagon(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        r = 50
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))
        return canvas.create_polygon(points, fill="", outline="blue")

    def draw_dreptunghi(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        return canvas.create_rectangle(center_x - 50, center_y - 25, center_x + 50, center_y + 25, outline="blue")

    def draw_plan_superior(self, canvas):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        return canvas.create_rectangle(0, 0, canvas.winfo_width(), center_y, outline="blue", fill="lightblue")

    def draw_ngon(self):
        # Obțineți numărul de laturi introdus de utilizator din câmpul de introducere
        ngon_sides = int(self.ngon_entry.get())
        # Setează numărul de laturi pentru utilizare ulterioară
        self.ngon_sides = ngon_sides

        # Desenați poligonul pe canvas-ul din prima secțiune folosind numărul de laturi specificat
        self.canvas1.delete("all")
        self.draw_axes(self.canvas1)
        self.draw_ngon_figure(self.canvas1, ngon_sides)

        # Activează opțiunile de transformare pentru poligonul desenat
        self.populate_list2()

    def show_parameters(self, event):
        transformare = self.listbox2.get(tk.ACTIVE)

        if transformare == "Translatie":
            self.entry1_label.config(text="dx:")
            self.entry2_label.config(text="dy:")
            self.entry2_label.grid()
            self.entry2.grid()
        elif transformare == "Omotetie":
            self.entry1_label.config(text="Factor de scalare:")
            self.entry2_label.grid_remove()
            self.entry2.grid_remove()
        elif transformare == "Rotatie":
            self.entry1_label.config(text="Unghi (grade):")
            self.entry2_label.grid_remove()
            self.entry2.grid_remove()


    def apply_transformation(self):
        self.canvas2.delete("all")
        self.draw_axes(self.canvas2)

        figura = self.listbox1.get(tk.ACTIVE)
        transformare = self.listbox2.get(tk.ACTIVE)
        param1 = self.entry1.get()
        param2 = self.entry2.get()
        param3 = self.entry3.get()

        if figura == "Segment":
            self.transform_segment(self.canvas2, transformare, param1, param2)
        elif figura == "Patrat":
            self.transform_square(self.canvas2, transformare, param1, param2)
        elif figura == "Cerc":
            self.transform_circle(self.canvas2, transformare, param1, param2)
        elif figura == "Triunghi":
            self.transform_triangle(self.canvas2, transformare, param1, param2)
        elif figura == "Hexagon":
            self.transform_hexagon(self.canvas2, transformare, param1, param2)
        elif figura == "Dreptunghi":
            self.transform_dreptunghi(self.canvas2, transformare, param1, param2)
        elif figura == "Semiplan Superior":
            self.transform_plan_superior(self.canvas2, transformare, param1, param2)
        elif figura == "Ngon":
            self.transform_ngon(self.canvas2, transformare, param1, param2,param3)

    def transform_segment(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            canvas.create_line(center_x - 50 + dx, center_y + dy, center_x + 50 + dx, center_y + dy, fill="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            canvas.create_line(center_x - 50 * factor, center_y, center_x + 50 * factor, center_y, fill="blue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            x1, y1 = -50, 0
            x2, y2 = 50, 0
            x1r = x1 * math.cos(angle) - y1 * math.sin(angle)
            y1r = x1 * math.sin(angle) + y1 * math.cos(angle)
            x2r = x2 * math.cos(angle) - y2 * math.sin(angle)
            y2r = x2 * math.sin(angle) + y2 * math.cos(angle)
            canvas.create_line(center_x + x1r, center_y - y1r, center_x + x2r, center_y - y2r, fill="blue")

    def transform_square(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            canvas.create_rectangle(center_x - 50 + dx, center_y - 50 + dy, center_x + 50 + dx, center_y + 50 + dy, outline="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            canvas.create_rectangle(center_x - 50 * factor, center_y - 50 * factor, center_x + 50 * factor, center_y + 50 * factor, outline="blue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            coords = [(-50, -50), (50, -50), (50, 50), (-50, 50)]
            new_coords = []
            for (x, y) in coords:
                xr = x * math.cos(angle) - y * math.sin(angle)
                yr = x * math.sin(angle) + y * math.cos(angle)
                new_coords.append((center_x + xr, center_y - yr))
            canvas.create_polygon(new_coords, fill="", outline="blue")

    def transform_circle(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            canvas.create_oval(center_x - 50 + dx, center_y - 50 + dy, center_x + 50 + dx, center_y + 50 + dy, outline="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            canvas.create_oval(center_x - 50 * factor, center_y - 50 * factor, center_x + 50 * factor, center_y + 50 * factor, outline="blue")
        elif transformare == "Rotatie":
            # Rotatia unui cerc în jurul centrului nu schimbă poziția sa
            canvas.create_oval(center_x - 50, center_y - 50, center_x + 50, center_y + 50, outline="blue")

    def transform_triangle(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        x1, y1 = center_x - 50, center_y + 25
        x2, y2 = center_x, center_y - 50
        x3, y3 = center_x + 50, center_y + 25

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            canvas.create_polygon(x1 + dx, y1 + dy, x2 + dx, y2 + dy, x3 + dx, y3 + dy, fill="", outline="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            canvas.create_polygon(center_x - 50 * factor, center_y + 25 * factor, center_x, center_y - 50 * factor, center_x + 50 * factor, center_y + 25 * factor, fill="", outline="blue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            coords = [(-50, 25), (0, -50), (50, 25)]
            new_coords = []
            for (x, y) in coords:
                xr = x * math.cos(angle) - y * math.sin(angle)
                yr = x * math.sin(angle) + y * math.cos(angle)
                new_coords.append((center_x + xr, center_y + yr))
            canvas.create_polygon(new_coords, fill="", outline="blue")

    def transform_hexagon(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        r = 50

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            points = []
            for i in range(6):
                angle = math.radians(60 * i)
                x = center_x + r * math.cos(angle) + dx
                y = center_y + r * math.sin(angle) + dy
                points.append((x, y))
            canvas.create_polygon(points, fill="", outline="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            points = []
            for i in range(6):
                angle = math.radians(60 * i)
                x = (center_x + r * factor * math.cos(angle))
                y = (center_y + r * factor * math.sin(angle))
                points.append((x, y))
            canvas.create_polygon(points, fill="", outline="blue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            points = []
            for i in range(6):
                angle_i = math.radians(60 * i)
                x = r * math.cos(angle_i)
                y = r * math.sin(angle_i)
                xr = x * math.cos(angle) - y * math.sin(angle)
                yr = x * math.sin(angle) + y * math.cos(angle)
                points.append((center_x + xr, center_y - yr))
            canvas.create_polygon(points, fill="", outline="blue")

    def transform_dreptunghi(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            canvas.create_rectangle(center_x - 50 + dx, center_y - 25 + dy, center_x + 50 + dx, center_y + 25 + dy, outline="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            canvas.create_rectangle(center_x - 50 * factor, center_y - 25 * factor, center_x + 50 * factor, center_y + 25 * factor, outline="blue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            coords = [(-50, -25), (50, -25), (50, 25), (-50, 25)]
            new_coords = []
            for (x, y) in coords:
                xr = x * math.cos(angle) - y * math.sin(angle)
                yr = x * math.sin(angle) + y * math.cos(angle)
                new_coords.append((center_x + xr, center_y - yr))
            canvas.create_polygon(new_coords, fill="", outline="blue")

    def transform_plan_superior(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2

        if transformare == "Translatie":
            dx = int(param1)
            dy = int(param2)
            new_center_y = center_y + dy
            canvas.create_rectangle(0, 0, canvas.winfo_width(), new_center_y, outline="blue", fill="lightblue")
        elif transformare == "Omotetie":
            factor = float(param1)
            new_height = center_y * factor
            canvas.create_rectangle(0, 0, canvas.winfo_width(), new_height, outline="blue", fill="lightblue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            # Define original points of the upper half plane
            points = [(-500, -100), (canvas.winfo_width()+100, -100), (canvas.winfo_width()+100, center_y), (-500, center_y)]
            rotated_points = [self.rotate_point(center_x, center_y, x, y, angle) for x, y in points]
            canvas.create_polygon(rotated_points, outline="blue", fill="lightblue")

    def rotate_point(self, cx, cy, x, y, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        x -= cx
        y -= cy
        new_x = x * c - y * s
        new_y = x * s + y * c
        x = new_x + cx
        y = new_y + cy
        return x, y

    def transform_ngon(self, canvas, transformare, param1, param2):
        center_x = canvas.winfo_width() // 2
        center_y = canvas.winfo_height() // 2
        n = int(input("Introduceți numărul de laturi pentru ngon: "))
        r = 50

        points = []
        for i in range(n):
            angle = math.radians(360 / n * i)
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))

        if transformare == "Translatie":
            dx, dy = float(param1), float(param2)
            new_points = [(x + dx, y + dy) for x, y in points]
            canvas.create_polygon(new_points, fill="", outline="blue")
        elif transformare == "Omotetie":
            factor = float(param1)
            new_points = [(x * factor, y * factor) for x, y in points]
            canvas.create_polygon(new_points, fill="", outline="blue")
        elif transformare == "Rotatie":
            angle = math.radians(float(param1))
            new_points = [self.rotate_point(center_x, center_y, x, y, angle) for x, y in points]
            canvas.create_polygon(new_points, fill="", outline="blue")

    def reset_canvas(self):
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.draw_axes(self.canvas1)
        self.draw_axes(self.canvas2)
        self.current_figure_coords = None





if __name__ == "__main__":
    app = Application()
    app.mainloop()
