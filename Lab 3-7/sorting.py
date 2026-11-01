import math
import re

MIN_ITEMS = 2
MAX_ITEMS = 20          


class StepLog:
    """Holds the list being sorted and takes a snapshot of it at every step.
    The page replays these snapshots as the animation.
    Each step is a dict: kind, array, active, pivot, bounds, sorted, note."""
    def __init__(self, numbers):
        self.data = list(numbers)
        self.done = set()             
        self.steps = []

    def add(self, kind, note, active=(), pivot=None, bounds=None):
        """Record the list as it is right now.
        kind is one of: start, compare, swap, write, pivot, merge, sorted, done."""
        self.steps.append({
            "kind": kind,
            "array": list(self.data),
            "active": list(active),                 
            "pivot": pivot,                         
            "bounds": list(bounds) if bounds else None,   
            "sorted": sorted(self.done),
            "note": note,
        })

    def swap(self, i, j, note, pivot=None, bounds=None):
        """Swap two positions and record it."""
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.add("swap", note, [i, j], pivot, bounds)

    def finish(self):
        """Mark everything as sorted. Returns (sorted_list, steps)."""
        self.done.update(range(len(self.data)))
        self.add("done", "Every value is in its final place. The list is sorted.")
        return self.data, self.steps


def bubble_sort(numbers):
    """Swap neighbours that are out of order, so the biggest value bubbles
    to the end on every pass. Returns (sorted_list, steps)."""
    log = StepLog(numbers)
    data = log.data
    log.add("start", "Start with the list as typed.")

    for end in range(len(data) - 1, 0, -1):
        swapped = False
        for i in range(end):
            log.add("compare", f"Compare {data[i]} and {data[i + 1]}.", [i, i + 1])
            if data[i] > data[i + 1]:
                log.swap(i, i + 1, f"{data[i]} is bigger than {data[i + 1]}, so swap them.")
                swapped = True
        log.done.add(end)
        log.add("sorted", f"{data[end]} has bubbled up and is now in its final place.")
        if not swapped:
            log.done.update(range(end))
            log.add("sorted", "No swaps in this pass, so the rest is already in order.")
            break

    return log.finish()


def selection_sort(numbers):
    """Find the smallest value in the unsorted part and swap it to the front.
    Returns (sorted_list, steps)."""
    log = StepLog(numbers)
    data = log.data
    log.add("start", "Start with the list as typed.")

    for i in range(len(data) - 1):
        smallest = i
        log.add("pivot", f"Look for the smallest value. {data[i]} is the smallest so far.", pivot=smallest)
        for j in range(i + 1, len(data)):
            log.add("compare", f"Compare {data[j]} with the smallest so far, {data[smallest]}.", [j], pivot=smallest)
            if data[j] < data[smallest]:
                smallest = j
                log.add("pivot", f"{data[smallest]} is the new smallest.", pivot=smallest)
        if smallest != i:
            log.swap(i, smallest, f"Swap {data[smallest]} to the front of the unsorted part.")
        log.done.add(i)
        log.add("sorted", f"{data[i]} is now in its final place.")

    return log.finish()


def insertion_sort(numbers):
    """Take each value in turn and slide it left until it sits in the right
    place among the values before it. Uses swaps so every move can be watched.
    Returns (sorted_list, steps)."""
    log = StepLog(numbers)
    data = log.data
    log.done.add(0)
    log.add("start", "Start with the list as typed. The first item on its own already counts as sorted.")

    for i in range(1, len(data)):
        key, j = data[i], i
        log.add("pivot", f"Take {key} and slide it left until it fits.", pivot=j)
        while j > 0:
            log.add("compare", f"Compare {key} with {data[j - 1]}.", [j - 1], pivot=j)
            if data[j - 1] <= key:
                break
            log.swap(j - 1, j, f"{data[j - 1]} is bigger than {key}, so swap them.", pivot=j - 1)
            j -= 1
        log.done.update(range(i + 1))
        log.add("sorted", f"{key} fits here. The first {i + 1} items are now in order.")

    return log.finish()


def merge_sort(numbers):
    """Split the list in half, sort each half, then merge the two sorted
    halves. Returns (sorted_list, steps)."""
    log = StepLog(numbers)
    log.add("start", "Start with the list as typed.")
    _merge_sort(log, 0, len(log.data) - 1)
    return log.finish()


def _merge_sort(log, low, high):
    """Sort log.data[low..high] by splitting, sorting each half, then merging."""
    if low >= high:
        return
    data = log.data
    mid = (low + high) // 2
    _merge_sort(log, low, mid)
    _merge_sort(log, mid + 1, high)

    bounds = (low, high)
    log.add("merge", f"Merge the two sorted halves (items {low + 1}-{mid + 1} and {mid + 2}-{high + 1}).", bounds=bounds)
    merged, i, j = [], low, mid + 1
    while i <= mid and j <= high:
        log.add("compare", f"Compare {data[i]} (left half) and {data[j]} (right half).", [i, j], bounds=bounds)
        if data[i] <= data[j]:                
            merged.append(data[i])
            i += 1
        else:
            merged.append(data[j])
            j += 1
    merged.extend(data[i:mid + 1])            
    merged.extend(data[j:high + 1])

    last_merge = low == 0 and high == len(data) - 1
    for offset, value in enumerate(merged):
        data[low + offset] = value
        if last_merge:
            log.done.add(low + offset)
        log.add("write", f"Write {value} into position {low + offset + 1}.", [low + offset], bounds=bounds)


def quick_sort(numbers):
    """Pick a pivot, move smaller values to its left and bigger values to its
    right, then sort each side the same way. Returns (sorted_list, steps)."""
    log = StepLog(numbers)
    log.add("start", "Start with the list as typed.")
    _quick_sort(log, 0, len(log.data) - 1)
    return log.finish()


def _quick_sort(log, low, high):
    """Sort log.data[low..high] using the last item as the pivot."""
    if low > high:
        return
    data = log.data
    bounds = (low, high)
    if low == high:
        log.done.add(low)
        log.add("sorted", f"{data[low]} is alone in its part, so it is in its final place.", bounds=bounds)
        return

    pivot = data[high]
    log.add("pivot", f"Choose {pivot}, the last item, as the pivot.", pivot=high, bounds=bounds)
    store = low                               
    for j in range(low, high):
        log.add("compare", f"Compare {data[j]} with the pivot {pivot}.", [j], pivot=high, bounds=bounds)
        if data[j] < pivot:
            if store != j:
                log.swap(store, j, f"{data[j]} is smaller than the pivot, so move it to the left side.",
                         pivot=high, bounds=bounds)
            store += 1
    if store != high:
        log.swap(store, high, f"Swap the pivot {pivot} into its final place.", bounds=bounds)
    log.done.add(store)
    log.add("sorted", f"The pivot {pivot} is now in its final place.", bounds=bounds)

    _quick_sort(log, low, store - 1)
    _quick_sort(log, store + 1, high)


ALGORITHMS = {
    "bubble": {
        "name": "Bubble Sort", "func": bubble_sort,
        "about": "Swaps neighbours that are out of order, so the biggest value bubbles to the end on every pass.",
        "time": "Time: best O(n), average and worst O(n²)",
    },
    "selection": {
        "name": "Selection Sort", "func": selection_sort,
        "about": "Finds the smallest value in the unsorted part and swaps it to the front.",
        "time": "Time: O(n²) in every case",
    },
    "insertion": {
        "name": "Insertion Sort", "func": insertion_sort,
        "about": "Slides each value left until it sits in the right place among the values before it.",
        "time": "Time: best O(n), average and worst O(n²)",
    },
    "merge": {
        "name": "Merge Sort", "func": merge_sort,
        "about": "Splits the list in half, sorts each half, then merges the two sorted halves.",
        "time": "Time: O(n log n) in every case",
    },
    "quick": {
        "name": "Quick Sort", "func": quick_sort,
        "about": "Picks a pivot, puts smaller values on its left and bigger values on its right, then repeats on each side.",
        "time": "Time: average O(n log n), worst O(n²)",
    },
}


def parse_numbers(text):
    """Turn text such as '5, 3 8 1' into a list of numbers.
    Raises ValueError when the input is not usable."""
    tokens = [t for t in re.split(r"[,\s]+", text.strip()) if t]
    numbers = []
    for token in tokens:
        try:
            value = int(token)
        except ValueError:
            try:
                value = float(token)
            except ValueError:
                raise ValueError(f"{token!r} is not a number.")
            if not math.isfinite(value):
                raise ValueError(f"{token!r} is not a number.")
            if value.is_integer():
                value = int(value)
        numbers.append(value)

    if len(numbers) < MIN_ITEMS:
        raise ValueError(f"Enter at least {MIN_ITEMS} numbers.")
    if len(numbers) > MAX_ITEMS:
        raise ValueError(f"Enter no more than {MAX_ITEMS} numbers so the animation stays readable.")
    return numbers


def sort_numbers(algorithm, numbers):
    """Run the chosen algorithm. Returns (sorted_list, steps).
    Raises ValueError when the algorithm name is not one of the five."""
    if algorithm not in ALGORITHMS:
        raise ValueError("Choose one of the five sorting algorithms.")
    return ALGORITHMS[algorithm]["func"](numbers)


def count_operations(steps):
    """Return (comparisons, swaps_or_writes) counted from the recorded steps."""
    comparisons = sum(1 for s in steps if s["kind"] == "compare")
    moves = sum(1 for s in steps if s["kind"] in ("swap", "write"))
    return comparisons, moves


if __name__ == "__main__":
    sample = [5, 3, 8, 1, 9, 2]
    for key, algo in ALGORITHMS.items():
        result, steps = sort_numbers(key, sample)
        comparisons, moves = count_operations(steps)
        print(f"{algo['name']:<15} -> {result} | {comparisons} comparisons, {moves} swaps/writes")
