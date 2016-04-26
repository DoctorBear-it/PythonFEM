// Gmsh project created on Thu Apr 21 19:18:47 2016
Point(1) = {0, 0, 0, 1.0};
Point(2) = {0, 1, 0, 1.0};
Point(3) = {1, 1, 0, 1.0};
Point(4) = {1, 0, 0, 1.0};
Line(1) = {2, 3};
Line(2) = {3, 4};
Line(3) = {4, 1};
Line(4) = {1, 2};
Line Loop(5) = {4, 1, 2, 3};
Plane Surface(6) = {5};
Coherence;
Coherence;
