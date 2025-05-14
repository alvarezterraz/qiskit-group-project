# Symbols maker - Usage Instructions
# -----------------------------------
# This program lets you draw on an 8x8 symbols using your mouse.
# Left-click and drag to draw (black), right-click and drag to erase (white).
# Use the radio buttons to label your drawing as a circle (0) or a cross (1). The label is saved as the last element of the vector.
# Click "Next" to save the current drawing and start a new one.
# Click "Save CSV" to export all saved drawings (including the label) to a CSV file.
# Click "Save PNG" to save the current drawing as a PNG image.
# Click "Reset" to clear the grid, or "Exit" to close the application.

import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
from PIL import Image

CELL_SIZE = 50
GRID_SIZE = 5

class GridDrawer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # Initialize an 8x8 grid state (0 = white, 1 = black)
        self.state = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        # List of sample vectors (length 65: 64 pixels + 1 shape label)
        self.samples = []
        # Shape label: 0 = circle, 1 = cross
        self.shape_var = tk.IntVar(value=0)
        self._build_widgets()

    def _build_widgets(self):
        self.pack()
        # Canvas for the grid drawing
        self.canvas = tk.Canvas(
            self,
            width=CELL_SIZE * GRID_SIZE,
            height=CELL_SIZE * GRID_SIZE,
            bg='white'
        )
        self.canvas.grid(row=0, column=0, rowspan=6)
        self._draw_grid()

        # Control panel
        tk.Label(self, text="Shape label:").grid(row=0, column=1, sticky='w')
        tk.Radiobutton(self, text='Circle', variable=self.shape_var, value=0).grid(row=1, column=1, sticky='w')
        tk.Radiobutton(self, text='Cross', variable=self.shape_var, value=1).grid(row=2, column=1, sticky='w')

        tk.Button(self, text="Next", command=self._next).grid(row=3, column=1, pady=5)
        tk.Button(self, text="Save CSV", command=self._save_all).grid(row=4, column=1, pady=5)
        tk.Button(self, text="Save PNG", command=self._save_png_current).grid(row=5, column=1, pady=5)
        tk.Button(self, text="Reset", command=self._reset).grid(row=6, column=0, pady=5)
        tk.Button(self, text="Exit", command=self.master.destroy).grid(row=6, column=1, pady=5)

        # Mouse events for drawing
        self.canvas.bind('<Button-1>', self._toggle_cell)
        self.canvas.bind('<B1-Motion>', self._paint_motion)
        self.canvas.bind('<Button-3>', self._erase_cell)
        self.canvas.bind('<B3-Motion>', self._erase_motion)

    def _draw_grid(self):
        # Draw grid lines and cell indices
        self.rects = {}
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline='gray')
                # Show cell index in light gray
                self.canvas.create_text(
                    x1 + CELL_SIZE/2,
                    y1 + CELL_SIZE/2,
                    text=str(row * GRID_SIZE + col),
                    fill='lightgray'
                )
                self.rects[(row, col)] = rect

    def _coords_to_cell(self, event):
        # Convert pixel coordinates to grid cell (row, col)
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
        return None

    def _toggle_cell(self, event):
        # Toggle cell color on click
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            self.state[r, c] = 1 - self.state[r, c]
            fill_color = 'black' if self.state[r, c] else 'white'
            self.canvas.itemconfig(self.rects[(r, c)], fill=fill_color)

    def _paint_motion(self, event):
        # Paint cells black on drag with left button
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            self.state[r, c] = 1
            self.canvas.itemconfig(self.rects[(r, c)], fill='black')

    def _erase_cell(self, event):
        # Erase cell (set to white) on right click
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            self.state[r, c] = 0
            self.canvas.itemconfig(self.rects[(r, c)], fill='white')

    def _erase_motion(self, event):
        # Erase cells on drag with right button
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            self.state[r, c] = 0
            self.canvas.itemconfig(self.rects[(r, c)], fill='white')

    def _next(self):
        # Save current sample and reset if any cell is filled
        if not self.state.any():
            messagebox.showwarning("Warning", "The sample is empty.")
            return
        vec = self.state.flatten().tolist()
        # Append shape label (circle=0, cross=1)
        vec.append(self.shape_var.get())
        self.samples.append(vec)
        messagebox.showinfo("Info", f"Sample saved. Total samples: {len(self.samples)}")
        self._reset()

    def _save_all(self):
        # Include current sample if not empty
        if self.state.any():
            vec = self.state.flatten().tolist()
            vec.append(self.shape_var.get())
            self.samples.append(vec)
        if not self.samples:
            messagebox.showwarning("Warning", "No samples to save.")
            return
        # Ask for CSV file path
        path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv')]
        )
        if path:
            # Save samples as CSV
            np.savetxt(path, np.array(self.samples, dtype=int), fmt='%d', delimiter=',')
            messagebox.showinfo("Info", f"Data saved to {path}")

    def _save_png_current(self):
        # Save current grid as PNG
        if not self.state.any():
            messagebox.showwarning("Warning", "The sample is empty.")
            return
        img = Image.fromarray((self.state * 255).astype('uint8'))
        img = img.resize((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), Image.NEAREST)
        path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[('PNG files', '*.png')]
        )
        if path:
            img.save(path)
            messagebox.showinfo("Info", f"Image saved to {path}")

    def _reset(self):
        # Reset grid and shape label to defaults
        self.state.fill(0)
        self.shape_var.set(0)
        for rect_id in self.rects.values():
            self.canvas.itemconfig(rect_id, fill='white')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Grid Collector')
    app = GridDrawer(master=root)
    app.mainloop()

