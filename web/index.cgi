#!/usr/bin/perl

use CGI;
$q = new CGI ();
print $q->header(-Location=>"http://$ENV{'HTTP_HOST'}/cart/schedule.cgi");
