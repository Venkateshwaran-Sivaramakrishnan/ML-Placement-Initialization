# Results:

## Iteration Count and HPWL Values: 

### Baseline Results

| Design | Tech      | # Iterations | Est. Wirelength (µm) |
|--------|-----------|--------------|-----------------------|
| gcd    | asap7     | 420          | 985.547               |
| gcd    | nangate45 | 620          | 3216.71               |
| ibex   | nangate45 | 19000        | 278282                |

---

### Our Method Results

## Our Method Results

| Design | Tech      | # Iterations | Est. Wirelength (µm) | HPWL Improved       | Iteration Count Improved |
|--------|-----------|--------------|-----------------------|----------------------|---------------------------|
| gcd    | asap7     | 420          | 3139.76               |                      |                           |
| gcd    | nangate45 | 620          | 3165.16               | <p align="center">✅</p> |                           |
| ibex   | nangate45 | 19000        | 263830                | <p align="center">✅</p> |                           |

---

## Runtime Summary

| Design | Tech       | Extraction Time (s) | Clustering Time (s) | Mapping Time (s) |
|--------|------------|---------------------|----------------------|------------------|
| gcd    | asap7      | 1.01                | 1.92                 | 0.85             |
| gcd    | nangate45  | 0.89                | 1.24                 | 0.85             |
| ibex   | nangate45  | 4.93                | 192.11               | 31.71            |
| jpeg   | asap7      | 5.38                | 1325.56              | 251.55           |
| jpeg   | nangate45  | 1.85                | 1543.82              | 326.45           |

---
