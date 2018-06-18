package Cpanel::API::Cpnginx;
use strict;
our $VERSION = '10.0';
use Cpanel                   ();
use Cpanel::API              ();
use Cpanel::Locale           ();
use Cpanel::Logger           ();
my $logger;
my $locale;

sub rebuildvhost {

    my ( $args, $result ) = @_;
    my ( $domain ) = $args->get( 'domain' );
    my $feature = 'cpnginix_home'; 
    if ( !main::hasfeature($feature) ) {                    
        $result->error( '_ERROR_FEATURE', $feature );
        return;
    }
    if ( $Cpanel::CPDATA{'DEMO'} ) {
        $result->error( '_ERROR_DEMO_MODE', $feature );
        return;
    }

    my $success=1;
    if ($success) {
        $result->data($domain);
        return 1;
    }
    else {
        return 0;
    }

}

1;
