import tkinter as tk
import random
import math

class GridApp:
    def __init__(self, master):
        self.master = master
        self.grid_size = tk.StringVar(value="10")
        self.cell_size = tk.StringVar(value="70")
        self.obstacle_percentage = tk.StringVar(value="0.15")
        self.start_cell_col = tk.StringVar(value="0")
        self.end_cell_row = tk.StringVar(value="9")
        self.end_cell_col = tk.StringVar(value="9")
        self.obstacle_positions = []

        tk.Label(master, text="Grid Size:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.grid_size).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Cell Size:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.cell_size).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Obstacle Percentage:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.obstacle_percentage).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="Start Cell Col:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.start_cell_col).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="End Cell Row:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.end_cell_row).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(master, text="End Cell Col:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.end_cell_col).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Button(master, text="Update Grid", command=self.update_grid).grid(row=6, column=0, columnspan=2, pady=0)
        tk.Button(master, text="Run Grassfire", command=self.grassfire).grid(row=6, column=3, columnspan=2, pady=0)

        self.error_label = tk.Label(master, text="", fg="red")
        self.error_label.grid(row=7, column=0, columnspan=2)

        self.canvas = tk.Canvas(master, width=1000, height=1000)
        self.canvas.grid(row=0, column=2, rowspan=12, padx=10, pady=10)
        self.update_grid()

    #function used to create grid with initial values and update it when update grid button is pressed
    def update_grid(self):
        size = int(self.grid_size.get())
        cell_size = int(self.cell_size.get())
        obstacle_percentage = float(self.obstacle_percentage.get())
        start_col = int(self.start_cell_col.get())
        end_row = int(self.end_cell_row.get())
        end_col = int(self.end_cell_col.get())
        #reset obstacle postitions
        self.obstacle_positions = []
        # Clear the canvas
        self.canvas.delete("all")

        # Validation Rules
        if size < 8:
            self.show_error("Error: Grid size should be at least 8x8.")
            return

        if not (0.1 <= obstacle_percentage <= 0.2):
            self.show_error("Error: Obstacle percentage should be in the range of 0.1 to 0.2.")
            return

        if not (0 <= start_col < size):
            self.show_error(f"Error: Start Cell Column should be between 0 and {size-1}.")
            return

        if not (end_row > size // 2 and size * 2 / 3 < end_col < size):
            self.show_error("Error: Invalid destination cell indices.")
            return
        
        else:
            self.clear_error()

        # Draw top and left borders
        self.canvas.create_line(0, 0, size * cell_size, 0, fill="black", width=5)
        self.canvas.create_line(0, 0, 0, size * cell_size, fill="black", width=5)

        for i in range(0, size * cell_size, cell_size):
            for j in range(0, size * cell_size, cell_size):
                # Draw cell borders
                self.canvas.create_rectangle(i, j, i + cell_size, j + cell_size, outline="black")

        # Generate obstacles
        for i in range(size):
            for j in range(size):
                #every cell has a chance to be an obstacle if it is not the start or end cell
                if random.random() < obstacle_percentage and (i != 0 or j != start_col) and (i != end_row or j != end_col):
                    self.update_cell_color(i, j, "black")
                    self.obstacle_positions.append((i, j))

        self.update_cell_color(0, start_col, "green")
        self.update_cell_color(end_row, end_col, "red")
        
    def update_cell_color(self, row, col, color):
        cell_size = int(self.cell_size.get())
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if coords == [x1, y1, x2, y2]:
                self.canvas.delete(item)

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def show_error(self, message):
        self.error_label.config(text=message)

    def clear_error(self):
        self.error_label.config(text="")

    def label_cell(self, row, col, text):
        cell_size = int(self.cell_size.get())
        x = col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        self.canvas.create_text(x, y, text=text)
    
    def grassfire(self):
        start_col = int(self.start_cell_col.get())
        end_row = int(self.end_cell_row.get())
        end_col = int(self.end_cell_col.get())
        size = int(self.grid_size.get())
        obstacle_positions = self.obstacle_positions
        print(start_col, end_row, end_col, size, len(obstacle_positions))

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()




           

           







   

        

