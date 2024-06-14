# Programming Task 5

## Graph Search Algorithm
### Course: IT00CD89-3005 Graph Algorithms 

-------
**Submitted By:**
**MD Hasibul Haque Zahid (2302302)** 

-------

### Implementation

This Python script implements the maximum-cardinality edge matching algorithm based on blossom contraction. The input graph data is read from a CSV file, and the script outputs a TXT file containing a comma-separated list of edge IDs representing a maximum-cardinality edge matching.

-------
### Algorithm Working Process

The algorithm starts by reading the graph data from a CSV file and constructing a graph object. It then applies blossom contraction to find augmenting paths and augment the matching iteratively until no more augmenting paths can be found. Finally, it extracts the matched edge IDs and writes them to a TXT file.

-------
### Testing Process

The script was tested using a dataset named "benchmark4.csv". The output of the script was a TXT file containing a comma-separated list of edge IDs representing a maximum-cardinality edge matching.

-------
### The correctness of the output was verified manually by:

Checking that the output edge IDs match the expected maximum-cardinality matching.
Confirming that all edges in the matching are non-overlapping and form a valid matching:
   - Maximum cardinality matching: `e12, e34, e56, e79, e810`
   - Verification:
     - `e12`: (n1, n2)
     - `e34`: (n3, n4)
     - `e56`: (n5, n6)
     - `e79`: (n7, n9)
     - `e810`: (n8, n10)
   - All edges are non-overlapping and form a valid matching.
