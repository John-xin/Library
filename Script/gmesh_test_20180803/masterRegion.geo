meshSize_dummy2=6;

Point(1)={63.976746,-18.851784,20.0,meshSize_dummy2}; //ptDictNo is 1
Point(2)={-15.292964,-18.851784,20.0,meshSize_dummy2}; //ptDictNo is 2
Point(3)={-15.292964,52.362061,20.0,meshSize_dummy2}; //ptDictNo is 3
Point(4)={63.976746,52.362061,20.0,meshSize_dummy2}; //ptDictNo is 4
Point(8)={-15.292964,-18.851784,0.0,meshSize_dummy2}; //ptDictNo is 8
Point(9)={-15.292964,52.362061,0.0,meshSize_dummy2}; //ptDictNo is 9
Point(14)={63.976746,52.362061,0.0,meshSize_dummy2}; //ptDictNo is 14
Point(19)={63.976746,-18.851784,0.0,meshSize_dummy2}; //ptDictNo is 19
Point(31)={-74.040813,-84.999138,0.0,meshSize_dummy2}; //ptDictNo is 31
Point(32)={-74.040813,115.000862,0.0,meshSize_dummy2}; //ptDictNo is 32
Point(33)={125.959187,115.000862,0.0,meshSize_dummy2}; //ptDictNo is 33
Point(34)={125.959187,-84.999138,0.0,meshSize_dummy2}; //ptDictNo is 34
Point(38)={-74.040813,115.000862,100.0,meshSize_dummy2}; //ptDictNo is 38
Point(39)={125.959187,115.000862,100.0,meshSize_dummy2}; //ptDictNo is 39
Point(43)={-74.040813,-84.999138,100.0,meshSize_dummy2}; //ptDictNo is 43
Point(44)={125.959187,-84.999138,100.0,meshSize_dummy2}; //ptDictNo is 44
Line(1)={1,2};
Line(2)={2,3};
Line(3)={3,4};
Line(4)={4,1};
Line(6)={2,8};
Line(7)={8,9};
Line(8)={9,3};
Line(11)={9,14};
Line(12)={14,4};
Line(15)={14,19};
Line(16)={19,1};
Line(19)={19,8};
Line(25)={31,32};
Line(26)={32,33};
Line(27)={33,34};
Line(28)={34,31};
Line(30)={32,38};
Line(31)={38,39};
Line(32)={39,33};
Line(34)={38,43};
Line(35)={43,44};
Line(36)={44,39};
Line(38)={31,43};
Line(44)={44,34};
Line Loop(1)={1,2,3,4};
Line Loop(2)={-2,6,7,8};
Line Loop(3)={-3,-8,11,12};
Line Loop(4)={-4,-12,15,16};
Line Loop(5)={-1,-16,19,-6};
Line Loop(6)={-19,-15,-11,-7};
Line Loop(7)={25,26,27,28};
Line Loop(8)={-26,30,31,32};
Line Loop(9)={-31,34,35,36};
Line Loop(10)={-25,38,-34,-30};
Line Loop(11)={-27,-32,-36,44};
Line Loop(12)={-28,-44,-35,-38};
Plane Surface(1)={1};
Plane Surface(2)={2};
Plane Surface(3)={3};
Plane Surface(4)={4};
Plane Surface(5)={5};
Plane Surface(6)={6,7};
Plane Surface(7)={8};
Plane Surface(8)={9};
Plane Surface(9)={10};
Plane Surface(10)={11};
Plane Surface(11)={12};
Surface Loop(1)={1,2,3,4,5,6,7,8,9,10,11};
Volume(1)={1};

Physical Surface("inlet") = {7};
Physical Surface("outlet") = {11};
Physical Surface("ground") = {6};
Physical Surface("lateral") = {8,9,10};
Physical Surface("interface_outer") = {1:5};
Physical Volume("domain")={1};

Transfinite Line {7, 8, 11, 3, 2, 6, 19, 1, 16, 4, 15, 12} = 20 Using Progression 1;
Transfinite Surface {1:5};
Recombine Surface {1:5};

//+

