from collections import defaultdict
from data_processing.process_lap import analyse_lap

def build_reference_lap(reference_laps):
    reference_samples = []
    corners_by_position = defaultdict(list)
    for i, lap in enumerate(reference_laps, 1):
        samples = lap["samples"]
        corners = analyse_lap(samples)
        reference_samples.append({"lap": i, "corners": corners})
    for c in reference_samples:
        for i, r in enumerate(c["corners"], start=1):
            corners_by_position[i].append(r)
    return corners_by_position
