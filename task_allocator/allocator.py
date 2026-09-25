robots = {
    "AMR-01": {"battery": 95, "tasks": 2},
    "AMR-02": {"battery": 87, "tasks": 1},
    "AMR-03": {"battery": 76, "tasks": 0},
}


def allocate_task():
    available = [
        (robot_id, data)
        for robot_id, data in robots.items()
        if data["battery"] > 30
    ]

    selected = min(
        available,
        key=lambda item: item[1]["tasks"]
    )

    return selected[0]


robot = allocate_task()

print(f"Task allocated to {robot}")