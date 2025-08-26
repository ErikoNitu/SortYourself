function showCategory(categoryId) {
    const categories = document.querySelectorAll('.category-content');
    categories.forEach(category => category.style.display = 'none');
    document.getElementById(categoryId).style.display = 'block';
}

function displayArrayOnSeparateLines(container, arr, stepNumber) {
    const maxLines = 10;
    const line = document.createElement('div');
    line.textContent = `Step ${stepNumber}: ${arr.join(', ')}`;
    container.appendChild(line);

    if (container.childElementCount > maxLines) {
        container.removeChild(container.firstChild);
    }
}

async function runVisualization(inputId, algorithm, visualizationId) {
    const input = document.getElementById(inputId).value.trim();
    if (!input) {
        alert("Please enter a valid input.");
        return;
    }

    const array = input.split(',').map(x => isNaN(x) ? x.trim() : Number(x));
    const container = document.getElementById(visualizationId);
    container.innerHTML = '';
    const response = await fetch('/sort', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ array: array, algorithm: algorithm, type: typeof array[0] === 'number' ? 'number' : 'string' })
    });

    const result = await response.json();
    if (result.error) {
        container.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
        return;
    }

    let stepNumber = 1;
    result.steps.forEach(step => {
        displayArrayOnSeparateLines(container, step, stepNumber++);
    });

    const algorithmDetails = document.getElementById("algorithmDetails");
    const videoURL = getVideoUrl(algorithm);
    const description = getAlgorithmDescription(algorithm);

    algorithmDetails.innerHTML = `
        <iframe src="${videoURL}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        <div class="algorithm-description">${description}</div>
    `;
}

function runNumberSort() {
    const algorithm = document.getElementById('numberAlgorithmSelect').value;
    runVisualization('numberInput', algorithm, 'numberVisualization');
}

function runStringSort() {
    runVisualization('stringInput', 'bubble', 'stringVisualization');
}

function getVideoUrl(algorithm) {
    switch (algorithm) {
        case 'bubble':
            return 'https://www.youtube.com/embed/Cq7SMsQBEUw';
        case 'quick':
            return 'https://www.youtube.com/embed/8hEyhs3OV1w';
        case 'merge':
            return 'https://www.youtube.com/embed/ZRPoEKHXTJg';
        case 'bogo':
            return 'https://www.youtube.com/embed/DaPJkYo2quc&t=5s';
        case 'insertion':
            return 'https://www.youtube.com/embed/8oJS1BMKE64';
        case 'heap':
            return 'https://www.youtube.com/embed/_bkow6IykGM';
        default:
            return '';
    }
}

function getAlgorithmDescription(algorithm) {
    switch (algorithm) {
        case 'bubble':
            return `
<pre><code>#include &lt;stdio.h&gt;
void bubbleSort(int arr[], int n) {
    int i, j, temp;
    for (i = 0; i &lt; n - 1; i++) {
        for (j = 0; j &lt; n - i - 1; j++) {
            if (arr[j] &gt; arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
</code></pre>`;
        case 'quick':
            return `
<pre><code>#include &lt;stdio.h&gt;
void quickSort(int arr[], int low, int high) {
    int pivot, i, j, temp;
    if (low &lt; high) {
        pivot = arr[high];
        i = low - 1;
        for (j = low; j &lt; high; j++) {
            if (arr[j] &lt; pivot) {
                i++;
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        quickSort(arr, low, i);
        quickSort(arr, i + 2, high);
    }
}
</code></pre>`;
        case 'merge':
            return `
<pre><code>#include &lt;stdio.h&gt;
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1, n2 = r - m;
    int L[n1], R[n2];
    for (int i = 0; i &lt; n1; i++) L[i] = arr[l + i];
    for (int i = 0; i &lt; n2; i++) R[i] = arr[m + 1 + i];
    int i = 0, j = 0, k = l;
    while (i &lt; n1 &amp;&amp; j &lt; n2) {
        if (L[i] &lt;= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i &lt; n1) arr[k++] = L[i++];
    while (j &lt; n2) arr[k++] = R[j++];
}
</code></pre>`;
        case 'bogo':
            return `
<pre><code>#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;time.h&gt;
int isSorted(int arr[], int n) {
    for (int i = 0; i &lt; n - 1; i++) if (arr[i] &gt; arr[i + 1]) return 0;
    return 1;
}
void bogoSort(int arr[], int n) {
    while (!isSorted(arr, n)) {
        for (int i = 0; i &lt; n; i++) {
            int j = rand() % n;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
}
</code></pre>`;
        case 'insertion':
            return `
<pre><code>#include &lt;stdio.h&gt;
void insertionSort(int arr[], int n) {
    int i, key, j;
    for (i = 1; i &lt; n; i++) {
        key = arr[i];
        j = i - 1;
        while (j &gt;= 0 &amp;&amp; arr[j] &gt; key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
</code></pre>`;
        case 'heap':
            return `
<pre><code>#include &lt;stdio.h&gt;
void heapify(int arr[], int n, int i) {
    int largest = i, left = 2 * i + 1, right = 2 * i + 2, temp;
    if (left &lt; n &amp;&amp; arr[left] &gt; arr[largest]) largest = left;
    if (right &lt; n &amp;&amp; arr[right] &gt; arr[largest]) largest = right;
    if (largest != i) {
        temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        heapify(arr, n, largest);
    }
}
void heapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i &gt;= 0; i--) heapify(arr, n, i);
    for (int i = n - 1; i &gt;= 0; i--) {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        heapify(arr, i, 0);
    }
}
</code></pre>`;
        default:
            return '';
    }
}

window.onload = function() {
    showCategory('number-sorting');
};
