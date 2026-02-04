#!perl

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);


my $import_dirname = ""; 
my $export_dirname = "";

my ($import_dirname, $export_dirname) = @ARGV;
BatchCalculate($import_dirname, $export_dirname);

#my $doc = $Documents{"IN.xsd"};
#DeleteDocBrigeNode($doc, 'Lr', 179);
#ProtectStraightPore($doc, 'Lr', 'Yb');

sub BatchCalculate(){
	$import_dirname = $_[0];
	$export_dirname = $_[1];

	opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
	while (my $file = readdir($dir)) {
	    if ($file =~ /\.cif$/i) {
	        print "$file\n";  
	        my $filename = $file;
	        $filename =~ s|.*/||;  
	        
	    	my $doc = Documents->Import("$import_dirname/$file");
	    	
			DeleteDocBrigeNode($doc, 'Lr', 179);
	
	        $doc -> Export("$export_dirname/$filename");
	        $doc -> discard;   
	    }
	}
	closedir($dir);
}

sub DeleteDocBrigeNode(){
	my $doc = $_[0];
	my $poreElement = $_[1];
	my $thresholds = $_[2];
	
	#$doc->MakeP1;
	my $protectedElement = 'Yb';
	ProtectStraightPore($doc, $poreElement, $protectedElement);
	
    my $atoms = $doc->UnitCell->Atoms;
	my $flag = 1;
	
	while ($flag == 1){
		$flag = 0;
		DeleteBrigeNode($doc, 'Lr', $thresholds);
		DeleteElement($doc, 'No');
		foreach my $atom (@$atoms) {
		    my $element = $atom->ElementSymbol;
		    my $numBonds = $atom -> NumBonds;
		    if ( $element eq $poreElement and $numBonds == 2){

			 	my $connectedAtoms = $atom->AttachedAtoms;
		    	
		    	my $atom1 = @$connectedAtoms[0];
		    	my $atom2 = @$connectedAtoms[1];
		    	my $monitor = $doc->CreateAngle([$atom1, $atom, $atom2]);
		    	my $angle = $monitor->Angle;
		    	$monitor->Delete;
				if ( $angle >= $thresholds ){			
			    	$flag = 1;
			    	last;
				}
		    }
		    
		}
	}
    foreach my $atom (@$atoms) {
    	if ( $atom -> ElementSymbol eq $protectedElement){
    		$atom -> ElementSymbol = $poreElement;
    	}	
    }
    #$doc->FindSymmetry;
}

sub DeleteBrigeNode(){
	my $doc = $_[0];
	my $poreElement = $_[1];
	my $thresholds = $_[2];
	
	#my $atoms = $fragment->Atoms;
	
	my $atoms = $doc->UnitCell->Atoms;
	foreach my $atom (@$atoms) {
	    my $element = $atom->ElementSymbol;
	    my $numBonds = $atom -> NumBonds;
	    if ( $element eq $poreElement and $numBonds == 2){
	    	#print($numBonds);
	    	my $connectedAtoms = $atom->AttachedAtoms;
	    	
	    	my $atom1 = @$connectedAtoms[0];
	    	my $atom2 = @$connectedAtoms[1];
	
	    	my $name1 = $atom1->Name;
	    	my $name2 = $atom2->Name;
	    	
	    	# print("$name1, $name2\n");
	    	my $monitor = $doc->CreateAngle([$atom1, $atom, $atom2]);
	    	my $angle = $monitor->Angle;
	    	$monitor->Delete;
			if ( $angle >= $thresholds ){			
		    	$doc->CreateBond($atom1, $atom2, "Single");
		    	$atom->ElementSymbol = "No";
			}

		}
	}
}

sub DeleteElement(){
	my $doc = $_[0];
	my $poreElement = $_[1];

	my @deleteAtoms;
	my $atoms = $doc->UnitCell->Atoms;
	foreach my $atom (@$atoms) {
	    if ($atom->ElementSymbol eq $poreElement) {
	    	push @deleteAtoms, $atom;
	    }
	}
	
	foreach my $atom (@deleteAtoms) {
		eval {
		    my $name = $atom->name;
		    #print($name);
		    $atom->Delete;
		}
	}
}


sub ProtectStraightPore(){
	my $doc = $_[0];
	my $poreElement = $_[1];
	my $protectedElement = $_[2];
	
	#my $atoms = $doc->UnitCell->Atoms;
	
	#my $doc = $Documents{"IN.xsd"};
	my $atoms = $doc->AsymmetricUnit->Atoms;
	my $flag;
	foreach my $atom (@$atoms) {
		if ($atom->ElementSymbol ne $poreElement){
			next;
		}
		
	    my @fragment = GetUnitFragment($atom);
	    $flag = 1;
	    foreach my $fragmentAtom (@fragment){
	    	#print($fragmentAtom->Name,"  ", $fragmentAtom->Name)
	    	if ($fragmentAtom -> NumBonds != 2){
	    		$flag = 0;
	    	}
	    }
	    if ( $flag == 1 ){
	    	foreach my $fragmentAtom (@fragment){
	    		$fragmentAtom -> ElementSymbol = $protectedElement;
	    	}
	    }   
	}
	
}


sub GetUnitFragment(){
	my $atom = $_[0];
	
	my @fragmentAtoms;
	my @fragmentAtomNames;
	
	push @fragmentAtoms, $atom;
	push @fragmentAtomNames, $atom->Name;

	my $flag = 1;
	while ($flag == 1){
		$flag = 0;
		foreach my $fragmentAtom (@fragmentAtoms){
			my $connectedAtoms = $fragmentAtom->AttachedAtoms;
			foreach my $connectedAtom (@$connectedAtoms) {
				#print("connectedAtom: ",$connectedAtom->Name, "\n");
				my $connectedAtomName = $connectedAtom -> Name;
			    if ( !grep { $_ eq $connectedAtomName } @fragmentAtomNames) {	
			    	push @fragmentAtoms, $connectedAtom;
					push @fragmentAtomNames, $connectedAtom->Name;
			    	$flag = 1;
			    }
			}		
		}
	}
	return @fragmentAtoms;
}