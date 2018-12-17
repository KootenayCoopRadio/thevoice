#!/usr/bin/perl
# -*- indent-tabs-mode: t; -*-

$ETC = $ENV{'ETC'} || '/etc';
@PLAYBOXES = grep (/\S/, split (/\n/, `cat $ETC/cart/playboxes`));
chomp($MPG123 = $ENV{'MPG123'} || `which mpg123` || '/usr/local/bin/mpg123');

if (!%tracks) {
    %tracks = ();
    my $playbox_dir, $playbox;
    foreach $playbox (@PLAYBOXES) {
	my ($playbox_dir, $prefix) = split (/=/, $playbox, 2);
	opendir PLAYBOX, $playbox_dir;
	while (defined ($_ = readdir PLAYBOX)) {
	    next unless /^(\d+)/;
	    $tracks{"${prefix}${1}"} ||= [];
	    push @{$tracks{"${prefix}${1}"}}, "$playbox_dir/$_";
	}
	closedir PLAYBOX;
    }
}

sub track_info {
    my $track = shift @_;
    my ($tracknumber, $inode) = $track =~ /^(\d+)(?:i(\d+))?/;
    my @matches = @{$tracks{$tracknumber}};
    if (@matches > 1 && $inode > 0) {
	my @best;
	for my $fnm (@matches) {
	    my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,
		$atime,$mtime,$ctime,$blksize,$blocks)
		= stat($fnm);
	    if ($ino == $inode) {
		push @best, $fnm;
	    }
	}
	if (@best > 0) {
	    @matches = @best;
	}
    }
    if (!@matches) {
	return "[track $tracknumber doesn't exist; i'll ignore that]\n";
    }
    else {
	my $which_rand = int(rand(1+$#matches));
	if (exists($last_rand{$tracknumber})
	    && $last_rand{$tracknumber} == $which_rand) {
	    $which_rand = ($which_rand + 1) % @matches;
	}
	$last_rand{$tracknumber} = $which_rand;
	my $selected_file = $matches[$which_rand];

	if (!$inode) {
	    my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,
		$atime,$mtime,$ctime,$blksize,$blocks)
		= stat($selected_file);
	    $inode = $ino;
	    $track = "${tracknumber}i${inode}";
	}

	local $/ = undef;
	my $time = $selected_file =~ /\.mp3$/i ? `$MPG123 -t -v -n 100 "$selected_file" 2>&1` : '';
	if ($time =~ /.*[\[\+](?:(\d+):)?(\d+):(\d+)(?:\.(\d+))?[\]\s]/) {
	    $m = $1*60 + $2;
	    $s = $3 + $4/100;
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
	push @program_track, $track;

	$selected_file =~ s,.*/\d+\s*,,;
	$selected_file =~ s,\.(\w+)$,,;
	return sprintf "%-6s%7s   %-55.55s\n", $tracknumber, $time, $selected_file;
    }
}

1;
