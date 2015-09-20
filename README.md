# koala
Koala is a billing system for openstack driven by ceilometer event.

Koala only interacts with ceilometer by Rest API. Once Ceilometer receive a notification from message bus, it will
send the event converted from notification to Koala. With the event, koala caculates the consumption and generates
the billing records.

Koala is designed as distribute system with following characteristics.
1. High-resolution timing as second level precision
2. Supports to multi-regions
3. High efficient driven by events
4. Decoupling from openstack
5. Distribute with stateless service
