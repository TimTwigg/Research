
module board(){
	difference(){
		cube([214,214,4]);
		translate([4,4,-.5]) cubes();
	}
}
//piece();
module piece(){
	translate([4.5,4.5,0]) cube([9,9,5]);
	translate([3.0,3.0,4]) cube([12,12,5]);
	//translate([7.5,3.0,9]) cube([3,12,5]);
}

module roundedpiece(){
	//%translate([0,0,0]) cube([9,9,5],center=true);
    translate([0,0,-2.5]) cylinder(d=9, h=5);
	translate([0,0,4]) cube([12,12,5],center=true);
	//translate([7.5,3.0,9]) cube([3,12,5]);
}
module cubes(){
	for (i = [0:14]){
		for (j = [0:14]){
			translate([i*14,j*14,0]) cube([10,10,5]);
		}
	}
}

translate([13,-27,0]) corner();
translate([-13,-27,0]) rotate([0,0,90]) corner();
translate([13,-2,0]) roundedpiece();
translate([13,11,0]) roundedpiece();
translate([13,24,0]) roundedpiece();
translate([-13,-2,0]) roundedpiece();
translate([-13,11,0]) roundedpiece();
translate([-13,24,0]) roundedpiece();
straight();
translate([0,-37,0]) straight();
module corner(){
	roundedpiece();
	translate([0,12,0]) roundedpiece();
	translate([12,0,0]) roundedpiece();
}

module straight(){
	roundedpiece();
	translate([0,12,0]) roundedpiece();
	translate([0,24,0]) roundedpiece();
}
