# Overview
Koala is a billing system for openstack driven by ceilometer event.

Koala only interacts with ceilometer by Rest API. Once Ceilometer receive a notification from message bus, it will
send the event converted from notification to Koala. With the event, koala caculates the consumption and generates
the billing records.

Koala is designed as distribute system with following characteristics.
>* High-resolution timing as second level precision
>* Supports to multi-regions
>* High efficient driven by events
>* Decoupling from openstack
>* Distribute with stateless service

#Architecture
##koala-api
The koala-api provide rest APIs for ceilometer and users, the event API is used to recieve events from ceilometer and the others are designed to privde for query billing records.

# Development
Any contributions will be appreciate.
