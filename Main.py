import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import functools

# --- Decorator Pattern for Measuring Execution Time ---
def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# --- Algorithm Implementations with Strategy Pattern ---
class SortStrategy:
    color = 'blue'
    def sort(self, data):
        raise NotImplementedError

class BubbleSort(SortStrategy):
    color = 'red'
    @timing_decorator
    def sort(self, data):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    yield data

class InsertionSort(SortStrategy):
    color = 'green'
    @timing_decorator
    def sort(self, data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
                yield data
            data[j + 1] = key
            yield data

class MergeSort(SortStrategy):
    color = 'orange'
    @timing_decorator
    def sort(self, data):
        yield from self._merge_sort(data, 0, len(data) - 1)

    def _merge_sort(self, data, left, right):
        if left < right:
            mid = (left + right) // 2
            yield from self._merge_sort(data, left, mid)
            yield from self._merge_sort(data, mid + 1, right)
            yield from self._merge(data, left, mid, right)

    def _merge(self, data, left, mid, right):
        left_copy = data[left:mid + 1]
        right_copy = data[mid + 1:right + 1]
        l = r = 0
        for i in range(left, right + 1):
            if l < len(left_copy) and (r >= len(right_copy) or left_copy[l] <= right_copy[r]):
                data[i] = left_copy[l]
                l += 1
            else:
                data[i] = right_copy[r]
                r += 1
            yield data

class QuickSort(SortStrategy):
    color = 'purple'
    @timing_decorator
    def sort(self, data):
        yield from self._quick_sort(data, 0, len(data) - 1)

    def _quick_sort(self, data, low, high):
        if low < high:
            pivot_index = self._partition(data, low, high)
            yield data
            yield from self._quick_sort(data, low, pivot_index - 1)
            yield from self._quick_sort(data, pivot_index + 1, high)

    def _partition(self, data, low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
        data[i + 1], data[high] = data[high], data[i + 1]
        return i + 1

class SelectionSort(SortStrategy):
    color = 'cyan'
    @timing_decorator
    def sort(self, data):
        n = len(data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            yield data

# --- Context Class ---
class AlgorithmContext:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self.strategy = strategy

    def execute(self, data):
        return self.strategy.sort(data)

# --- GUI Class ---
class AlgorithmAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Analyzer with Patterns")

        self.canvas = tk.Canvas(root, width=600, height=300, bg='white')
        self.canvas.pack(pady=20)

        self.data = []
        self.current_color = 'blue'

        controls_frame = ttk.Frame(root)
        controls_frame.pack()

        ttk.Label(controls_frame, text="Choose Algorithm:").grid(row=0, column=0)
        self.algo_menu = ttk.Combobox(controls_frame, values=[
            "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Selection Sort"])
        self.algo_menu.grid(row=0, column=1)
        self.algo_menu.current(0)

        ttk.Button(controls_frame, text="Generate Data", command=self.generate_data).grid(row=0, column=2, padx=5)
        ttk.Button(controls_frame, text="Start", command=self.start_sort).grid(row=0, column=3, padx=5)

    def generate_data(self):
        import random
        self.data = [random.randint(10, 100) for _ in range(30)]
        self.draw_data(self.data)

    def draw_data(self, data, colorArray=None):
        self.canvas.delete("all")
        c_height = 300
        c_width = 600
        x_width = c_width / (len(data) + 1)
        offset = 30
        spacing = 10
        normalized_data = [i / max(data) for i in data]

        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = c_height - height * 250
            x1 = (i + 1) * x_width + offset
            y1 = c_height
            color = self.current_color if not colorArray else colorArray[i]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        self.root.update_idletasks()

    def start_sort(self):
        if not self.data:
            messagebox.showerror("Error", "Please generate data first")
            return

        algo = self.algo_menu.get()
        if algo == "Bubble Sort":
            strategy = BubbleSort()
        elif algo == "Insertion Sort":
            strategy = InsertionSort()
        elif algo == "Merge Sort":
            strategy = MergeSort()
        elif algo == "Quick Sort":
            strategy = QuickSort()
        elif algo == "Selection Sort":
            strategy = SelectionSort()
        else:
            messagebox.showerror("Error", "Unknown algorithm selected")
            return

        self.current_color = strategy.color
        context = AlgorithmContext(strategy)
        threading.Thread(target=self.run_sort, args=(context,)).start()

    def run_sort(self, context):
        generator = context.execute(self.data.copy())
        for data in generator:
            self.draw_data(data)
            time.sleep(0.1)

# --- Run the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmAnalyzer(root)
    root.mainloop()