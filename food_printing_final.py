import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.filedialog as tkFileDialog


class EpicycloidGUI:
    def __init__(self, master):
        self.master = master
        master.title('Epicycloid with Large and Small Circles')

        # Initialize some parameters
        self.a_init = self.a = 5
        self.b_init = self.b = 2
        self.d_init = self.d = 6
        self.layers = 1
        self.active_syringe = 0    # just added

        # Create the Tkinter window and canvas
        self.canvas = tk.Canvas(master, width=800, height=800)
        self.canvas.pack()

        # Create the Matplotlib figure and plot the initial curve
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.t_init = np.linspace(0, 2 * np.pi * self.b_init / np.gcd(self.a_init, self.b_init), 1000)
        self.x_init, self.y_init = self.epicycloid(self.a_init, self.b_init, self.d_init, self.t_init)
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_init, self.y_init)
        
        # Embed the Matplotlib plot into the canvas
        self.plot_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.plot_widget.draw()
        self.plot_widget.get_tk_widget().pack()

        # Create the sliders
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.slider_a = tk.Scale(self.frame, from_=1, to=50, orient=tk.HORIZONTAL, label='a', length=400, resolution=1, command=self.update_a)
        self.slider_b = tk.Scale(self.frame, from_=1, to=50, orient=tk.HORIZONTAL, label='b', length=400, resolution=1, command=self.update_b)
        self.slider_d = tk.Scale(self.frame, from_=1, to=50, orient=tk.HORIZONTAL, label='d', length=400, resolution=1, command=self.update_d)
        self.slider_layers = tk.Scale(self.frame, from_=1, to=50, orient=tk.HORIZONTAL, label='layer', length=400, resolution=1, command=self.update_layers)
        self.slider_a.set(self.a_init)
        self.slider_b.set(self.b_init)
        self.slider_d.set(self.d_init)
        self.slider_layers.set(self.layers)
        self.slider_a.pack()
        self.slider_b.pack()
        self.slider_d.pack()
        self.slider_layers.pack()
        
        # Create a frame for the buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        # Create the save button
        self.save_button = tk.Button(self.button_frame, text='Save Figure', command=self.save_fig)
        self.save_button.config(font=('Arial', 12), width=15, height=1)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create the Gcode button
        self.gcode_button = tk.Button(self.button_frame, text='Generate Gcode', command=self.generate_gcode)
        self.gcode_button.config(font=('Arial', 12), width=15, height=1)
        self.gcode_button.pack(side=tk.LEFT, padx=10, pady=10)

    def epicycloid(self, big_radius: float, small_radius: float, distance_from_center: float, t: np.ndarray) -> tuple:
        """
        Calculate the (x, y) coordinates of an epicycloid curve.

        Parameters:
        big_radius (float): The radius of the large circle.
        small_radius (float): The radius of the small circle.
        distance_from_center (float): The distance from the center of the large circle to the center of the small circle.
        t (np.ndarray): An array of angles for the curve.

        Returns:
        tuple: A tuple containing the (x, y) coordinates of the curve.
        """
        x = (big_radius + small_radius) * np.cos(t) - distance_from_center * np.cos(((big_radius + small_radius) / small_radius) * t)
        y = (big_radius + small_radius) * np.sin(t) - distance_from_center * np.sin(((big_radius + small_radius) / small_radius) * t)
        return x, y
    


    def update_a(self, val: int):
        self.a = int(val)
        self.update_plot()

    def update_b(self, val: int):
        self.b = int(val)
        self.update_plot()
    
    def update_d(self, val: int):
        self.d = int(val)
        self.update_plot()
    
    def update_layers(self, val: int):
        self.layers = int(val)
        
    def update_plot(self):
        self.ax.clear()
        t = np.linspace(0, 2 * np.pi * self.b / np.gcd(self.a, self.b), 1000)
        x, y = self.epicycloid(self.a, self.b, self.d, t)
        self.ax.plot(x, y)
        self.plot_widget.draw()
    
    def save_fig(self):
        """
        Save the current figure to a file.
        """
        filename = tk.filedialog.asksaveasfilename(defaultextension='.png')
        if filename:
            self.fig.savefig(filename)
    
    '''def rotate_point(x, y, angle):
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        x_rotated = x * cos_angle - y * sin_angle
        y_rotated = x * sin_angle + y * cos_angle
        return x_rotated, y_rotated'''
    
    '''def switch_syringe(self):
        if self.active_syringe == 0:
            self.active_syringe = 1
            return "T1"
        else:
            self.active_syringe = 0
            return "T0"'''
    
    def generate_gcode(self):
        """
        Generate Gcode for the epicycloid curve.
        """
        # Add a function to switch between syringes

        
        z_height = 1.25 # The height of each layer in mm
        #extrusion_multiplier = 0.05 # Adjust this value to control extrusion amount
        twist_angle = np.radians(3)
        commands = []
        # G-code header
        commands.append("T0") 
        commands.append("G21")  
        commands.append("G92 X0 Y0 Z0 E0 G90") 
        #commands.append("G1 E0.5")
        #new
        #commands.append("G92 E0") # Reset extruder position
        #commands.append("G91") # Set extruder to relative mode
        # Calculate the curve coordinates
        def rotate_point(x, y, angle):
            cos_angle = np.cos(angle)
            sin_angle = np.sin(angle)
            x_rotated = x * cos_angle - y * sin_angle
            y_rotated = x * sin_angle + y * cos_angle
            return x_rotated, y_rotated
    
        t = np.linspace(0, 2 * np.pi * self.b / np.gcd(self.a, self.b), 1000)
        x, y = self.epicycloid(self.a, self.b, self.d, t)
        
        # Scale the coordinates to fit within the printer bed
        x = x / np.max(x) * 30
        y = y / np.max(y) * 30

        # Convert the coordinates to Gcode commands
        for layer in range(self.layers):
            '''commands.append(self.switch_syringe())'''

            for i in range(len(x)):
                x_rot, y_rot = rotate_point(x[i], y[i], twist_angle * layer)
                x_new, y_new = x_rot + 100, y_rot + 100  # add 100 to X and Y
                if i == 0:
                    #commands.append('G0 X{} Y{} Z{} E0.1 F200'.format(x[i], y[i], layer * z_height))
                    #commands.append('G0 X{} Y{} Z{} F200'.format(x[i], y[i], layer * z_height))
                    # commands.append('G0 X{} Y{} Z{} E0.05 F200'.format(x_rot, y_rot, layer * z_height))
                    commands.append('G0 X{:.2f} Y{:.2f} Z{:.2f} E0.01 F200'.format(x_new, y_new, layer * z_height))
                else:
                    #commands.append('G1 X{} Y{} Z{} E0.1 F200'.format(x[i], y[i], layer * z_height))
                    #new

                    commands.append('G1 X{:.2f} Y{:.2f} Z{:.2f} E0.01 F200'.format(x_new, y_new, layer * z_height))
                
                
        # G-code footer
        commands.append("G1 Z5 E-2 F200") # move up & retract plunger a bit
        commands.append("G1 X25 F400 ") # move away from the print
        commands.append("G28") # Home printer
        #new
        #commands.append("G90") # Set extruder to absolute mode
        # Save the commands to a file
        filename = tk.filedialog.asksaveasfilename(defaultextension='.gcode')
        if filename:
            with open(filename, 'w') as f:
                f.write('\n'.join(commands))
    

if __name__ == '__main__':
    root = tk.Tk()
    gui = EpicycloidGUI(root)
    root.mainloop()

