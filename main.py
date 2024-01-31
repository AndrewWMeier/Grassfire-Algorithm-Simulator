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
        self.speed = tk.StringVar(value="100")
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

        tk.Label(master, text="Speed:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(master, textvariable=self.speed).grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Button(master, text="Update/Reset Grid", command=self.update_grid).grid(row=7, column=0, columnspan=2, pady=0)
        tk.Button(master, text="Run Grassfire", command=self.grassfire).grid(row=7, column=3, columnspan=2, pady=0)

        self.error_label = tk.Label(master, text="", fg="red")
        self.error_label.grid(row=8, column=0, columnspan=2)

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
        #clear the canvas
        self.canvas.delete("all")

        #validation Rules
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

        #draw top and left borders
        self.canvas.create_line(0, 0, size * cell_size, 0, fill="black", width=5)
        self.canvas.create_line(0, 0, 0, size * cell_size, fill="black", width=5)

        for i in range(0, size * cell_size, cell_size):
            for j in range(0, size * cell_size, cell_size):
                #draw cell borders
                self.canvas.create_rectangle(i, j, i + cell_size, j + cell_size, outline="black")

        #generate obstacles and start and end cells
        for i in range(size):
            for j in range(size):
                #every cell has a chance to be an obstacle if it is not the start or end cell
                if random.random() < obstacle_percentage and (i != 0 or j != start_col) and (i != end_row or j != end_col):
                    self.update_cell_color(i, j, "black")
                    self.obstacle_positions.append([i, j])
        self.update_cell_color(0, start_col, "green")
        self.update_cell_color(end_row, end_col, "red")
        
    #function to update cell color
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

    #writes number in the center of the cell
    def label_cell(self, row, col, text):
        cell_size = int(self.cell_size.get())
        x = col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        self.canvas.create_text(x, y, text=text)

    #function to write numbers in the cells with a delay
    def label_cells_with_delay(self, grid, obstacle_positions, size, speed):
            for row in range(size):
                for col in range(size):
                    cell_value = grid[row][col]
                    if (row, col) not in obstacle_positions:
                        #label cells with a delay
                        self.master.after(cell_value * speed, self.label_cell, row, col, cell_value)
    
    #function to draw the path with a delay 
    def draw_path(self, path, start_position, end_position):
        for step, (row, col) in enumerate(path):
            #making sure not to color start and end cells
            #as each cell is colored redraw the value in the cell
            if (row, col) != start_position and (row, col) != end_position:
                self.master.after(step * 100, self.update_cell_color, row, col, "yellow")
                self.master.after(step * 100, self.label_cell, row, col, step)
            
          
    
    #used by grassfire to find the path        
    def find_path(self, grid, end_position):
        path = []
        current_position = end_position
        while grid[current_position[0]][current_position[1]] != 0:
            path.append(current_position)
            for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_row = current_position[0] + neighbor[0]
                neighbor_col = current_position[1] + neighbor[1]
                if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]) and grid[neighbor_row][neighbor_col] == grid[current_position[0]][current_position[1]] - 1:
                    current_position = (neighbor_row, neighbor_col)
                    break
        path.append(current_position)
        return path[::-1]
    
    def grassfire(self):
        self.show_error("Running Grassfire...")

        #get grid size and obstacle positions
        size = int(self.grid_size.get())
        obstacle_positions = {(row, col) for row, col in self.obstacle_positions}
        print("obstacle postions format row, col: " + str(obstacle_positions))

        #get start and end positions into tuples
        start_position = (0, int(self.start_cell_col.get()))
        end_position = (int(self.end_cell_row.get()), int(self.end_cell_col.get()))

        #initialize the 2D grid array with -1 as the value for all cells
        grid = [[-1 for _ in range(size)] for _ in range(size)]

        #initialize the start cell with 0
        start_row, start_col = start_position
        grid[start_row][start_col] = 0

        #initialize the queue with the start cell
        queue = [(start_row, start_col)]

        #perform the grassfire algorithm
        while queue:
            current_row, current_col = queue.pop(0)

            #check the neighbors of the current position
            for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor_row = current_row + neighbor[0]
                neighbor_col = current_col + neighbor[1]

                #check if the neighbor is within the grid boundaries
                if 0 <= neighbor_row < size and 0 <= neighbor_col < size:
                    #check if the neighbor is not an obstacle and has not been visited yet
                    if grid[neighbor_row][neighbor_col] == -1 and (neighbor_row, neighbor_col) not in obstacle_positions:
                        #update the neighbor's value in the grid
                        grid[neighbor_row][neighbor_col] = grid[current_row][current_col] + 1
                        #add the neighbor to the queue for further exploration
                        queue.append((neighbor_row, neighbor_col))

        # Find the path and print it
        path = self.find_path(grid, end_position)
        print("Path:", path)

        #label empty cells with a delay
        self.label_cells_with_delay(grid, obstacle_positions, size, int(self.speed.get()))

        #draw path after cells are labeled
        self.master.after(len(path) * int(self.speed.get()), self.draw_path, path, start_position, end_position)
        
        #after cells are labeled and path is drawn, give done msg
        self.master.after(len(path) * int(self.speed.get()) + 1000, self.show_error, "Grassfire Done! Reset the grid to run again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()




           

           







   

        

