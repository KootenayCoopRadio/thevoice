#!/usr/bin/perl

use CGI;
$q = new CGI ();
print $q->header(-Location=>"schedule.cgi");
