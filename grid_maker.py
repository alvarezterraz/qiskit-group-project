#!/usr/bin/env python3
"""
grid_maker.py

Pequeña utilidad Tkinter para **dibujar símbolos “+ / –” en una malla 8 × 8**.

Novedades ↻
-----------
1. Botón **Next**  → guarda el dibujo actual en una lista interna y reinicia el tablero.
2. Botón **Guardar** → exporta **todos** los dibujos acumulados a un único CSV
   donde cada fila es un vector binario (longitud 64) en el orden de índices
   mostrados en pantalla (fila por fila, de izquierda a derecha).

Adicionalmente se puede seguir exportando un PNG de la cuadrícula actual.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image

CELL_SIZE = 50   # píxeles por celda
GRID_SIZE = 8    # 8 × 8 celdas


class GridDrawer(tk.Frame):
    """Widget principal con lienzo y controles."""

    def __init__(self, master: tk.Tk | None = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.state = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)  # 0 = blanco, 1 = negro
        self.samples: list[np.ndarray] = []  # lista de vectores 1‑D (64,)
        self._build_widgets()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------

    def _build_widgets(self):
        canvas_px = CELL_SIZE * GRID_SIZE
        self.canvas = tk.Canvas(self, width=canvas_px, height=canvas_px, bg="white")
        self.canvas.pack(side="left")

        self.rects: dict[tuple[int, int], int] = {}
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                    outline="gray", fill="white",
                )
                idx = row * GRID_SIZE + col
                self.canvas.create_text(
                    x1 + CELL_SIZE / 2,
                    y1 + CELL_SIZE / 2,
                    text=str(idx),
                    fill="gray70",
                    font=("Helvetica", int(CELL_SIZE * 0.3), "bold"),
                )
                self.rects[(row, col)] = rect_id

        # Eventos de ratón
        self.canvas.bind("<Button-1>", self._toggle_cell)
        self.canvas.bind("<B1-Motion>", self._paint_motion)
        self.canvas.bind("<Button-3>", self._erase_cell)
        self.canvas.bind("<B3-Motion>", self._erase_motion)

        # Controles laterales
        panel = tk.Frame(self)
        panel.pack(side="right", fill="y", padx=10)
        tk.Button(panel, text="Next", command=self._next).pack(fill="x", pady=4)
        tk.Button(panel, text="Guardar", command=self._save_all).pack(fill="x", pady=4)
        tk.Button(panel, text="PNG actual", command=self._save_png_current).pack(fill="x", pady=4)
        tk.Button(panel, text="Reiniciar", command=self._reset).pack(fill="x", pady=4)
        tk.Button(panel, text="Salir", command=self.master.destroy).pack(side="bottom", fill="x", pady=4)

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

    def _coords_to_cell(self, event):
        col, row = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return int(row), int(col)
        return None

    # ----------------- Pintar / Borrar -------------------------------

    def _toggle_cell(self, event):
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            self.state[r, c] ^= 1
            self.canvas.itemconfig(self.rects[cell], fill=("black" if self.state[r, c] else "white"))

    def _paint_motion(self, event):
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            if not self.state[r, c]:
                self.state[r, c] = 1
                self.canvas.itemconfig(self.rects[cell], fill="black")

    def _erase_cell(self, event):
        cell = self._coords_to_cell(event)
        if cell:
            r, c = cell
            if self.state[r, c]:
                self.state[r, c] = 0
                self.canvas.itemconfig(self.rects[cell], fill="white")

    def _erase_motion(self, event):
        self._erase_cell(event)

    # ----------------- Lógica Next / Guardar -------------------------

    def _next(self):
        """Guarda el dibujo actual en la lista y reinicia el lienzo."""
        flat = self.state.flatten().copy()
        if flat.any():
            self.samples.append(flat)
            self._reset(update_msg=False)
            messagebox.showinfo("Next", f"Dibujo #{len(self.samples)} almacenado. Puedes crear otro.")
        else:
            messagebox.showwarning("Vacío", "El dibujo está vacío. Dibuja algo antes de pulsar Next.")

    def _save_all(self):
        """Guarda TODOS los dibujos almacenados en un CSV (una fila = un vector)."""
        if not self.samples and not self.state.any():
            messagebox.showwarning("Nada que guardar", "No hay dibujos almacenados.")
            return
        # Asegurarse de incluir el estado actual si no está vacío y no se ha pulsado Next
        if self.state.any():
            self.samples.append(self.state.flatten().copy())
        fname = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV (vector por fila)", "*.csv")],
            title="Guardar todos los dibujos en…",
        )
        if not fname:
            return
        try:
            mat = np.vstack(self.samples)
            np.savetxt(fname, mat, fmt="%d", delimiter=",")
            messagebox.showinfo("Guardado", f"{len(self.samples)} dibujos guardados en {fname}")
            self.samples.clear()  # vaciar la lista tras guardar
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar: {exc}")

    def _save_png_current(self):
        """Guarda únicamente el dibujo actual como imagen PNG."""
        fname = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")],
            title="Guardar imagen actual en…",
        )
        if not fname:
            return
        try:
            img = Image.fromarray(255 * (1 - self.state).astype(np.uint8))
            img.save(fname)
            messagebox.showinfo("Guardado", f"PNG guardado en {fname}")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar: {exc}")

    # ----------------- Reiniciar ---------------------------

    def _reset(self, update_msg: bool = True):
        self.state.fill(0)
        for rect in self.rects.values():
            self.canvas.itemconfig(rect, fill="white")
        if update_msg:
            messagebox.showinfo("Reiniciar", "Lienzo limpio.")


# --------------------------------------------------------------------

def main():
    root = tk.Tk()
    root.title("Dibujador 8×8 [+ / -] — múltiples muestras")
    GridDrawer(master=root)
    root.mainloop()


if __name__ == "__main__":
    main()
