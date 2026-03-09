# bsa_servers
A list of connected servers to the database that are discoverable.

## Structure
```sql
CREATE TABLE `bsa_servers` (
    `server_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `service_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `address` VARCHAR(46) NULL,
    `heartbeat_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_server_services
        FOREIGN KEY (`service_id`) REFERENCES `bsa_services`(`service_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    INDEX idx_heartbeat (heartbeat_at)
);
```

- server_id - unique id of the server.
- service_id - service this server belongs to.
- name - unique server name, such as `BS-GMOD-1` or `BS-GMOD-DEV`.
- address - optional IP/host address; null often means static/system service.
- heartbeat_at - timestamp for the last heartbeat received from the server.
- created_at - timestamp for when the server was created.

## Restrictions
Baseline seed row uses `server_id = 1` with name `SYSTEM`.
No trigger currently locks this row, so treat it as reserved operationally.

## Design Requirements
- Each live platform must regularly update its own row so `heartbeat_at` stays fresh.
- Consider servers stale when heartbeat is older than 60 seconds.
- Use stable, unique server names; do not recycle names across active nodes.
- Command fanout logic should target only alive servers.
