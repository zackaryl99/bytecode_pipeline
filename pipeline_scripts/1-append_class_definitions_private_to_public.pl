# Appends class definiion to all files so that STUBBER can process them
# Also repalces private/protected with public in files
# Overwrites files in so doing

#!/usr/bin/perl
use strict;
use warnings;
use File::Find;

# Get the directory and the string to insert
my ($directory) = @ARGV;

# Function to process each file
sub process_file {
    # Only process .java files
    return unless /\.java$/;

    # Read the file content
    open my $in, '<', $_ or die "Could not open '$_' for reading: $!";
    my @lines = <$in>;
    close $in;

    # Add the insert_string at the beginning and end
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

# Traverse the directory and process each .java file
find(\&process_file, $directory);
