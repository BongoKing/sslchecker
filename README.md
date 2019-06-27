# sslchecker
Python Script to check the linked URLs of the BVH e.V. members


Instruction:

There are 3 different response options.

1. "OK" - There is a valide SSL Cert and everything works fine (status Code 200)
2. "SSL Inconsistency" - There is some problem / inconsistency with the site (not status code 200)
3. "Error / No SSL Cert found!" - the site is not available (there is no SSL Cert or there is some other problem)


Specifically, the third option may mean that the page is only accessible via a "www." URL. In future versions, I would like to query this case too.
