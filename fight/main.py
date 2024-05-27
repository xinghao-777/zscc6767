import pygame as pg
import control_system

if __name__ == "__main__":
    pg.init()
    con = control_system.Control()
    con.run()


