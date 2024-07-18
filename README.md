# Thistlethwaite-polynomial

In his paper, "A Spanning Tree Exansion of the Jones Polynomial," Thistlethwaite defines a polynomial for signed graphs.

This program takes a signed and connected graph as an input and returns the corresponding value of Thistlethwaite's polynomial.

An example of a correct input would be "1+2,2+3,3+1" : this example is a triangle with three positive edges - the vertices are labelled "1," "2," and "3," and the triple "2+3" means that vertices 2 and 3 are connected by a positive edge. Another example of a correct input would be "1+2,2+3,3-4,4-1" : this example is a square with two adjacent edges being positive and the other two edges being negative. 

The order of the of the vertices in the input does not matter. The numbers used to label the vertices also doesn't matter. For example, "5+10,27+999,27+5,999+10" is a valid input : it is a square with four positive edges. 
