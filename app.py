from flask_cors import CORS
from flask import Flask, request, jsonify
import time

#initializare Flask si activare CORS (pentru a permite cereri din alte domenii)
app = Flask(__name__)
CORS(app)

#ruta pentru sortare sir
@app.route('/sort', methods=['POST'])
def sort_array():
    data = request.json
    array = data.get('array') #sirul pentru sortat
    algorithm = data.get('algorithm') #algoritmul de sortare ales
    data_type = data.get('type', 'number') #tipul datelor din sir

#varificare daca datele necesare sunt furnizate
    if not array or not algorithm:
        return jsonify({"error": "Array and algorithm are required"}), 400

    if data_type == 'number':
        try:
            array = [float(x) for x in array] 
        except ValueError:
            return jsonify({"error": "Invalid input. All elements must be numbers."}), 400
    elif data_type == 'string':
        array = [str(x) for x in array]

    response = {"sorted_array": [], "steps": [], "time_taken": 0}

#cronometrarea sortarii (not functional)
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
        if data_type == 'string':
            return jsonify({"error": "Radix sort only supports numbers."}), 400
        response["sorted_array"], response["steps"] = radix_sort(array)
    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    response["time_taken"] = round(time.time() - start_time, 4)
    return jsonify(response)

@app.route('/compare', methods=['POST'])
def compare_algorithms():
    data = request.json
    array = data.get('array')

    if not array:
        return jsonify({"error": "Array is required"}), 400

    try:
        array = [float(x) for x in array]
    except ValueError:
        return jsonify({"error": "Invalid input. All elements must be numbers."}), 400

    algorithms = ['bubble', 'quick', 'merge', 'insertion', 'heap', 'shell', 'radix']
    results = {}

    for algorithm in algorithms:
        start_time = time.time()
        if algorithm == 'bubble':
            sorted_array, _ = bubble_sort(array.copy())
        elif algorithm == 'quick':
            sorted_array, _ = quick_sort(array.copy())
        elif algorithm == 'merge':
            sorted_array, _ = merge_sort(array.copy())
        elif algorithm == 'insertion':
            sorted_array, _ = insertion_sort(array.copy())
        elif algorithm == 'heap':
            sorted_array, _ = heap_sort(array.copy())
        elif algorithm == 'shell':
            sorted_array, _ = shell_sort(array.copy())
        elif algorithm == 'radix':
            sorted_array, _ = radix_sort(array.copy())

        time_taken = round(time.time() - start_time, 4)
        results[algorithm] = {"sorted_array": sorted_array, "time_taken": time_taken}

    return jsonify(results)

#functia bubble sort
def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            steps.append(arr.copy())
    return arr, steps

#functia quick sort
def quick_sort(arr): 
    steps = []

    def _quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        sorted_array = _quick_sort(left) + middle + _quick_sort(right)
        steps.append(sorted_array)
        return sorted_array

    return _quick_sort(arr), steps

#functia merge sort
def merge_sort(arr):
    steps = []

    def _merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        merged = merge(left, right)
        steps.append(merged)
        return merged

    return _merge_sort(arr), steps

#functie interclasare
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

#functia bogo sort :))
def bogo_sort(arr):
    import random
    steps = []

    def is_sorted(arr):
        return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

    while not is_sorted(arr):
        random.shuffle(arr)
        steps.append(arr.copy())
    return arr, steps

#functia de insertion sort
def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append(arr.copy())
    return arr, steps

def heap_sort(arr):
    steps = []

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        steps.append(arr.copy())
        heapify(arr, i, 0)

    return arr, steps

def shell_sort(arr):
    steps = []
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
            steps.append(arr.copy())
        gap //= 2
    return arr, steps

def radix_sort(arr):
    steps = []

    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]
            steps.append(arr.copy())

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

    return arr, steps

if __name__ == '__main__':
    app.run(debug=True)

from flask_cors import CORS
from flask import Flask, request, jsonify
import time

app = Flask(__name__)
CORS(app)

@app.route('/sort', methods=['POST'])
def sort_array():
    data = request.json
    array = data.get('array')
    algorithm = data.get('algorithm')
    data_type = data.get('type', 'number')

    if not array or not algorithm:
        return jsonify({"error": "Array and algorithm are required"}), 400

    if data_type == 'number':
        try:
            array = [float(x) for x in array] 
        except ValueError:
            return jsonify({"error": "Invalid input. All elements must be numbers."}), 400
    elif data_type == 'string':
        array = [str(x) for x in array]

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
    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    response["time_taken"] = round(time.time() - start_time, 4)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
