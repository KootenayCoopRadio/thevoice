#!/usr/bin/perl
# -*- indent-tabs-mode: t; -*-

use lib '.';
require 'track_info.pm';
use CGI;
$q = new CGI ();
print $q->header;

@months = qw(Zero January February March April May June July August September October November December);
@default = localtime(time+86400);
$defaultdate = $months[$default[4]+1] . " $default[3], " . ($default[5]+1900);
$defaulttime = sprintf ("%d:%02d", $default[2], $default[1]);
$defaulttime = "10:00";

$currentschedule = "";
opendir SCHED, "/etc/cart/cron/";
foreach (sort readdir SCHED) {
    if (-l "/etc/cart/cron/$_" && !/\D/ && $_ > time - 1800) {
	@program = ();
	@program_seconds_after = ();
	@program_track_time = ();
	@program_track = ();
	$tracklist = '';
	$tracks = readlink "/etc/cart/cron/$_";
	foreach (split(/[, ]+/, $tracks)) {
	    $tracklist .= track_info($_);
	}
	$totaltime = 0;
	foreach (@program_track_time) {
	    my ($min, $sec) = /(\d*):(\d+)/;
	    $totaltime += $min * 60 + $sec;
	}
	$currentschedule .= ("<P>Date: <B>" .
			     (scalar localtime $_) .
			     "</B><BLOCKQUOTE>Tracks:<B>\n" .
			     "<PRE>" .
			     $q->escapeHTML($tracklist) .
			     sprintf ("Total %4d:%02d", int($totaltime/60), int($totaltime)%60) .
			     "</PRE>" .
			     "</B>(Want to <A href=\"schedule-delete.cgi?timestamp=$_\">delete</A> this one?)</BLOCKQUOTE>\n");
    }
}
if ($currentschedule =~ /\S/) {
    $currentschedule =~ s/^/<P>Here is the current schedule:<P>/;
} else {
    $currentschedule = "<P>There is currently <B>nothing scheduled</B>.";
}

print <<EOF;
<HTML><HEAD><TITLE>Paddy schedule</TITLE></HEAD>
<BODY bgcolor="#ffffff">

<H3><A href="./">Paddy</A><BR>schedule</H3>

<P>You can program some tracks on Paddy, to play at a specific date
and time.

<BLOCKQUOTE>

<FORM action="schedule2.cgi" method=post>
Date: <INPUT type=text name=date value="$defaultdate"> (like "Feb 23"; default=tomorrow)<BR>
Time: <INPUT type=text name=time value="$defaulttime"> (like "2:30pm"; default=10am)<BR>
Track numbers: <INPUT type=text name=tracknumbers size=50><BR>(separate track numbers with spaces or commas or +)<BR>
<INPUT type=submit name="  OK  " value="  OK  ">
</FORM>

</BLOCKQUOTE>

<HR noshade>

$currentschedule

<HR noshade>

</BODY>
EOF

1;
