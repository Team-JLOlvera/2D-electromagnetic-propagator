# Electromagnetic simulator for GPR

Development of a 2D electromagnetic propagator, based on finite differences in the time domain (FDTD)

By: Aplatag

## Project Organization

    ├── README.md          <- Project description.
    │
    ├── scripts            <- Project script.
    │   └── main.py    <- code to define the gpr scenario and execute it.
    │
    ├── environment.yml    <- The requirements file.
    │
    └── modules             
        ├── __init__.py    <- Python module.
        │
        ├── interface          
        │   └── user_messages.py  <- User guide messages while simulation.
        │
        ├── images_Bscan          
        │   └── formation_Bscan.py  <- union of all code modules.
        │
        ├── objets          
        |   ├──creation_objects.py  <- The objects present in the subsurface are created.
        │   │
        │   └── join_objects.py  <- attach the objects to the model.
        │
        ├── propagator      
        │   └── propagator_2D.py   <- propagator 2D in FDTD.
        │
        ├── waveform      
        │   └── waveform.py   <- function of different waveform.
        │
        ├── visualization      
        │   └── display.py   <- image display function.
        │
        └── pulses          
            └── waveform.py   <- pulse formation.
        
         



        