
module board(){
	difference(){
		cube([214,214,4]);
		translate([4,4,-.5]) cubes();
	}
}
piece();
module piece(){
	translate([4.5,4.5,0]) cube([9,9,5]);
	translate([3.0,3.0,4]) cube([12,12,5]);
	//translate([7.5,3.0,9]) cube([3,12,5]);
}

module cubes(){
	for (i = [0:14]){
		for (j = [0:14]){
			translate([i*14,j*14,0]) cube([10,10,5]);
		}
	}
}
