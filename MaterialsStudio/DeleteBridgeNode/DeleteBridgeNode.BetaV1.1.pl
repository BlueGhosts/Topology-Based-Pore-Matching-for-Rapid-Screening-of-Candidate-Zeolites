#!perl
# Beta V1.1 by wangjiaze in 2025-02-26 

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);


#my $import_dirname = ""; 
#my $export_dirname = "";

my ($import_dirname, $export_dirname, $outfilepath) = @ARGV;
$outfilepath = "$outfilepath.csv";

opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
open(my $OUT, '>', $outfilepath) or die "Error to open $outfilepath $!";

print "filename,beforeAtomNumber,afterAtomNumber,Deleted\n";
print $OUT "filename,beforeAtomNumber,afterAtomNumber,Deleted\n";

BatchCalculate($import_dirname, $export_dirname);

#my $doc = $Documents{"IN.xsd"};
#DeleteDocBrigeNode($doc, 'Lr', 179);
#DeleteDocBrigeNode($doc, 'Lr', 179);
#ProtectStraightPore($doc, 'Lr', 'Yb');

sub BatchCalculate(){
	my $import_dirname = $_[0];
	my $export_dirname = $_[1];

	opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
	while (my $file = readdir($dir)) {
	    if ($file =~ /\.cif$/i) {
	        #print "$file\n";  
	        my $filename = $file;
	        $filename =~ s|.*/||;  
	    	my $doc = Documents->Import("$import_dirname/$file");
            
	    	my $atoms = $doc->AsymmetricUnit->Atoms;
	    	my $beforeAtomNumber = @$atoms;
	    	#$doc->MakeP1;
			DeleteDocBrigeNode($doc, 'Lr', 179);
			#$doc->FindSymmetry;
            my $atoms = $doc->AsymmetricUnit->Atoms;
            my $afterAtomNumber = @$atoms;
            
            my $deletedFlag;
            if ($beforeAtomNumber == $afterAtomNumber){
                    $deletedFlag = 0;
                }
                else{
                    $deletedFlag = 1;
                }
            print "$filename,$beforeAtomNumber,$afterAtomNumber,$deletedFlag\n";
			print $OUT "$filename,$beforeAtomNumber,$afterAtomNumber,$deletedFlag\n";
            
	        $doc -> Export("$export_dirname/$filename");
	        $doc -> discard;   
	    }
	}
	closedir($dir);
    close($OUT);
}

sub DeleteDocBrigeNode(){
	my $doc = $_[0];
	my $poreElement = $_[1];
	my $thresholds = $_[2];
	
	
	my $protectedElement = 'Yb';
	ProtectStraightPore($doc, $poreElement, $protectedElement);
	
    my $atoms = $doc->UnitCell->Atoms;
	my $flag = 1;
	
	while ($flag == 1){
		$flag = 0;
		$flag = DeleteBrigeNode($doc, 'Lr', $thresholds);
		DeleteElement($doc, 'No');
		
	}
    foreach my $atom (@$atoms) {
    	if ( $atom -> ElementSymbol eq $protectedElement){
    		$atom -> ElementSymbol = $poreElement;
    	}	
    }
}

sub DeleteBrigeNode(){
	my $doc = $_[0];
	my $poreElement = $_[1];
	my $thresholds = $_[2];
	
	#my $atoms = $fragment->Atoms;

	my $atoms = $doc->UnitCell->Atoms;
	my $flag = 0;
	foreach my $atom (@$atoms) {
	    my $element = $atom->ElementSymbol;
	    my $numBonds = $atom -> NumBonds;
	    if ( $element eq $poreElement and $numBonds == 2){
	    	# print($numBonds);
	    	
	    	my $connectedAtoms = $atom->AttachedAtoms;
	    	
	    	my $atom1 = @$connectedAtoms[0];
	    	my $atom2 = @$connectedAtoms[1];
	
	    	#print("Atom:", $atom->Name,"\n");
	    	my $monitor = $doc->CreateAngle([$atom1, $atom, $atom2]);
	    	my $angle = $monitor->Angle;
	    	$monitor->Delete;
			if ( $angle >= $thresholds ){	
			
				my $leftAtom = $atom1;
				my $rightAtom = $atom2;
				my $centerAtom = $atom;
	
				#print($centerAtom->Name,"\n");
				
				while ($leftAtom->NumBonds==2){
					my $leftConnectedAtoms = $leftAtom->AttachedAtoms;
					if (@$leftConnectedAtoms[0]->Name eq $centerAtom->Name){
						$leftAtom = @$leftConnectedAtoms[1];
						$centerAtom = @$leftConnectedAtoms[0];
					}
					else{ 
						$leftAtom = @$leftConnectedAtoms[0]; 
						$centerAtom = @$leftConnectedAtoms[1];
					}
				}	
				$flag = 1;
		    	#$doc->CreateBond($atom1, $atom2, "Single");
		    	$doc->CreateBond($leftAtom, $rightAtom, "Single");
		    	$atom->ElementSymbol = "No";
		    	#$atom->Delete;
			}	
		}
	}
	return $flag;		
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
	my $atoms = $doc->UnitCell->Atoms;
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