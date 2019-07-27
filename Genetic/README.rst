====
GAFT
====

A **G**\ enetic **A**\ lgorithm **F**\ ramework in py\ **T**\ hon

.. image:: https://travis-ci.org/PytLab/gaft.svg?branch=master
    :target: https://travis-ci.org/PytLab/gaft
    :alt: Build Status

.. image:: https://img.shields.io/codecov/c/github/PytLab/gaft/master.svg
    :target: https://codecov.io/gh/PytLab/gaft
    :alt: Codecov

.. image:: https://landscape.io/github/PytLab/gaft/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PytLab/gaft/master
    :alt: Code Health

.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/pypi-v0.5.7-blue.svg
    :target: https://pypi.python.org/pypi/gaft/
    :alt: versions

.. image:: https://readthedocs.org/projects/gaft/badge/?version=latest
    :target: https://gaft.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Introduction
------------

**GAFT** is a general Python Framework for genetic algorithm computation. It provides built-in genetic operators for target optimization and plugin interfaces for users to define your own genetic operators and on-the-fly analysis for algorithm testing.

**GAFT** is now accelerated using MPI parallelization interfaces. You can run it on your cluster in parallel with MPI environment.

Python Support
--------------

**GAFT** requires Python version 3.x (Python 2.x is not supported).

Installation
------------

1. Via pip::

    pip install gaft

2. From source::

    python setup.py install

If you want GAFT to run in MPI env, please install mpi4py explicitly::

    pip install mpi4py

See `INSTALL.md <https://github.com/PytLab/gaft/blob/master/INSTALL.md>`_ for more installation details.

Test
----

Run unit test::
    
    python setup.py test

Quick start
-----------

1. Importing
````````````

.. code-block:: python

    from gaft import GAEngine
    from gaft.components import BinaryIndividual, Population
    from gaft.operators import RouletteWheelSelection, UniformCrossover, FlipBitMutation

    # Analysis plugin base class.
    from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis

2. Define population
````````````````````

.. code-block:: python
    
    indv_template = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
    population = Population(indv_template=indv_template, size=50)
    population.init()  # Initialize population with individuals.

3. Create genetic operators
```````````````````````````

.. code-block:: python

    # Use built-in operators here.
    selection = RouletteWheelSelection()
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    mutation = FlipBitMutation(pm=0.1)

4. Create genetic algorithm engine to run optimization
``````````````````````````````````````````````````````

.. code-block:: python

    engine = GAEngine(population=population, selection=selection,
                      crossover=crossover, mutation=mutation,
                      analysis=[FitnessStore])

5. Define and register fitness function
```````````````````````````````````````

.. code-block:: python

    @engine.fitness_register
    def fitness(indv):
        x, = indv.solution
        return x + 10*sin(5*x) + 7*cos(4*x)

or if you want to minimize it, you can add a minimization decorator on it

.. code-block:: python

    @engine.fitness_register
    @engine.minimize
    def fitness(indv):
        x, = indv.solution
        return x + 10*sin(5*x) + 7*cos(4*x)

6. Define and register an on-the-fly analysis (optional)
````````````````````````````````````````````````````````

.. code-block:: python

    @engine.analysis_register
    class ConsoleOutput(OnTheFlyAnalysis):
        master_only = True
        interval = 1
        def register_step(self, g, population, engine):
            best_indv = population.best_indv(engine.fitness)
            msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.fmax)
            engine.logger.info(msg)

7. Run
``````

.. code-block:: python

    if '__main__' == __name__:
        engine.run(ng=100)

8. Evolution curve
``````````````````

.. image:: https://github.com/PytLab/gaft/blob/master/examples/ex01/envolution_curve.png

9. Optimization animation
`````````````````````````

.. image:: https://github.com/PytLab/gaft/blob/master/examples/ex01/animation.gif

See `example 01 <https://github.com/PytLab/gaft/blob/master/examples/ex01/ex01.py>`_ for a one-dimension search for the global maximum of function `f(x) = x + 10sin(5x) + 7cos(4x)`

Global maximum search for binary function
-----------------------------------------

.. image:: https://github.com/PytLab/gaft/blob/master/examples/ex02/surface_animation.gif

See `example 02 <https://github.com/PytLab/gaft/blob/master/examples/ex02/ex02.py>`_ for a two-dimension search for the global maximum of function `f(x, y) = y*sin(2*pi*x) + x*cos(2*pi*y)`

Obtain a copy
-------------

The GAFT framework is distributed under the GPLv3 license and can be obtained from the GAFT git repository or PyPI 

- https://github.com/PytLab/gaft
- https://pypi.python.org/pypi/gaft/

