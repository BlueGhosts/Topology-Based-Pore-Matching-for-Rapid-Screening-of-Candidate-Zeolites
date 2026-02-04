#!perl

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);
use POSIX qw(floor);
use File::Basename;
my ($import_dirname, $output_dirname) = @ARGV;
#my $import_dirname= "P:/Project/Program/PoresTopology/FindByBA";
#my $output_dirname = "P:/Project/Program/PoresTopology/FindByBA";
#$outfilepath = "$outfilepath.csv";

#opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
#open(my $OUT, '>', $outfilepath) or die "Error to open $outfilepath $!";

#print "filename,MinZAAngle\n";
#print $OUT "filename,MinZAAngle\n";

BatchCalculate($import_dirname, $output_dirname);
#my $doc = $Documents{"CHA-PPT 1_6.xsd"};
#GetBondAndAngle($doc, 'Lr');

sub BatchCalculate(){
	my $import_dirname = $_[0];
    my $output_dirname = $_[1];

	opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
	while (my $file = readdir($dir)) {
	    if ($file =~ /\.cif$/i) {
	        print "$file\n";  
	        my $filename = $file;
	        $filename =~ s|.*/||;  
	        my $filename_with_ext = basename($file);
		    my $filename = $filename_with_ext;
		    $filename =~ s/\.[^.]+$//;
    
	    	my $doc = Documents->Import("$import_dirname/$file");
	    	my $outpath = "$output_dirname/$filename.txt";
	    	GetBondAndAngle($doc, 'Lr', $outpath, $filename);

	        $doc -> discard;   
	    }
	}
	closedir($dir);
}

sub GetBondAndAngle(){
	my $doc = $_[0];
	my $poreElement = $_[1];
	my $outpath = $_[2];
	my $filename = $_[3];
	
	open(my $OUT, '>', $outpath) or die "Error to open $outpath $!";

	#print "filename,MinZAAngle\n";
	print $OUT "$filename\n";
	print $OUT "Bond\n";
	
	my $bonds = $doc->AsymmetricUnit->Bonds;
	my %bondOrder_name;
	my $order = 1;	
	foreach my $bond (@$bonds) {
		my $atom1 = $bond->Atom1;
    	my $atom2 = $bond->Atom2;
    	
 		my $element1 = $atom1->ElementSymbol;
		my $element2 = $atom2->ElementSymbol;
		if (($element1 ne $poreElement) or ($element2 ne $poreElement)){
			next;
		}
		
    	my $name1 = $atom1->Name;
    	my $name2 = $atom2->Name;
    	
    	my $xyz1 = $atom1->FractionalXYZ;
    	my $xyz2 = $atom2->FractionalXYZ;
    	
	    my $x1 = sprintf("%.4g", $xyz1->X);
	    my $y1 = sprintf("%.4g", $xyz1->Y);
	    my $z1 = sprintf("%.4g", $xyz1->Z);
	    		    	
	    my $x2 = sprintf("%.4g", $xyz2->X);
	    my $y2 = sprintf("%.4g", $xyz2->Y);
	    my $z2 = sprintf("%.4g", $xyz2->Z);
	    
	    my $length =  sprintf("%.4g", $bond->Length);
	    
	    $bondOrder_name{$order}  = [$name1,$name2];
		print $OUT "Bond$order,$name1($x1;$y1;$z1),$name2($x2;$y2;$z2),$length\n";
		$order++;
	}

	print $OUT "Angle\n";
	my $atoms = $doc->AsymmetricUnit->Atoms;
	foreach my $atom (@$atoms) {
		my $element = $atom->ElementSymbol;
	    my $numBonds = $atom -> NumBonds;
	    if ( $element ne $poreElement or $numBonds < 2){
	    	next;
	    }
	    #print("$numBonds \n");
    	my $attachingBonds = $atom->Bonds;
		my $order = 1;
    	for (my $i = 0; $i < @$attachingBonds; $i++) {
		    for (my $j = $i + 1; $j < @$attachingBonds; $j++) {
		    	my $bond1 = @$attachingBonds[$i];
		    	my $bond2 = @$attachingBonds[$j];
		    	my $atom1;
		    	my $atom2;
		    	if (Distance($atom->XYZ, $bond1->Atom1->XYZ)){
		    		$atom1 = $bond1->Atom1;
		    	}
		    	else{
		    		$atom1 = $bond1->Atom2;
		    	}
		    	
		    	if (Distance($atom->XYZ, $bond2->Atom1->XYZ)){
		    		$atom2 = $bond2->Atom1;
		    	}
		    	else{
		    		$atom2 = $bond2->Atom2;
		    	}
		    	my $bondOrder1;
		    	my $bondOrder2;

				foreach my $bondOrder (keys %bondOrder_name) {
				    my @bondAtomNames = @{$bondOrder_name{$bondOrder}};
				
				    if (($atom->{Name} eq $bondAtomNames[0] and $atom1->{Name} eq $bondAtomNames[1]) or
				        ($atom->{Name} eq $bondAtomNames[1] and $atom1->{Name} eq $bondAtomNames[0])) {
				        $bondOrder1 = $bondOrder;
				    }
				    
				    if (($atom->{Name} eq $bondAtomNames[0] and $atom2->{Name} eq $bondAtomNames[1]) or
				        ($atom->{Name} eq $bondAtomNames[1] and $atom2->{Name} eq $bondAtomNames[0])) {
				        $bondOrder2 = $bondOrder;
				    }
				}
				my $xyz1 = $atom1->FractionalXYZ;
				my $xyz = $atom->FractionalXYZ;
		    	my $xyz2 = $atom2->FractionalXYZ;

			    my $x1 = sprintf("%.4f", $xyz1->X);
			    my $y1 = sprintf("%.4f", $xyz1->Y);
			    my $z1 = sprintf("%.4f", $xyz1->Z);
			    		    	
			    my $x = sprintf("%.4f", $xyz->X);
			    my $y = sprintf("%.4f", $xyz->Y);
			    my $z = sprintf("%.4f", $xyz->Z);
			    			    		    
			    my $x2 = sprintf("%.4f", $xyz2->X);
			    my $y2 = sprintf("%.4f", $xyz2->Y);
			    my $z2 = sprintf("%.4f", $xyz2->Z);
			    
				my $name1 = $atom1->Name;
				my $name = $atom->Name;
				my $name2 = $atom2->Name;
				my $monitor = $doc->CreateAngle([$atom1, $atom, $atom2]);
		    	my $angle = sprintf("%.4g", $monitor->Angle);
		    	$monitor->Delete;
		    	my $distance1 = Distance($atom1, $atom);
		    	my $distance2 = Distance($atom2, $atom);
				print $OUT "$name-Angle$order,Bond$bondOrder1($name1($x1;$y1;$z1);$distance1),$name($x;$y;$z),Bond$bondOrder2($name2($x2;$y2;$z2);$distance2),$angle\n";
				$order++;

		    }
		}
	}
}	

sub Distance(){
	my $xyz1 = $_[0];
	my $xyz2 = $_[1];
	
    my $x1 = $xyz1->X;
    my $y1 = $xyz1->Y;
    my $z1 = $xyz1->Z;
    		    	
    my $x2 = $xyz2->X;
    my $y2 = $xyz2->Y;
    my $z2 = $xyz2->Z;
        
    my $dx = $x2 - $x1;
    my $dy = $y2 - $y1;
    my $dz = $z2 - $z1;
    
    my $distance = sqrt($dx**2 + $dy**2 + $dz**2);
    $distance = sprintf("%.4g", $distance);
    return $distance;
}
