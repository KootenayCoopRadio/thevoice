#!/usr/bin/perl

$ETC = $ENV{'ETC'} || '/etc';
@PLAYBOXES = grep (/\S/, split (/\n/, `cat $ETC/cart/playboxes`));
$MPG123 = $ENV{'MPG123'} || '/usr/local/bin/mpg123';

sub track_info {
    my $tracknumber = shift @_;
    my @matches;
    my $playbox_dir, $playbox;
    foreach $playbox (@PLAYBOXES) {
	my ($playbox_dir, $prefix) = split (/=/, $playbox, 2);
	opendir PLAYBOX, $playbox_dir;
	while (defined ($_ = readdir PLAYBOX)) {
	    next unless /^\d/;
	    my $filename = "$playbox_dir/$_";
	    s/^/$prefix/;
	    next unless /^$tracknumber\D/ && /\.(mp3|wav)$/i;
	    push @matches, $filename;
	}
	closedir PLAYBOX;
    }
    if (!@matches) {
	return "[track $tracknumber doesn't exist; i'll ignore that]\n";
    }
    elsif (0 && exists $program{$tracknumber}) {
	return "[you already programmed track $tracknumber; i'll ignore that]\n";
    }
    else {
	my $which_rand = int(rand(1+$#matches));
	if (exists($last_rand{$tracknumber})
	    && $last_rand{$tracknumber} == $which_rand) {
	    $which_rand = ($which_rand + 1) % @matches;
	}
	$last_rand{$tracknumber} = $which_rand;
	my $selected_file = $matches[$which_rand];

	local $/ = undef;
	my $time = $selected_file =~ /\.mp3$/i ? `$MPG123 -t -qvv -n 100 "$selected_file" 2>&1` : '';
	if ($time =~ /.*\[((\d+):)?(\d+):(\d+)(\.(\d+))?\]/) {
	    $m = $1*60 + $3;
	    $s = $4 + $6/100;
	    $time = sprintf ("%d:%02d", $m, $s);
	    for $i (0..$#program_seconds_after) {
		next if $program_seconds_after[$i] < 0;
		$program_seconds_after[$i] += $m * 60 + $s;
	    }
	} else {
	    $time = "";
	    for $i (0..$#program_seconds_after) {
		$program_seconds_after[$i] = -1;
	    }
	}
	push @program_seconds_after, 0;
	push @program_track_time, $time;
	push @program, $selected_file;
	push @tracknumber, $tracknumber;
	$program{$tracknumber} = 1;

	$selected_file =~ s,.*/\d+\s*,,;
	$selected_file =~ s,\.(\w+)$,,;
	return sprintf "%-6s%7s   %-55.55s\n", $tracknumber, $time, $selected_file;
    }
}

1;
