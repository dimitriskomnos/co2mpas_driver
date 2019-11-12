## Com2pas_driver: Try it live
<!--move them to CONTRIBUTING.md -->
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JRCSTU/co2mpas_driver/master?urlpath=lab/tree/examples)

Access this Binder at the following URL:

https://mybinder.org/v2/gh/JRCSTU/co2mpas_driver/master

Click the binder badge to try it live without installing anything. 
This will take you directly to JupyterLab where we used Jupyter notebook to 
present examples on how to use co2mpas_driver model (i.e., MFC) to simulate 
the driver behaviour of a vehicle.

## What is co2mpas_driver?

Co2mpas_driver is a library used to implement a lightweight microsimulation 
free-flow acceleration model (MFC) that is able to capture the vehicle acceleration 
dynamics accurately and consistently, it provides a link between the model and 
the driver and can be easily implemented and tested without raising the 
computational complexity. The proposed model has been developed by the Joint Research Centre of the 
European Commission for more details https://journals.sagepub.com/doi/10.1177/0361198119838515

## Installation

1. **Download or clone co2mpas_driver**
    If you have access to the project under JRCSTU github repository then clone
    the co2mpas_driver project to your local machine.
   
        git clone https://github.com/JRCSTU/co2mpas_driver.git
       
2. **Install on your local machine**
    You can install on your machine using:
    
        pip install dist/co2mpas_driver-1.0.0-py2.py3-none-any.whl 
        
## How to use co2mpas_driver library

In this example we will use co2mpas_driver model in order to extract the drivers 
acceleration behavior as approaching the desired speed.

a. **Setup** 
   
  * First, set up python, numpy, matplotlib.
  
    set up python environment: numpy for numerical routines, and matplotlib 
    for plotting
    
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
   
  * Import dispatcher(dsp) from co2mpas_driver that contains functions 
    and simulation model to process vehicle data and Import also schedula
    for selecting and executing functions. for more information on how to use 
    schedula https://pypi.org/project/schedula/
     
        >>> from co2mpas_driver import dsp
        >>> import schedula as sh
   
b. **Load data**

  * Load vehicle data for a specific vehicle from vehicles database
   
        >>> db_path = 'EuroSegmentCar.csv'
        
  * Load user input parameters from an excel file
   
        >>> input_path = 'sample.xlsx'  
  
  * Sample time series
   
        >>> sim_step = 0.1 #The simulation step in seconds
        >>> duration = 100 #Duration of the simulation in seconds
        >>> times = np.arange(0, duration + sim_step, sim_step)
        
  * Load user input parameters directly writing in your sample script
   
        >>> inputs = {
        'vehicle_id': 35135,  # A sample car id from the database
        'inputs': {'gear_shifting_style': 0.7, #The gear shifting style as 
                                                described in the TRR paper
                    'starting_speed': 0,
                   'desired_velocity': 40,
                   'driver_style': 1},  # gear shifting can take value
        # from 0(timid driver) to 1(aggressive driver)
        'time_series': {'times': times}
        }
        
c. **Dispatcher**      
  
  * Dispatcher will select and execute the proper functions for the given inputs 
    and the requested outputs
           
        >>> core = dsp(dict(db_path=db_path, input_path=input_path, inputs=inputs),
           outputs=['outputs'], shrink=True)
           
  * Plot workflow of the core model from the dispatcher
           
        >>> core.plot()
    
    This will automatically open an internet browser and show the work flow 
    of the core model as below. you can click all the rectangular boxes to see
    in detail sub models like load, model, write and plot. 
        
    ![alt text](https://github.com/ashenafimenza/new_MFC/blob/master/co2mpas_driver/images/core_example.PNG)
    
    **The Load module**
    
    ![alt text](https://github.com/ashenafimenza/new_MFC/blob/master/co2mpas_driver/images/load_example.PNG)
    
    **merged vehicle data for the vehicle_id used above**
    
    ![alt text](https://github.com/ashenafimenza/new_MFC/blob/master/co2mpas_driver/images/data.PNG)
        
  * Load outputs of dispatcher
    Select the chosen dictionary key (outputs) from the given dictionary.
           
        >>> outputs = sh.selector(['outputs'], sh.selector(['outputs'], core))
        
  * select the desired output
        
        >>> output = sh.selector(['Curves', 'poly_spline', 'Start', 'Stop', 'gs',
                      'discrete_acceleration_curves', 'velocities',
                      'accelerations', 'transmission'], outputs['outputs'])
         
    The final acceleration curves, the engine acceleration potential 
    curves (poly_spline), before the calculation of the resistances and the
    limitation due to max possible acceleration (friction).
                    
        >>> curves, poly_spline, start, stop, gs, discrete_acceleration_curves, \
        velocities, accelerations, transmission = \
        output['Curves'], output['poly_spline'], output['Start'], output['Stop'], output['gs'], \
        output['discrete_acceleration_curves'], output['velocities'], \
        output['accelerations'], output['transmission'], \
        
    curves: Final acceleration curves
    poly_spline: 
    start and stop: Start and stop speed for each gear
    gs:
    discrete_acceleration_curves
    velocities:
    accelerations:
             
d. **Plot**          
        
    >>> plt.figure('Time-Speed')
    >>> plt.plot(times, velocities)
    >>> plt.grid()
    >>> plt.figure('Speed-Acceleration')
    >>> plt.plot(velocities, accelerations)
    >>> plt.grid()
    >>> plt.figure('Acceleration-Time')
    >>> plt.plot(times, accelerations)
    >>> plt.grid()
    
    
    >>> plt.figure('Speed-Acceleration')
    >>> for curve in discrete_acceleration_curves:
        sp_bins = list(curve['x'])
        acceleration = list(curve['y'])
        plt.plot(sp_bins, acceleration, 'k')
    >>> plt.show()
        
e. **Results**
  
 ![alt text](https://github.com/ashenafimenza/new_MFC/blob/master/co2mpas_driver/images/speed-time.PNG)
 
 **Figure 1.** Speed(m/s) versus time(s) graph over the desired speed range.
 
 Acceleration(m/s*2) versus speed(m/s) graph
  
 ![alt text](https://github.com/ashenafimenza/new_MFC/blob/master/co2mpas_driver/images/acce-speed.PNG)
 
 **Figure 2.** Acceleration per gear, the gear-shifting points and final acceleration potential of our selected 
   vehicle over the desired speed range
 
 Acceleration(m/s*2) versus speed graph(m/s)
  
 ![alt text](https://github.com/ashenafimenza/new_MFC/blob/master/co2mpas_driver/images/acc-time.PNG)
  
 **Figure 3.** The final acceleration potential of our selected vehicle over the desired speed range
 
       
   **Contributing**
   
   Pull requests and stars are very welcome.
   
   For bugs and feature requests, please [create an issue](https://github.com/ashenafimenza/new_MFC/issues/new).
               
[1]: https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/
[2]: https://black.readthedocs.io/  