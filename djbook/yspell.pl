use strict;
use warnings;

use Getopt::Long;
use LWP::UserAgent;

my $URL = "http://speller.yandex.net/services/yspell";
my $options = 4; # IGNORE_URLS
my @lang = ();
my $encoding = "utf-8";
my ($a, $mode, $H, $sgml) = (1, "", 0, "");

sub main();

GetOptions(
    "a" => \$a, "lang=s" => \@lang, "mode=s" => \$mode, "H" => \$H,
    "rem-sgml-check=s" => \$sgml,
    "encoding=s" => \$encoding)
    or exit(1);

main();

sub main() {
    $mode = "html" if $H;

    my $url = $URL;
    $url .= "?options=$options";
    $url .= "&lang=" . join(",", @lang);
    $url .= "&mode=" . $mode;

    my $text = "";
    $text .= $_ while <>;
    
    my $ua = new LWP::UserAgent;
    my $request = new HTTP::Request("POST", $url);
    $request->header("Content-Type" => "text/plain; charset=$encoding");
    $request->content($text);
    my $response = $ua->request($request);

    if ($response->code != 200) {
        print STDERR "yspell.pl: $URL: " . $response->content . "\n";
        exit(1);
    }
    
    print $response->content;
}
