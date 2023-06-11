# Top-k-queries

The goal of the work is to develop an algorithm for top-k queries, which aggregate individual scores of objects from three sources. The objects can be restaurants, with each source being a restaurant review website (e.g., Google, TripAdvisor, Yelp), and the individual score of an object in a source is the average of the ratings the restaurant received on that specific website.

The two initial sources, seq1 and seq2, allow only sequential accesses. In seq1 and seq2, the objects are sorted in descending order of their individual scores. The third source, rnd, allows only random accesses. In rnd, the objects are sorted based on their ID. The data from the sources are stored in the files seq1.txt, seq2.txt, and rnd.txt, respectively. Note that the minimum possible individual score of an object in a source is 0.0, and the maximum possible score is 5.0. In each line of a file, the first number represents the object's ID, and the second number represents the individual score in that specific source. The goal of the queries we want to evaluate is to find the top-rated restaurants based on the sum of their ratings in the three sources.

The task is to write a program that takes a positive integer k as a command-line argument and calculates and prints the top-k objects from the three sources using the sum function. For example, the top-1 object is 50905 with a total score of 14.84.

The program should first read the rnd.txt file in its entirety and store the scores of the objects in a main memory data structure (array) R, where position x of the array contains the individual score of the object with ID=x. For example, R[0] = 2.07, R[1] = 2.33, etc. Then, the program should read lines from seq1.txt and seq2.txt alternately (round-robin). Note: You should not read the seq1.txt and seq2.txt files entirely into main memory structures like arrays or lists. For each object with ID=x that we read sequentially from seq1.txt or seq2.txt:

•	If we haven't seen object x before, we initialize the lower bound of its total score to be the score we just read sequentially plus the score R[x] (assuming a random access to the R array to retrieve R[x]).

•	If we have seen object x before, it means we already have a lower bound for x. In this case, we add the individual score we just read to the lower bound to obtain the complete score of x (because now we have seen x in all three sources).


To illustrate the process described, let's consider an example:

Suppose we read object 33136 from seq1.txt, which has a score of 5.00 in seq1. We access R[33136] and retrieve a score of 4.40, which we add to the lower bound, resulting in a lower bound score of 9.40 for object 33136. Later, when we sequentially access 33136 from seq2.txt, we obtain a score of 4.28 in seq2, which is added to 9.40, yielding a total score of 13.68 for object 33136.

Once we have exactly seen k objects, initialize a min-heap Wk to store the top-k objects so far based on their lower bounds or exact scores. The top element of Wk should have the smallest lower bound score among the top-k objects seen so far.

Afterward, continue alternating between accessing seq1.txt and seq2.txt. After each access and update of a lower bound or total score, update the Threshold T as follows: T = last score seen in seq1.txt + last score seen in seq2.txt + 5.0. T represents the best possible score of any object we haven't seen so far. As long as the score of the top object in Wk is smaller than T, we cannot terminate and need to perform additional sequential accesses in seq1.txt and seq2.txt.

When T becomes smaller than or equal to the top element of Wk, it is possible to terminate. In this case, you should check if there is any object x that we have already seen but is not in Wk, and its upper bound is greater than that of the top object in Wk. If such an object exists, continue with sequential accesses. Otherwise, terminate and print Wk as the final result. The upper bound of an object x can be calculated by adding the last score we sequentially read in the source where we haven't seen x yet to its lower bound (which we already know).

