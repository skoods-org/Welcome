# Welcome to Skoods

Skoods is a Self-Racing Car Team, crowdsourced, running virtual competitions in our platform. We build simulation scenarios and models for self-driving cars as racing competitions.

Our community of pilots develops algorithms on our platform: learning, interacting and competing for the Podium.

Our mission is to have a real Self-Driving Car racing by 2020.

- Website: www.skoods.org

## What's New





## Requirements

Windows

## Download and Run the Competition Executable

Run the executable and navigate the world with the using the arrows.

- Alpha Version Race

## Download and Install Anaconda

The open source Anaconda Distribution is the fastest and easiest way to do Python, data science and machine learning on Linux, Windows, and Mac OS X. It's the industry standard for developing, testing, and training on a single machine.

- Download and install the latest version: https://www.anaconda.com/download/

- Video Tutorial: [Python - Install Anaconda, Jupyter Notebook, Spyder on Windows 10](https://www.youtube.com/watch?v=Q0jGAZAdZqM)

## Create a Conda Environment

An environment consists of a certain Python version and some packages. Consequently, if you want to develop or use applications with different Python or package version requirements, you need to set up different environments.

We are currently using Python version 3.5.

After installing Anaconda, Open the Anaconda Prompt app from the Start Menu and follow the instructions:.

To create a new environment, type:

```comm
conda create -n skoods35 python=3.5
```

When conda asks you to proceed, type `y`:

```
proceed ([y]/n)?
```

After this process, check if the environment was created. To see a list of all of your environments, run in the Anaconda Prompt:

```
conda info --envs
```

## Activate Environment

On Windows, in your Anaconda Prompt, run:

```
activate skoods35
```

On macOS and Linux, in your Terminal Window, run:

```
source activate skoods35
```

## Install Additional Packages

PIP is a package manager for Python packages, or modules if you like. A package contains all the files you need for a module and modules are Python code libraries you can include in your project.

First, upgrade PIP itself:

```
pip install --upgrade pip
```

Then, follow the instructions to install 3 additional packages:

```
pip install msgpack-rpc-python
```

```
pip install airsim
```

```
conda install --channel https://conda.anaconda.org/menpo opencv3
```

If you use more Python packages in your code, you must install them here. Make sure the environment is activated before running the command.

## (Optional) Download and Install Visual Studio Code

Visual Studio Code combines the simplicity of a source code editor with powerful developer tooling.

- Download: https://code.visualstudio.com/download

- More information: https://code.visualstudio.com/docs/editor/whyvscode

## Run the Code



