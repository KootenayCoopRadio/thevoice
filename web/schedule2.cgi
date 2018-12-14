#!/usr/bin/perl

use lib '.';
require 'track_info.pm';
use CGI;
$q = new CGI ();

$date = $q->param('date');
$time = $q->param('time');
$tracknumbers = $q->param('tracknumbers');

@months = qw(Zero January February March April May June July August September October November December);
($mday, $year) = ($date =~ /^\D+(\d+)(?:,? +(\d+))?/);
($monthname) = ($date =~ /(\w{3,})/);
if (defined ($monthname)) {
    for(1..12) {
	if ($months[$_] =~ /^$monthname/i) {
	    $month = $_;
	}
    }
}
if (!defined($mday) || !defined($month)) {
    print $q->header;
    print "<HTML><BODY bgcolor=\"#ffffff\"><H3>Oops...</H3><P>Can't read your date.  Try something more like 'June 24'.</BODY></HTML>";
    exit;
}
if (!defined($year)) { $year = "+0"; }
($hour, $minute, $second, $ampm) = ($time =~ /^(\d+):(\d+)(?::(\d+))? *([ap]m)?/i);
if (!defined($minute)) {
    print $q->header;
    print "<HTML><BODY bgcolor=\"#ffffff\"><H3>Oops...</H3><P>Can't read your time ('$time').  Try something more like '4:20pm'.</BODY></HTML>";
    exit;
}
if (!defined($second)) {
    $second = 0;
}
if ($ampm =~ /p/ && $hour < 12) {
    $hour += 12;
}
print $q->header;

chomp($timestamp = `date -v${mday}d -v${month}m -v${year}y -v${hour}H -v${minute}M -v${second}S +%s`);

chomp($nice_date = `date -j -r $timestamp`);
@tracknumbers = split(/[^\dbim]+/, $tracknumbers);
$html_tracknumbers = join(",", @tracknumbers);

%program = ();
@program = ();
@program_seconds_after = ();
@program_track_time = ();
$tracklist = '';
$tracks = readlink "/etc/cart/cron/$_";
foreach (@tracknumbers) {
    $tracklist .= track_info($_);
}
$totaltime = 0;
foreach (@program_track_time) {
    my ($min, $sec) = /(\d*):(\d+)/;
    $totaltime += $min * 60 + $sec;
}

$nice_tracknumbers = $q->escapeHTML($tracklist);
$nice_tracknumbers .= sprintf("Total %4d:%02d", int($totaltime/60), int($totaltime)%60);

print <<EOF;
<HTML><HEAD><TITLE>Paddy schedule</TITLE></HEAD>
<BODY bgcolor="#ffffff">

<H3><A href="./">Paddy</A><BR><A href="schedule.cgi">schedule</A><BR>confirm</H3>

<P>Please confirm your reservation.

<FORM action="schedule3.cgi" method=post>
<INPUT type=hidden name=timestamp value=$timestamp>
<INPUT type=hidden name=tracknumbers value="$html_tracknumbers">
Date: <B>$nice_date</B>
<BLOCKQUOTE>
<PRE>$nice_tracknumbers</PRE>
</BLOCKQUOTE>
    If everything is OK, press this Confirm button.&nbsp;
<INPUT type=submit name="Confirm" value="Confirm"><BR>
</FORM>


</BODY>
EOF

1;
