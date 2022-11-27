# electromagnetic simulator for GPR

Development of a 2D electromagnetic propagator, based on finite differences in the time domain (FDTD)

By: Aplata

## Project Organization

    ├── README.md          <- Project description.
    ├── scripts            <- Project script.
    │
    ├── environment.yml    <- The requirements file.
    │
    └── modules             
        ├── __init__.py    <- Python module.
        │
        ├── interface          
        │   └── user_messages.py  <- User guide messages while simulation.
        │
        ├── objets          
        |   └── creation_objects.py  <- The objects present in the subsurface are created.
        │
        ├── propagator      
        │   └── propagator_2D.py   <- propagator 2D in FDTD.
        │
        ├── waveform      
        │   └── waveform.py   <- function of different waveform.
        │
        └── utils          
            └── paths.py   <- relative paths.
        
         



        