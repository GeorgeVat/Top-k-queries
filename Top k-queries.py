import sys
import itertools
import heapq

def top_boundry_checker(seq1,seq2):
    """ Check if the top boundary score for each object is bigger than the top Wk item.
        Returns True if there is at least one top boundary score bigger than Wk.
    """
    for key in scores:
        # If the len is < 3 it means that the object has no final score
        if len(scores[key]) < 3 and (key,scores[key]) not in Wk: 
            # We add the score from the sequence where we haven't seen the X.
            if scores[key][1] == 1:
                top_boundry = scores[key][0] + seq1
            else:
                top_boundry = scores[key][0] + seq2

            # If there is bigger top boundry we continue the iterations
            if top_boundry > Wk[0][1][0]:
                return True
    return False

# Taking the k argument from the command line
try:
    k = int(sys.argv[1])
    if k <= 0:
        raise ValueError
except (ValueError):
    sys.exit(1)


# Open and read the 'rnd.txt' file
with open('rnd.txt', 'r') as file:
    rndData = [line.strip() for line in file.readlines()]

# Extract the ratings from the 'rnd.txt' data, casting them as floats
rndData = [float(line.split(' ')[1]) for line in rndData]

# Dictionary to store object scores
scores = {}

seqAccesses = 0
with open('seq1.txt', 'r') as seq1_file, open('seq2.txt', 'r') as seq2_file:
     # Open 'seq1.txt' and 'seq2.txt' files simultaneously and iterate over the lines
    for seq in itertools.chain.from_iterable(itertools.zip_longest(seq1_file, seq2_file)):
        # Counter of accesses
        seqAccesses += 1
        
        # Extract the seq ID and seq rating from the line
        segID = int(seq.split(' ')[0])
        seqRating = float(seq.split(' ')[1])

        # Hold the seq rating separately for each file to distinguish which  file we are iterating over
        if seqAccesses % 2 != 0:
            seq2 = seqRating
            seqFlag = 1 # seqFlag helps us know in which seq we found the last object
        else:
            seq1 = seqRating
            seqFlag = 2

        # Update lower bound if we've seen this object before
        if segID in scores:
            # Insert the total score in the first place
            scores[segID].insert(0,scores[segID][0] + seqRating)
       
        # Initialize lower bound if we haven't seen this object before
        else:
            scores[segID] = []
            scores[segID].append(seqRating + rndData[segID])
            scores[segID].append(seqFlag)
        
        # When the accesses are >= k, create the heap 
        if k <= seqAccesses: 
            # Get the k objects with the highest scores
            Wk = heapq.nlargest(k, scores.items(), key=lambda x: x[1][0])
            # Rearrange the heap in accending order
            Wk = heapq.nsmallest(k, Wk, key=lambda x: x[1][0])

            thresholdT = seq1 + seq2 + 5.0

            if thresholdT <= Wk[0][1][0] and not top_boundry_checker(seq1,seq2):
                break
            

print('Number of sequential accesses= ', seqAccesses)
print('Top ',k,'objects')
for item in reversed(Wk):
    print(str(item[0])+':',"{:.2f}".format(item[1][0]))


