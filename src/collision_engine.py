from scipy.spatial import KDTree
import numpy as np

def detect_collisions(df, radius=0.02):
    coords = df[["lat", "lon"]].values
    tree = KDTree(coords)

    alerts = []

    for i, point in enumerate(coords):
        neighbors = tree.query_ball_point(point, radius)

        for j in neighbors:
            if i >= j:
                continue

            p1 = coords[i]
            p2 = coords[j]

            v1 = np.array([df.iloc[i].vx, df.iloc[i].vy])
            v2 = np.array([df.iloc[j].vx, df.iloc[j].vy])

            rel_pos = p1 - p2
            rel_vel = v1 - v2

            if np.linalg.norm(rel_vel) == 0:
                continue

            tcpa = - np.dot(rel_pos, rel_vel) / np.linalg.norm(rel_vel)**2
            cpa = np.linalg.norm(rel_pos + tcpa * rel_vel)

            if tcpa > 0 and cpa < 0.005:
                alerts.append((df.iloc[i].MMSI, df.iloc[j].MMSI, cpa))

    return alerts

def collision_risk_value(is_collision):

    if is_collision:
        return 80
    else:
        return 10