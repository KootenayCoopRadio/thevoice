#!/usr/bin/perl

use CGI;
$q = new CGI ();

$timestamp = $q->param('timestamp');
$tracknumbers = $q->param('tracknumbers');

symlink $tracknumbers, "/etc/cart/cron/$timestamp";

print $q->redirect("schedule.cgi");

1;
