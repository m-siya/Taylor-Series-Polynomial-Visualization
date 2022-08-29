import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class Taylor_Series_Plotter:

    def __init__(self):
        
        self.t, self.a = sp.symbols('t a')
        self.approx_point = 0
        self.func = ''
        self.order = ''

        self.derivatives = ''
    

    def generate_derivatives(self, func, derivatives = None):
        
        if derivatives is None:
            derivatives = [func.subs({self.t: self.a})]
        
        if len(derivatives) > self.order:
            return derivatives
        
        derivative = func.diff(self.t)
        derivatives.append(derivative.subs({self.t: self.a}))

        return self.generate_derivatives(derivative, derivatives)

    def generate_taylor_terms(self, derivatives):
        terms = []
        for i in range(len(derivatives)):
            terms.append(derivatives[i].subs({self.a: self.approx_point}) / sp.factorial(i) * (self.t - self.approx_point) ** i)
        
        return terms

    def generate_taylor_polynomial(self, terms):
        polynomial = terms[0]

        for term in terms[1:]:
            if term:
                polynomial += term
        
        print(polynomial)
        return polynomial


    def generate_graph(self):
        xlist = np.arange(-2*np.pi,2*np.pi,0.1)

        #accomodate for func being log, have to approximate at pi
        available_functions = {'sin' : sp.sin(self.t), 
							'cos' : sp.cos(self.t),
							'tan' : sp.tan(self.t),
							'e' : sp.exp(self.t),
							'log' : sp.log(self.t)
							}

        f = available_functions[self.func]
        
        if f == available_functions['log']:
            xlist = np.arange(0.01,2*np.pi,0.1)
            self.approx_point = np.pi

        self.derivatives = derivatives = self.generate_derivatives(func=f)
        terms = self.generate_taylor_terms(derivatives)
        polynomial = self.generate_taylor_polynomial(terms)

        #initialize plot
        fig, ax = plt.subplots()
        ax.set(xlabel = 'Angles in Multiples of $\pi $ ', ylabel = 'y', title = "Taylor polynomial approximation")
        legend = []

        
        ax.plot(xlist,[polynomial.subs({self.t: point}) for point in xlist])
        
        legend.append(f"Taylor Approximation - {self.order} terms")
        
        #now plot the original func
        ax.plot(xlist,[f.subs({self.t:point}) for point in xlist])
        legend.append(f"f(x)")
        
        if f == available_functions['log']:
            ax.set_ylim([-5,3])
        else:
            ax.set_ylim([-7,4])
        
        #set up the legend
        
        ax.legend(legend)	
        ax.grid()
        plt.rcParams['figure.figsize'] = [6.4, 4.5]

        return fig

    def format_poly(self, polynomial):
        
        polynomial = polynomial.replace('**', '^')
        x = sp.Symbol(polynomial)
        print(x)

    
        
        


        



