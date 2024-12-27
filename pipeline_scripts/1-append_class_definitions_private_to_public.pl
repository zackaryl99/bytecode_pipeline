# 2024 Zackary Savoie
# Appends class definiion to all files so that STUBBER can process them
# Also repalces private/protected with public in files
# Overwrites files in so doing, so create copy of originals in case you make a mistake

#!/usr/bin/perl
use strict;
use warnings;
use File::Find;

my ($directory) = @ARGV;

sub process_file {
    return unless /\.java$/;

    open my $in, '<', $_ or die "Could not open '$_' for reading: $!";
    my @lines = <$in>;
    close $in;

    unshift @lines, "public class HelloWorld {\n";
    push @lines, "}\n";

    # replace private and protected keywords in method signatures with public
    for my $line (@lines){
        if ($line =~ m/^\s*private.*\(.*\)\s*{/){
            $line =~ s/private/public/;
            print $line;
            next;
        }
        if ($line =~ m/^\s*protected.*\(.*\)\s*{/){
            $line =~ s/protected/public/;
            print $line;
            next;
        }
    }

    # Write the modified content back to the file
    open my $out, '>', $_ or die "Could not open '$_' for writing: $!";
    print $out @lines;
    close $out;

    print "Processed file: $_\n";
}

# Traverse directory and process each .java file
find(\&process_file, $directory);
