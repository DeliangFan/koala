----------- Price -----------
curl -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/prices -d '{"name": "sata_volume", "resource_type": "volume", "unit_price": 8888, "region": "bj"}'

curl -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/prices -d '{"name": "sata_volume", "resource_type": "volume_snapshot", "unit_price": 1.0, "region": "bj"}'

curl -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/prices -d '{"name": "router", "resource_type": "router", "unit_price": 0.888, "region": "bj"}'

curl -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/prices -d '{"name": "image01", "resource_type": "image", "unit_price": 1, "region": "bj"}'

curl -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/prices -d '{"name": "instance-snapshot", "resource_type": "instance_snapshot", "unit_price": 1, "region": "bj"}'

----------- Event ---------

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "123jj-daj-444444444", "resource_name": "volume01", "resource_type": "volume","event_type": "create", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:00:17.523000", "content": {"size": 50}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "123jj-daj-444444444", "resource_name": "volume01", "resource_type": "volume","event_type": "exists", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:40:17.523000", "content": {"size": 50}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "1111", "resource_name": "volumesnapshot01", "resource_type": "volume_snapshot","event_type": "resize", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:00:17.523000", "content": {"size": 1}}'

---------- Record -----------
curl 127.0.0.1:9999/v1/records/123jj-daj-444444444

---------- Router -----------
curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "22222222", "resource_name": "rt", "resource_type": "router","event_type": "create", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:00:17.523000", "content": {}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "22222222", "resource_name": "rt", "resource_type": "router","event_type": "exists", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T22:20:17.523000", "content": {}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "22222222", "resource_name": "rt", "resource_type": "router","event_type": "delete", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T23:00:17.523000", "content": {}}'

------------ Image ----------
curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "3", "resource_name": "image", "resource_type": "image","event_type": "upload", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:00:17.523000", "content": {"size": 10}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "3", "resource_name": "image", "resource_type": "image","event_type": "exists", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T23:00:17.523000", "content": {"size": 10}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "3", "resource_name": "image", "resource_type": "image","event_type": "delete", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-18T23:00:17.523000", "content": {"size": 10}}'

----------- Instance Snapshot -----------
curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "4", "resource_name": "instance-image", "resource_type": "instance_snapshot","event_type": "upload", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T21:00:17.523000", "content": {"size": 10}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "4", "resource_name": "instance-image", "resource_type": "instance_snapshot","event_type": "exists", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-08T23:00:17.523000", "content": {"size": 10}}'

curl   -X POST -H "Content-Type: application/json" 127.0.0.1:9999/v1/events -d '{"resource_id": "4", "resource_name": "instance-image", "resource_type": "instance_snapshot","event_type": "delete", "tenant_id": "8888", "region": "bj", "event_time": "2015-09-18T21:00:17.523000", "content": {"size": 10}}'


