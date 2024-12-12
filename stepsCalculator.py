import tkinter as tk
from tkinter import ttk, messagebox


class TrailBuilder:
    def __init__(self):
        self.height = 0.0
        self.distance = 0.0
        self.slope_percent = 0.0
        self.num_steps = 3
        self.step_height = 0.0
        self.step_length = 0.0
        self.trail_length = 0.0
        self.num_podiums = 1
        self.podiums_H = 0.026
        self.podiums_L = 1.3
        self.result_list = []

    def get_inputs(self, height, distance):
        try:
            self.height = float(height)
            self.distance = float(distance)
        except ValueError:
            raise ValueError("Please enter valid numbers.")

    def calculate_slope(self):
        if self.distance != 0:
            self.slope_percent = (self.height / self.distance) * 100
        else:
            raise ValueError("Distance cannot be zero.")

    def calculate_steps(self):
        self.result_list = []
        if self.slope_percent > 4.5:
            for i in range(3, 13):
                counter = 0.5
                self.initStairs(True, 0)
                self.calculateNewSlope(i)
                for x in range(10, 15):
                    self.initStairs(False, counter)
                    counter += 0.5
                    self.calculateNewSlope(i)

    def initStairs(self, flag, dis):
        if flag:
            self.step_height = 15 / 100
            self.step_length = 31 / 100
        else:
            self.step_height = (15 - dis) / 100
            self.step_length = (62 / 100) - 2 * self.step_height

    def calculateNewSlope(self, steps):
        new_height = self.height - (self.step_height * steps)
        new_length = self.distance - (self.step_length * steps)
        new_slope = new_height / new_length * 100
        flag = 4.5 > new_slope > 0
        temp_result = {
            'stairs': steps,
            'slope': new_slope,
            'step_H': self.step_height,
            'step_b': self.step_length,
            'result': flag
        }
        if flag:
            self.result_list.append(temp_result)
            # self.check_padast(temp_result)


    def display_results(self):
        results = []
        counter = 0
        for i, item in enumerate(self.result_list):
            if item["result"]:
                counter = counter + 1
                results.append(f"Option {counter}: Steps: {item['stairs']}, Slope: {item['slope']:.2f}%")
        if not results:
            results.append("No valid results found.")
        return results

    def get_result_details(self, index):
        if 0 <= index < len(self.result_list):
            item = self.result_list[index]
            print(item)
            return (f"Steps: {item['stairs']}\n"
                    f"Slope: {item['slope']:.2f}%\n"
                    f"Step Height: {item['step_H'] * 100:.2f} cm\n"
                    f"Step Length: {item['step_b'] * 100:.2f} cm")
        else:
            return "Invalid index."


class TrailBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trail Builder Calculator")

        self.builder = TrailBuilder()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Enter height between 2 points [m]:").grid(row=0, column=0, padx=10, pady=10)
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.root, text="Enter distance between 2 points [m]:").grid(row=1, column=0, padx=10, pady=10)
        self.distance_entry = ttk.Entry(self.root)
        self.distance_entry.grid(row=1, column=1, padx=10, pady=10)

        self.calculate_button = ttk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.results_listbox = tk.Listbox(self.root, height=10, width=50)
        self.results_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.results_listbox.bind("<<ListboxSelect>>", self.show_details)

        self.details_text = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
        self.details_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def calculate(self):
        height = self.height_entry.get()
        distance = self.distance_entry.get()

        try:
            self.builder.get_inputs(height, distance)
            self.builder.calculate_slope()
            self.builder.calculate_steps()
            results = self.builder.display_results()

            self.results_listbox.delete(0, tk.END)
            for result in results:
                self.results_listbox.insert(tk.END, result)

            self.details_text.config(state=tk.DISABLED)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def show_details(self, event):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            details = self.builder.get_result_details(index)
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, details)
            self.details_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = TrailBuilderGUI(root)
    root.mainloop()
