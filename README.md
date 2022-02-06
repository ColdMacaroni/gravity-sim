# Grav sim
Simple gravitational simulation of spherical bodies. This doesn't follow any
real like constants or anything just adding vectors together with values I made
up.

## How to use
Run `main.py` with python >= 3.10 and pygame (not sure what version).

Left click once to create a circle. Move the mouse to determine the radius and
click again to set it. The arrow that pops up represents the initial movement
of the body.

## Shortcuts
### On a blank canvas:
|   Action   | Result                    |
|   :---:    | ---                       |
| Left click | Create body               |
| Z          | Delete last body          |
| R          | Reset (delete all bodies) |

### After setting the size of a body
|    Action   | Result                         |
|    :---:    | ---                            |
| Left click  | Set speed                      |
| Right click | Set body as passive (immobile) |
| Esc         | Leave speed unset (0)          |
