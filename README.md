# Top-k Queries Algorithm for Aggregating Restaurant Ratings

## Overview

This project implements an algorithm to calculate the **top-k queries** for aggregating individual scores of objects (e.g., restaurants) from three different sources. The goal is to find the **top-k objects** based on their combined scores across these sources. The objects in this case are restaurants, and the three sources represent reviews from different platforms (e.g., Google, TripAdvisor, and Yelp).

Each source provides individual scores, which are averaged ratings that a restaurant received on that specific website. The objective is to aggregate the scores from the three sources and identify the top-k restaurants based on the sum of their ratings.

### Data Sources

- **seq1.txt**: Contains restaurant scores, sorted in descending order, and allows only **sequential access**.
- **seq2.txt**: Contains restaurant scores, sorted in descending order, and allows only **sequential access**.
- **rnd.txt**: Contains restaurant scores sorted by restaurant ID and allows **random access**.

In each file, the format is as follows:
- **First column**: Restaurant (object) ID.
- **Second column**: Restaurant score on the respective platform.

The scores in each source range from **0.0 to 5.0**.

### Problem Definition

Given the three sources and a positive integer **k** (the number of top-rated restaurants to be retrieved), the task is to calculate and return the **top-k restaurants** based on the **sum** of their ratings across all three sources.

### Approach

1. **Read `rnd.txt` Entirely:**
   - First, read the entire contents of `rnd.txt` and store the scores in an array `R`, where the position `x` of the array corresponds to the score of the object with ID = `x`.
   - For example, `R[0] = 2.07`, `R[1] = 2.33`, and so on.

2. **Process `seq1.txt` and `seq2.txt` in Round-Robin:**
   - Alternate between reading lines from `seq1.txt` and `seq2.txt` in a **round-robin** manner. Each line contains the object ID and the score for that object in the respective source.
   - **Sequential Access:** Only process one line at a time from `seq1.txt` and `seq2.txt`. You are not allowed to load these files entirely into memory.

3. **Score Calculation:**
   - For each object with ID = `x` read from either `seq1.txt` or `seq2.txt`:
     - If this object is seen for the **first time**, initialize its **lower bound score** by adding the score from the current source to its score in `rnd.txt` (accessed via `R[x]`).
     - If the object has been seen previously (from another source), update its **total score** by adding the score from the current source to the **existing lower bound** (since we now have scores from all three sources).

4. **Top-k Tracking with Min-Heap:**
   - Once you have seen exactly **k objects**, initialize a **min-heap (`Wk`)** to store the **top-k objects** based on their lower or total scores. The heap will contain the current top-k objects, and the root of the heap will have the **smallest score** among the top-k objects seen so far.
   - Continue alternating between `seq1.txt` and `seq2.txt`, updating scores for each new object or updating an object's total score if it's seen in another source.

5. **Threshold Calculation and Early Termination:**
   - After each sequential access (one line from `seq1.txt` or `seq2.txt`), update the **Threshold `T`** as:
     ```
     T = last score seen in seq1.txt + last score seen in seq2.txt + 5.0
     ```
   - The **threshold `T`** represents the **best possible score** that any unseen object could achieve based on the maximum possible score (5.0) from the third source.
   - **Termination condition:** As long as the score of the top object in the heap `Wk` is **smaller than `T`**, continue processing more sequential accesses from `seq1.txt` and `seq2.txt`. Once the score of the top object in `Wk` becomes **greater than or equal to `T`**, we can potentially terminate.

6. **Final Checks Before Termination:**
   - Before terminating, ensure there are no objects that we have already seen, but which are not in `Wk`, and their **upper bound score** (i.e., the score they could still achieve based on the remaining source) is greater than the top object in `Wk`.
   - If such objects exist, continue sequential accesses to update their scores; otherwise, terminate and return the top-k objects stored in `Wk`.

### Example Walkthrough

1. Suppose we read object `33136` from `seq1.txt`, which has a score of **5.00**. We access `R[33136]` from `rnd.txt` and retrieve a score of **4.40**. The **lower bound score** for object `33136` becomes:
   ```
   5.00 (from seq1.txt) + 4.40 (from rnd.txt) = 9.40
   ```

2. Later, when we read object `33136` from `seq2.txt`, the score is **4.28**. We now have the complete score for object `33136`:
   ```
   9.40 (current lower bound) + 4.28 (from seq2.txt) = 13.68 (total score)
   ```

3. After seeing exactly **k objects**, we initialize the heap `Wk` with these objects based on their lower or total scores.

4. The threshold `T` is updated after each access, and we continue processing until the termination condition is met.

### Program Flow

1. **Read and store `rnd.txt`** in array `R`.
2. **Process `seq1.txt` and `seq2.txt`** in a round-robin fashion, updating object scores.
3. **Maintain a min-heap** to store the top-k objects based on their scores.
4. **Update the threshold** and check for termination conditions.
5. **Terminate and print the top-k objects** once the threshold allows for termination.

### Conclusion

This algorithm efficiently finds the top-k objects from three different sources with limited access patterns. By leveraging sequential and random accesses and maintaining a dynamic heap for top-k results, it ensures that the program minimizes unnecessary data reads and terminates as early as possible based on the computed threshold.
