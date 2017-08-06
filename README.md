# Hydra Proxy

TDS Protocol Proxy

# Event
## Input Event
size unit : byte
```json
{
	"stamp": "20170802140000",
	"user": "user1",
	"database": "EHISQL",
	"client_ip": "10.16.82.135",
	"event": "input",
	"size": 1245712 
}
```

## Output Event
size unit : byte

```json
{
	"stamp": "20170802140000",
	"user": "user1",
	"database": "EHISQL",
	"client_ip": "10.16.82.135",
	"event": "output",
	"size": 1245712 // unit Byte
}
```

## Login

```json
{
	"stamp": "20170802140000",
	"user": "user1",
	"database": "EHISQL",
	"client_ip": "10.16.82.135",
	"event": "login"
}
```

## Logout

```json
{
	"stamp": "20170802140000",
	"user": "user1",
	"database": "EHISQL",
	"client_ip": "10.16.82.135",
	"event": "logout"
}
```

## Batch
### execute sql
elapse unit ms

show error message if some exception occur

```json
{
	"stamp": "20170802140000",
	"user": "user1",
	"database": "EHISQL",
	"client_ip": "10.16.82.135",
	"event": "batch",
	"text": "SELECT * FROM User LIMIT 10;",
	"elapse": 120,
	"error": "Unknown Databases"
}
```