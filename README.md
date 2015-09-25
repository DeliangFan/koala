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

# API
Koala provides several kinds api for billing and rating.
## Price
Price APIs enable to manage the price of resource, you can create, update or delete the price.
/v1/prices

    {
        "description": null,
        "id": 2,
        "name": "ram",
        "region": "bj",
        "resource_type": "ram",
        "unit_price": 0.0001
    }

## Resource
Resource APIs enbale user to get the consumption information of the resource.
/v1/resources

    {
        "consumption": 1382.5777777777776,
        "created_at": "2015-09-25T07:54:38.235522",
        "deleted": 1,
        "deleted_at": "2015-09-25T07:55:34.465942",
        "description": "Resource has been deleted",
        "region": "bj",
        "resource_id": "ca9ef7fe-889d-462e-91e4-f05a60abc739",
        "resource_name": "lg",
        "resource_type": "volume",
        "status": "delete",
        "tenant_id": "33294fe9cd6c4150b43b38cd92ea17c5",
        "updated_at": null
    }

## Record
Record API enable user to get the billing records of a resource.
/v1/records/{resource_id}

    [
        {
            "consumption": 0.0022200000000000002,
            "description": "Resource has been deleted",
            "end_at": "2015-09-25T08:01:48.629053",
            "resource_id": "723566f3-db38-4e37-bdc7-fb0d33856468",
            "start_at": "2015-09-25T08:01:39.504316",
            "unit_price": 0.88800000000000001
        }
    ]

## Event
Event API is used for ceilometer notification recieve event messages and generates the billing records.

    {
        "region": "bj",
        "resource_id": "ca9ef7fe-889d-462e-91e4-f05a60abc739",
        "resource_name": "lg",
        "resource_type": "volume",
        "tenant_id": "33294fe9cd6c4150b43b38cd92ea17c5",
        "event_type": "create",
        "event_time": "2015-09-25T07:54:38.235522"
        "content": {"size": 100}
    }

# Development
Any contributions will be appreciate.
