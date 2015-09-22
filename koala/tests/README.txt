curl -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/prices -d '{"name": "sata_volume", "resource_type": "volume", "unit_price": 8888, "region": "bj"}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "123jj-daj-444444444", "resource_name": "volume01", "resource_type": "volume","event_type": "create", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:00:17.523000", "content": {"size": 50}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "123jj-daj-444444444", "resource_name": "volume01", "resource_type": "volume","event_type": "exists", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:40:17.523000", "content": {"size": 50}}'

curl 127.0.0.1:9999/v1/records/123jj-daj-444444444
