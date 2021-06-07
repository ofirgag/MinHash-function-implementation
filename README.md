# MinHash-function-implementation
This repo includes an implementation of the MinHash function combined with the banding technique. This allows the user to create an LSH (Locality Sensitivity Hash) signature for texts (like file names)

# MinHash function and banding technique
The MinHash function is useful when trying to find the similarity between sets. In our case, each file name/software name (or simply name) represents a set of tri-grams
derived from the name's words. Given a set of tri-grams, the MinHash function outputs a signature. We now elaborate on the process of calculating a signature for a
given set of tri-grams of a given name. First we build a characteristic matrix (CM).
The CM rows defined by all possible tri-grams, overall there are 26^3 = 17; 576 possible tri-grams (26 letters), hence the matrix has 17,576 rows.
The matrix columns defined by all the names. The matrixcells filled according to the next definition:

<img width="500" alt="2021-06-07_15h02_57" src="https://user-images.githubusercontent.com/19409406/121013650-cabd5580-c7a1-11eb-8b0c-f6bed206fba7.png">

Next we define 100 different hash functions of the form:

<img width="300" alt="2021-06-07_15h03_03" src="https://user-images.githubusercontent.com/19409406/121013695-d90b7180-c7a1-11eb-93da-6d2406e6dd9c.png">

for random ai, bi and i in [1, 100]. The input x represents the tri-gram position in [0, 26^3 - 1] defined according alphabetic order. We define the set of hash functions as
H.

At this stage we calculate the signature matrix (SM). The SM rows defined by all hash functions (100 overall). The matrix columns defined by all the names. The
matrix cells filled according to the next Algorithm:

<img width="600" alt="2021-06-07_15h03_06" src="https://user-images.githubusercontent.com/19409406/121014013-2c7dbf80-c7a2-11eb-9b8b-5ead14af751f.png">

In practice, we only iterate through the non-zero elements. Each column in the SM represents a 100 length signature of a file name/software name
(or simply name). Next we apply on the SM the banding technique. We split each signature into 25 bands of length 4 each. Each of this 4 length number represents a band tuple.
