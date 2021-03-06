Installation
=============

Before we get started
----------------------

This version of code is currently only supported on Linux. It may be possible to execute it on Windows, 
though this hasn’t been extensively tested. Some functionalities like generating the image including the
decision tree rules from the dot file may not work as intended. Please refer to the :ref:`limitations` section
for further information regarding this problem.

Preparing the environment
-------------------------

We recommend using Anaconda to create the virtual environment with all the libraries, packages and dependencies needed 
to run the code. Anaconda is a library that includes Python and many useful packages for Python, as well as an
environment manager called conda that makes package management simple.

Follow the installation instructions for Anaconda `here <https://docs.continuum.io/anaconda/install/>`__. Then create a
conda environment from the yaml file *environment.yml* as follows

.. parsed-literal::

    conda env create -f environment.yml

After that, the new environment can be activated using the following command

.. parsed-literal::

    conda activate aberdeen

You can verify whether the new environment was installed correctly by running

.. parsed-literal::

    conda env list
