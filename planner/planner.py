from dataclasses import dataclass


@dataclass
class Robot:
    robot_id: str
    x: float
    y: float


def distance(a: Robot, b: Robot):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def conflict(a: Robot, b: Robot, threshold=1.5):
    return distance(a, b) < threshold


robots = [
    Robot("AMR-01", 1, 1),
    Robot("AMR-02", 2, 1),
    Robot("AMR-03", 8, 8),
]


for i in range(len(robots)):
    for j in range(i + 1, len(robots)):

        a = robots[i]
        b = robots[j]

        if conflict(a, b):
            print(
                f"CONFLICT: {a.robot_id} <-> {b.robot_id}"
            )
        else:
            print(
                f"SAFE: {a.robot_id} <-> {b.robot_id}"
            )