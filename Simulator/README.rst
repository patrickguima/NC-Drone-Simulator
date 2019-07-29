====
UAV SIMULATOR
====


Introduction
------------
This simulator is implemented using Python and the PyGame Library.



Python Support
--------------

Requires Python version 3.x (Python 2.x is not supported).

Running
------------

Via terminal::

    python3 simulator.py


Quick start
-----------

1. Number of simulations cycles
````````````

.. code-block:: python

    ticks = 10000

2. Running ON or OFF screen
``````````````````````````````````````````````````````
.. code-block:: python

    simulation_on_screen = True


3. Selecting strategys
````````````````````

.. code-block:: python
    
    time_strategy = False
    evaporation_strategy = True
    quandrant_strategy = False


4. Simulations parameters
```````````````````````````

.. code-block:: python

    evap_time = 1
    evap_factor =  0.83
    threshold_time = 0
    num_simulations = 30

4. Running or step by step
``````````````````````````````````````````````````````

.. code-block:: python
    
    run = True #True to run and False to run step by step using the right arrow


5. Running or step by step
``````````````````````````````````````````````````````
.. code-block:: python
    #Just uncoment the lines below to add the obstacles
    #make_obstacles1(grid)
    #make_obstacles2(grid)
    #make_obstacles3(grid)