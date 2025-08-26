from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory
import time
import os

# initializare Flask si activare CORS
app = Flask(__name__)
CORS(app)

# --- HOME: servim index.html din același folder cu app.py ---
@app.get("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

# (opțional) servește și alte fișiere statice (css/js) din folderul curent
@app.get("/<path:filename>")
def static_passthrough(filename):
    # doar dacă vrei să deschizi direct style.css / script.js din același folder
    if os.path.exists(os.path.join(os.getcwd(), filename)):
        return send_from_directory(os.getcwd(), filename)
    return ("Not found", 404)

# ruta pentru sortare sir
@app.route('/sort', methods=['POST'])
def sort_array():
    data = request.json or {}
    array = data.get('array')  # sirul pentru sortat
    algorithm = data.get('algorithm')  # algoritmul de sortare ales
    data_type = data.get('type', 'number')  # tipul datelor din sir

    # verificare daca datele necesare sunt furnizate
    if array is None or algorithm is None:
        return jsonify({"error": "Array and algorithm are required"}), 400

    if data_type == 'number':
        try:
            array = [float(x) for x in array]
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid input. All elements must be numbers."}), 400
    elif data_type == 'string':
        array = [str(x) for x in array]
    else:
        return jsonify({"error": "Invalid type"}), 400

    # gardă pentru radix: doar intregi ne-negativi
    if algorithm == 'radix':
        if data_type != 'number' or any((not float(x).is_integer()) or (x < 0) for x in array):
            return jsonify({"error": "Radix sort needs non-negative integers only."}), 400
        array = [int(x) for x in array]

    # limită pentru bogo
    if algorithm == 'bogo' and len(array) > 8:
        return jsonify({"error": "Bogo sort is limited to <= 8 elements."}), 400

    response = {"sorted_array": [], "steps": [], "time_taken": 0}

    start_time = time.time()
    if algorithm == 'bubble':
        response["sorted_array"], response["steps"] = bubble_sort(array)
    elif algorithm == 'quick':
        response["sorted_array"], response["steps"] = quick_sort(array)
    elif algorithm == 'merge':
        response["sorted_array"], response["steps"] = merge_sort(array)
    elif algorithm == 'bogo':
        response["sorted_array"], response["steps"] = bogo_sort(array)
    elif algorithm == 'insertion':
        response["sorted_array"], response["steps"] = insertion_sort(array)
    elif algorithm == 'heap':
        response["sorted_array"], response["steps"] = heap_sort(array)
    elif algorithm == 'shell':
        response["sorted_array"], response["steps"] = shell_sort(array)
    elif algorithm == 'radix':
        response["sorted_array"], response["steps"] = radix_sort(array)
    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    response["time_taken"] = round(time.time() - start_time, 4)
    return jsonify(response)

@app.route('/compare', methods=['POST'])
def compare_algorithms():
    data = request.json or {}
    array = data.get('array')

    if array is None:
        return jsonify({"error": "Array is required"}), 400

    try:
        array = [float(x) for x in array]
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. All elements must be numbers."}), 400

    algorithms = ['bubble', 'quick', 'merge', 'insertion', 'heap', 'shell', 'radix']
    results = {}

    for algorithm in algorithms:
        arr_copy = array.copy()
        start_time = time.time()

        if algorithm == 'radix':
            if any((not x.is_integer()) or (x < 0) for x in arr_copy):
                results[algorithm] = {"error": "Requires non-negative integers"}
                continue
            arr_copy = [int(x) for x in arr_copy]

        if algorithm == 'bubble':
            sorted_array, _ = bubble_sort(arr_copy)
        elif algorithm == 'quick':
            sorted_array, _ = quick_sort(arr_copy)
        elif algorithm == 'merge':
            sorted_array, _ = merge_sort(arr_copy)
        elif algorithm == 'insertion':
            sorted_array, _ = insertion_sort(arr_copy)
        elif algorithm == 'heap':
            sorted_array, _ = heap_sort(arr_copy)
        elif algorithm == 'shell':
            sorted_array, _ = shell_sort(arr_copy)
        elif algorithm == 'radix':
            sorted_array, _ = radix_sort(arr_copy)

        time_taken = round(time.time() - start_time, 4)
        results[algorithm] = {"sorted_array": sorted_array, "time_taken": time_taken}

    return jsonify(results)

# ---------- Algoritmi ----------
def bubble_sort(arr):
    arr = arr.copy()
    steps = []
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
            steps.append(arr.copy())
        if not swapped:
            break
    return arr, steps

def quick_sort(arr):
    steps = []
    def _q(a):
        if len(a) <= 1:
            return a
        pivot = a[len(a)//2]
        left  = [x for x in a if x < pivot]
        mid   = [x for x in a if x == pivot]
        right = [x for x in a if x > pivot]
        out = _q(left) + mid + _q(right)
        steps.append(out.copy())
        return out
    return _q(arr.copy()), steps

def merge_sort(arr):
    steps = []
    def merge(left, right):
        res, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i]); i += 1
            else:
                res.append(right[j]); j += 1
        res.extend(left[i:]); res.extend(right[j:])
        return res
    def _m(a):
        if len(a) <= 1:
            return a
        mid = len(a)//2
        l = _m(a[:mid]); r = _m(a[mid:])
        merged = merge(l, r)
        steps.append(merged.copy())
        return merged
    return _m(arr.copy()), steps

def bogo_sort(arr):
    import random
    arr = arr.copy()
    steps = []
    def sorted_(a): return all(a[i] <= a[i+1] for i in range(len(a)-1))
    while not sorted_(arr):
        random.shuffle(arr)
        steps.append(arr.copy())
    return arr, steps

def insertion_sort(arr):
    arr = arr.copy()
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]; j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]; j -= 1
        arr[j+1] = key
        steps.append(arr.copy())
    return arr, steps

def heap_sort(arr):
    arr = arr.copy()
    steps = []
    def heapify(n, i):
        largest = i
        l, r = 2*i + 1, 2*i + 2
        if l < n and arr[l] > arr[largest]: largest = l
        if r < n and arr[r] > arr[largest]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        steps.append(arr.copy())
        heapify(i, 0)
    return arr, steps

def shell_sort(arr):
    arr = arr.copy()
    steps = []
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]; j = i
            while j >= gap and arr[j-gap] > temp:
                arr[j] = arr[j-gap]; j -= gap
            arr[j] = temp
            steps.append(arr.copy())
        gap //= 2
    return arr, steps

def radix_sort(arr):
    arr = arr.copy()
    steps = []
    def counting_sort(exp):
        n = len(arr)
        output = [0]*n
        count = [0]*10
        for i in range(n):
            idx = (arr[i] // exp) % 10
            count[int(idx)] += 1
        for i in range(1, 10):
            count[i] += count[i-1]
        for i in range(n-1, -1, -1):
            idx = (arr[i] // exp) % 10
            output[count[int(idx)] - 1] = arr[i]
            count[int(idx)] -= 1
        for i in range(n):
            arr[i] = output[i]
            steps.append(arr.copy())
    if arr:
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            counting_sort(exp)
            exp *= 10
    return arr, steps

if __name__ == '__main__':
    app.run(debug=True)
