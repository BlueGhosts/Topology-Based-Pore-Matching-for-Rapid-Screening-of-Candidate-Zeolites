#!perl

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);

my ($import_dirname, $outfilepath) = @ARGV;
$outfilepath = "$outfilepath.csv";

opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
open(my $OUT, '>', $outfilepath) or die "Error to open $outfilepath $!";

print "filename,MinZAAngle\n";
print $OUT "filename,MinZAAngle\n";

BatchCalculate($import_dirname);


sub BatchCalculate(){
	my $import_dirname = $_[0];

	opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
	while (my $file = readdir($dir)) {
	    if ($file =~ /\.cif$/i) {
	        print "$file\n";  
	        my $filename = $file;
	        $filename =~ s|.*/||;  
	        
	    	my $doc = Documents->Import("$import_dirname/$file");
	    	
			my $minAngle = CalculateMinZAAngle($doc, 'Lr');
            if ($minAngle != 361){
                printf "$filename,$minAngle\n";
                printf $OUT "$filename,%.4f\n", $minAngle;
            }
            else{
                print "$filename,NA\n";
                print $OUT "$filename,NA\n";
            }

	        $doc -> discard;   
	    }
	}
	closedir($dir);
}

sub CalculateMinZAAngle(){
	my $doc = $_[0];
	my $poreElement = $_[1];

	my $minAngle = 361;
	my $atoms = $doc->UnitCell->Atoms;
	foreach my $atom (@$atoms) {
	    my $element = $atom->ElementSymbol;
	    my $numBonds = $atom -> NumBonds;
	    if ( $element eq $poreElement and $numBonds >= 2){
	    	my $connectedAtoms = $atom->AttachedAtoms;
	    	
	    	my $atom1 = @$connectedAtoms[0];
	    	my $atom2 = @$connectedAtoms[1];
	
	    	my $name1 = $atom1->Name;
	    	my $name2 = $atom2->Name;
	    	
	    	my $monitor = $doc->CreateAngle([$atom1, $atom, $atom2]);
	    	my $angle = $monitor->Angle;
	    	$monitor->Delete;
			if ( $angle < $minAngle ){	
		    	$minAngle = $angle;
			}	
		}
	}		
	return $minAngle;
}	