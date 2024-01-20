import tkinter as tk
import random 
import math

class GridApp:
    def __init__(self, master, rows, cols, cell_size, obstacle_percentage):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.obstacle_percentage = obstacle_percentage

        # Create a Canvas widget
        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        # Draw the grid lines
        self.draw_grid()

        #generate starting cell
        self.generate_starting_cell(4)

        #generate obstacles
        self.generate_obstacles(0.15)

        #generate goal cell
        self.generate_goal_cell(7,7)

     

        #test update_cell_color
        # self.master.after(1000, lambda: self.update_cell_color(5, 5, "green"))
        # self.master.after(2000, lambda: self.update_cell_color(6, 6, "yellow"))
        # self.master.after(3000, lambda: self.update_cell_color(7, 7, "orange"))

    def draw_grid(self):
        for i in range(0, self.cols * self.cell_size, self.cell_size):
            for j in range(0, self.rows * self.cell_size, self.cell_size):
                #Draw cell borders
                self.canvas.create_rectangle(i, j, i + self.cell_size, j + self.cell_size, outline="black")

    def label_cell(self, row, col, value):
        #Calculate the center of the specified cell
        center_x = col * self.cell_size + self.cell_size // 2
        center_y = row * self.cell_size + self.cell_size // 2

        # Add text to the center of the cell with the specified value
        self.canvas.create_text(center_x, center_y, text=str(value))

    def update_cell_color(self, row, col, color):
        #Calculate the coordinates of the specified cell
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        #Delete any existing rectangle at the specified coordinates
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            if coords == [x1, y1, x2, y2]:
                self.canvas.delete(item)

        #Change the color of the specified cell
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def generate_obstacles(self, obstacle_percentage):
        #iterate through grid and each cell has a probability of being an obstacle 
        for i in range(0, self.cols):
            for j in range(0, self.rows):
                if random.random() < obstacle_percentage:
                    self.update_cell_color(i, j, "black")
        
    def generate_starting_cell(self, row_position):
        #generate starting cell
        if row_position < self.cols:
            self.update_cell_color(0, row_position, "green")
        #make them re enter (later)
            
    def generate_goal_cell(self, row, col):
        #Ensure the row index is greater than half of the number of rows
        rows = self.rows
        if row <= rows // 2:
            row = rows // 2 + 1
        #Ensure the column index is greater than 2/3 of the number of columns
        cols = self.cols
        min_col = math.ceil(cols * 2 / 3)
        if col <= min_col:
            col = min_col + 1
        #Update the color of the specified cell
        self.update_cell_color(row, col, "red")  

        
if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root, rows=10, cols=10, cell_size=50,obstacle_percentage=0.15)
    root.mainloop()


