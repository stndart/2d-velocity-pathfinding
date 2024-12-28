import sys

from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from backend import Core, logger
from launch_config import generate_launch
from backend.pathfinding.buildgraph import check_collisions

from backend.sprites import make_sprite
from backend.geometry import Line

def main(core: Core):
    app = QApplication(sys.argv)
    window = MainWindow(core)
    
    logger.log("App running")
    sys.exit(app.exec_())

if __name__ == '__main__':
    back = Core()
    generate_launch(back, launch_configuration=4, gen_configuration=1, generate=False,
                    pathfinder_algorithm='Theta*')
    
    sp = [c.collision_shape for c in back.sprites()][:4]
    c1, c2, t1, t2 = sp
    q = back.quadtree
    pt = back.pathfinder
    g = pt.graph.graph
    p1, p2, p3 = t2.vertexes()
    print(check_collisions(q, p3))
    
    main(back)