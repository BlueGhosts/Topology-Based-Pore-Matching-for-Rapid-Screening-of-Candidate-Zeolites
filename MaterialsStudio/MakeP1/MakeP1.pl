#!perl

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);

# my $import_dirname = "D:/Work/Data/PCOD_2.1/PCOD_2.1"; 
# my $export_dirname = "D:/Work/Data/PCOD_2.1/MS-FindSym-PCOD_2.1";

my ($import_dirname, $export_dirname) = @ARGV;
opendir(my $dir, $import_dirname) or die "Error in opening dir '$import_dirname': $!";

while (my $file = readdir($dir)) {
    if ($file =~ /\.cif$/i) {
        print "$file\n";  
        my $filename = $file;
        $filename =~ s|.*/||;  
        
    	my $doc = Documents->Import("$import_dirname/$file");

        $doc->MakeP1;

        $doc -> Export("$export_dirname/$filename");
        $doc -> discard;   
    }
}
closedir($dir);