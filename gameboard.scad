
difference(){
	cube([214,214,2]);
	translate([4,4,-.5]) cubes();
}

module cubes(){
	for (i = [0:14]){
		for (j = [0:14]){
			translate([i*14,j*14,0]) cube([10,10,5]);
		}
	}
}
