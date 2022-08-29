import tkinter as tk
import taylor_series_plotter as tsp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

FUNC_FONT_STYLE = ('Arial', 24)
DEFAULT_FONT_STYLE = ('Arial', 20)
SMALL_FONT_SIZE = ('Arial', 16)
LARGE_FONT_SIZE = ('Arial', 16)

LIGHT_GRAY = '#F5F5F5'
DISPLAY_FRAME = '#fbfcfc'
WHITE = '#FFFFFF'
LABEL_COLOR = '#25265E'
OFF_WHITE = '#F8FAFF'
LIGHT_BLUE = '#d6eaf8'

class Calculator:
    
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.geometry("625x800")
        self.window.resizable(0, 0)
        self.window.title("Compare Taylor Series")

        self.total_expression = ''
        self.current_expression = ''
        self.fig = ''

        self.taylor_series = tsp.Taylor_Series_Plotter()

        self.graph_frame = self.create_graph_frame()
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_label, self.label = self.create_display_label()

        self.functions = { 'sin': (0, 4), 'tan': (2, 4), 'log': (3, 4),
                        'cos': (1, 4), 'e': (4, 4)}

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            3: (3, 1), 2: (3, 2), 1: (3, 3),
            0: (4, 1) }

        for x in range(5):
            if x:
                self.buttons_frame.rowconfigure(x, weight = 1)
                self.buttons_frame.columnconfigure(x, weight = 1)
            else:
                self.buttons_frame.rowconfigure(x, weight = 1)


        self.create_function_buttons()
        self.create_digit_buttons()
        self.create_clear_button()
        self.create_go_button()
        self.create_plot_button()

    def run(self):
        self.window.mainloop()

    def create_display_label(self):
        total_label = tk.Label(self.display_frame, text = self.total_expression, 
                                anchor = tk.W, bg = DISPLAY_FRAME, fg = LABEL_COLOR,
                                font = SMALL_FONT_SIZE)
        total_label.pack(expand = True, fill = 'both')

        label = tk.Label(self.display_frame, text = self.current_expression, 
                            anchor = tk.W, bg = DISPLAY_FRAME, fg = LABEL_COLOR,
                            font = LARGE_FONT_SIZE)
        label.pack(expand = True, fill = 'both')

        return total_label, label

    def create_graph_frame(self):
        frame = tk.Frame(self.window, height = 400, bg = LIGHT_GRAY)
        frame.pack(expand = True, fill = 'both')
        return frame
    
    def create_display_frame(self):
        frame = tk.Frame(self.window, height = 400, bg = DISPLAY_FRAME)
        frame.pack(expand = True, fill ='both')
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.window, height = 150)
        frame.pack(expand = True, fill = 'both')
        return frame

    def create_function_buttons(self):
        for func, grid_value in self.functions.items():
            button = tk.Button(self.buttons_frame, text = func, bg = LIGHT_BLUE,
                                fg = LABEL_COLOR, font = FUNC_FONT_STYLE, borderwidth = 0,
                                command = lambda x = func: self.add_to_expression(x))
            button.grid(row = grid_value[0], column = grid_value[1], sticky = tk.NSEW)

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text = str(digit),
                                 bg = LIGHT_BLUE, fg = LABEL_COLOR, font = FUNC_FONT_STYLE,
                                 borderwidth = 0, command = lambda x = digit: self.get_number_of_terms(x))
            button.grid(row = grid_value[0], column = grid_value[1], sticky = tk.NSEW)


    def create_go_button(self):
        button = tk.Button(self.buttons_frame, text = 'GO', bg = OFF_WHITE, 
                            fg = LABEL_COLOR, font = DEFAULT_FONT_STYLE,
                            borderwidth = 0, command = self.get_func)
        button.grid(row = 4, column = 2, sticky = tk.NSEW)

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text = 'Clear', bg = OFF_WHITE, 
                            fg = LABEL_COLOR, font = DEFAULT_FONT_STYLE,
                            borderwidth = 0, command = self.clear_display)
        button.grid(row = 0, column = 1, columnspan = 3, sticky = tk.NSEW)

    def create_plot_button(self):
        button = tk.Button(self.buttons_frame, text = 'Plot', bg = OFF_WHITE, 
                            fg = LABEL_COLOR, font = DEFAULT_FONT_STYLE,
                            borderwidth = 0, command = self.plot_graph)
        button.grid(row = 4, column = 3, sticky = tk.NSEW)

    def update_total_label(self):
        self.total_label.config(text = self.total_expression)

    def update_label(self):
        self.label.config(text = self.current_expression)

    def add_to_expression(self, value):
        self.current_expression += value
        self.update_label()
    
    def clear_display(self):
        self.taylor_series.order = ''
        plt.close(self.fig)
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def get_number_of_terms(self, value):
        self.taylor_series.order +=  str(value)
        self.current_expression += str(value)
        self.update_label()

    def plot_graph(self):
        self.taylor_series.order = int(self.taylor_series.order)
        self.fig = self.taylor_series.generate_graph()
        canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row = 0, column = 0, sticky = tk.NSEW)
        
        self.list_attributes()


    
    def list_attributes(self):
        derivatives = self.taylor_series.derivatives
        terms = self.taylor_series.generate_taylor_terms(derivatives)
        polynomial = self.taylor_series.generate_taylor_polynomial(terms)
        
        self.taylor_series.format_poly(str(polynomial))

        self.current_expression = f"Polynomial: {polynomial}"
        self.update_label()

    def get_func(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        self.taylor_series.func = self.total_expression

        self.current_expression = "Input number of terms in approximation: "
        self.update_label()
        

        self.total_expression = ""


if __name__ == '__main__':
    calc = Calculator()
    calc.run()
