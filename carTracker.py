import math
from datetime import datetime
class EuclideanDistTracker:
    def __init__(self):
        # Almacena las posiciones centrales de los objetos
        self.center_points = {}
        # Mantiene el recuento de las identificaciones cada vez que se detecta una nueva identificación de objeto
        self.id_count = 0


    def update(self, objects_rect):
        # Cajas de objetos e identificaciones
        objects_bbs_ids = []

        # Obtener el punto central del nuevo objeto
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Averigüe si ese objeto ya fue detectado
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # Se detecta un nuevo objeto asignamos la ID a ese objeto
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Limpia el diccionario por puntos centrales para eliminar los IDS que ya no se usan
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Actualiza diccionario con ID no utilizados eliminados
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



