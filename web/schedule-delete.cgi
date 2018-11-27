#!/usr/bin/perl

use CGI;
$q = new CGI ();

$timestamp = int(0 + $q->param('timestamp'));
unlink "/etc/cart/cron/$timestamp";

print $q->redirect("http://$ENV{'SERVER_NAME'}/cart/schedule.cgi");

