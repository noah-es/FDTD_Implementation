import numpy as np
import matplotlib.pyplot as plt
import imageio

# Simulation parameters
dominio = 200  # Domain size, 200 cells
tiempo = 200  # Time steps
epsilon_vacio = 1  # Vacuum permittivity
mu_vacio = 1  # Vacuum permeability
epsilon_material = 4  # Wall permittivity
sigma = 0.04  # Wall conductivity

# We will consider the Δt and Δx are both the unit, 
# so they will not appear explicitly in the field expressions.
# It's important to note that our light velocity is the unity.
# The light travels a Δx in Δt. Because of this, epsilon_vacio*epsilon_vacio=1.

# I initialise E.M fields to zero with the function np.zeros 

ez = np.zeros(dominio)
hy = np.zeros(dominio)

# I define the source's position [x] in the first cell of the domain. 
# The source is a senoidal frequency-time dependent function.
# I define Pi number and source's frequency [f] too.
# The frecuency also is different for us, due to the change in the value of c.

x = 0
pi = 3.1415927
f = 0.21
# alpha is a constant dependent of material conductivity and permittivity (vacuum and material)
alpha = (sigma) / (2 * epsilon_material * epsilon_vacio)

# Initialize list to store frames
frames = []

# I now perform the computations for both fields. 
# For this purpose, several loops are nested, so that Ex and Hy are calculated 
# for each region of space at each time step. 
# The time starts at 1, and goes up to 'tiempo'+1, i.e. 'tiempo' time steps.

for t in range(1, tiempo + 1):
    
    # Calculation of Ez
    # I introduce an if-else to taking into consideration de wall
    # The wall's widhth is 20 cells, as you can see in the first 'if'.
    # The calculation changes a little bit, because I introduce alpha, that has 
    # all the information of the wall.
    
    for i in range(0, dominio):
        if 80 <= i <= 100:
            ez[i] = ez[i] * ((1 - alpha) / (1 + alpha)) + (hy[i - 1] - hy[i]) / (np.sqrt(mu_vacio * epsilon_vacio) * epsilon_material * (1 + alpha))
        else:
            ez[i] = ez[i] + (hy[i - 1] - hy[i]) / (np.sqrt(mu_vacio * epsilon_vacio))
           
    pulso = np.sin(2 * pi * f * t)
    ez[x] = pulso

    # Calculation of Hy. 
    # Now, I CANNOT loop to 'dominio', due to it involves a 'ez[i+1]'
    for i in range(0, dominio - 1):
        hy[i] = hy[i] + (ez[i] - ez[i + 1]) / np.sqrt(mu_vacio * epsilon_vacio)
    
    # Create the plot for the current timestep
    plt.rcParams['font.size'] = 12
    plt.figure(figsize=(8, 3.5))
    
    plt.subplot(211)
    plt.plot(ez, color='k', linewidth=1)
    plt.ylabel('E$_z$', fontsize='14')
    plt.xticks(np.arange(0, 201, step=20))
    plt.xlim(-20, 200)
    plt.yticks(np.arange(-2, 3, step=1))
    plt.ylim(-2, 2)
    plt.text(80, 2.5, 'T = {}'.format(t), horizontalalignment='center')
    plt.text(115, 2.5, 'F = {}'.format(f), horizontalalignment='center')
    for y in np.arange(2, -2.1, -0.5):
        plt.text(80, y, '|', horizontalalignment='center')
        plt.text(100, y, '|', horizontalalignment='center')
        
    plt.subplot(212)
    plt.plot(hy, color='k', linewidth=1)
    plt.ylabel('H$_y$', fontsize='14')
    plt.xlabel('Celdas FDTD')
    plt.xticks(np.arange(0, 201, step=20))
    plt.xlim(-20, 200)
    plt.yticks(np.arange(-2, 3, step=1))
    plt.ylim(-2, 2)
    for y in np.arange(2, -2.1, -0.5):
        plt.text(80, y, '|', horizontalalignment='center')
        plt.text(100, y, '|', horizontalalignment='center')
    
    plt.subplots_adjust(bottom=0.2, hspace=0.45)
    
    # Save the current frame
    plt.savefig(f'frame_{t}.png')
    plt.close()
    
    frames.append(f'frame_{t}.png')

# Create GIF
with imageio.get_writer('em_wave_propagation.gif', mode='I', duration=0.1) as writer:
    for frame in frames:
        image = imageio.imread(frame)
        writer.append_data(image)

# Clean up the frames
import os
for frame in frames:
    os.remove(frame)
