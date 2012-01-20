======
Cirrus
======

dns_setup reads a simple yaml file that only defines credentials, 
domains and bind style zone files used to define the domains.

Amazon Alias entries are treated as a TXT dns type with _alias added to 
the domain name and the value starting with 'Alias '. This is to work 
around the dnspython library does not allowing invalid dns types. An 
example alias in a zone file, (replace hosted_zone_id and dns_name):
$TTL      600 ; 10 minutes - Alias entries always have a ttl of 600
_alias                  IN     TXT "Alias hosted_zone_id dns_name."

update_host.py will update a single host entry in an route 53 domain. It 
relies on environment variables and command line arguments rather than 
yaml. I use it to accomplish dynamic dns for ec2 with the simple init 
script found in contrib. Since this will potentially be on many many 
machines for security I suggest you use a dns subdomain and different 
AWS credentials with this script.

