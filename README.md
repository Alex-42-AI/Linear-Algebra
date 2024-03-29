# Linear-Algebra
The file Vectors.py contains implementations of 2D and 3D vectors.The 2D vector is like a 3D vector with a z coordinate equal to zero, so Vector3D inherits from it.
The vectors have methods for:
1) getting the polar coordinates of the vector;
2) getting the dot product of two vectors;
3) checking whether two vectors are parallel;
4) checking whether two vectors are perpendicular;
5) getting the mixed product of three vectors;
6) getting the opposite vector of the given;
7) getting the length of the vector;
8) addition and subtraction of two vectors;
9) vector product of two vectors;
10) dividing the vector by a number;
11) checking whether two vectors are equal.

The Matrix.py file has an implementation of a matrix, along with some necessary functions. It also has methods, for:
1) checking whether the matrix is squared;
2) transposing the matrix;
3) returning a matrix, result of neutralising the elements under the main diagonal of the original one, as well as the number of inversions made;
4) checking whether the rows of the matrix are linearly dependent;
5) calculating the determinant of the matrix - one via neutralising its elements under the main diagonal and another using recursion;
6) negation of the matrix;
7) sum, difference, product and division of two matrices;
8) product, division and powering of a matrix with a number;
9) checking whether two matrices are equal.

The file with many functions and mathematical formulas contains the function round_if_possible. It is necessary, because sometimes, when dividing two numbers, the result will return something like 5.99999999999999996 or 6.00000000000000002 instead of 6. The rest of the functions are pretty self-explanatory. There is also an implementation of a rational number.
