#!perl

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);

my ($import_dirname, $outfilepath) = @ARGV;
$outfilepath = "$outfilepath.csv";
# $import_dirname = "P:/Project/PoreTopology/01_IZA/02_Process/03_PoreTopology/02_Cif/Test"; 
# $outfilepath = "P:/Project/PoreTopology/01_IZA/02_Process/03_PoreTopology/02_Cif/Test.csv"; 

opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";
open(my $OUT, '>', $outfilepath) or die "Error to open $outfilepath $!";

print "filename,ZANumber,nodesNumber,atom_mul,atom_connection\n";
print $OUT "filename,ZANumber,nodesNumber,atom_mul,atom_connection\n";

while (my $file = readdir($dir)) {
    if ($file =~ /\.cif$/i) {
        #print "$file\n";  
        my $filename = $file;
        $filename =~ s|.*/||;  
        $filename =~ /^([^.]*)/;
        my $filename = $1;
        
        my $doc = Documents->Import("$import_dirname/$file");
        my ($ZANumber, $nodeNumber) = CalculateNode($doc, "Lr");
        my ($atom_mul, $atom_connection) = CalculateConnection($doc, "Lr");
        
        # my ($ZANumber, $nodeNumber) = CalculateNode($doc, "Si");
        # my ($atom_mul, $atom_connection) = CalculateConnection($doc, "Si");
        
        $doc->discard;   

        my $atom_mul_str = join(";", map { "$_:$atom_mul->{$_}" } keys %$atom_mul);
        my $atom_connection_str = join(";", map { "$_:$atom_connection->{$_}" } keys %$atom_connection);
        
        print "$filename,$ZANumber,$nodeNumber,{$atom_mul_str},{$atom_connection_str}\n";
        print $OUT "$filename,$ZANumber,$nodeNumber,{$atom_mul_str},{$atom_connection_str}\n";
    }
}
closedir($dir);
close($OUT);

sub CalculateConnection {
    my $doc = $_[0];
    
    my %atom_connection;
    my %atom_mul;
    
    my $atoms = $doc->AsymmetricUnit->Atoms;
    foreach my $atom (@$atoms) {
        my $name = $atom->Name;
        my $element = $atom->ElementSymbol;
        if (@_[1]) {
            if ($element ne @_[1]) {
                next;
            }    
        } 
        my $mul = $atom->SymmetryMultiplicity;
        my $atomConnection = $atom->NumBonds;
        if (not exists $atom_connection{$name}) {
            $atom_connection{$name} = 0;
            $atom_mul{$name} = 0;
        } 
        $atom_connection{$name} = $atomConnection;
        $atom_mul{$name} = $mul;
    }
    return (\%atom_mul, \%atom_connection);
}

sub CalculateNode {
    my $doc = $_[0];
    my $ZANumber = 0;
    my $nodeNumber = 0;
    
    my $atoms = $doc->AsymmetricUnit->Atoms;
    foreach my $atom (@$atoms) {
        my $element = $atom->ElementSymbol;
        if (@_[1]) {
            if ($element ne @_[1]) {
                next;
            }
        }
        my $atomConnection = $atom->NumBonds;   
        if ($atomConnection != 0){
        	$nodeNumber++;
        }
        $ZANumber++; 
    } 
    return ($ZANumber, $nodeNumber);     
}