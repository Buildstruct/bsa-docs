# bsa_servers
A list of connected servers to the database that are discoverable.

!!! info
    This is an expandable table, you may add/remove columns here without issue.\
    Please keep `server_id`, `service_id`, `name`, `address`, `hidden`, `heartbeat_at` and `created_at` as is, these are required by BSA.\
    You may also foreign key this table as well if you don't plan on adding more columns.

## Structure
```sql
CREATE TABLE `bsa_servers` (
    `server_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `service_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `address` VARCHAR(46) NULL,
    `hidden` BIT NOT NULL DEFAULT 0,
    `temporary` BIT NOT NULL DEFAULT 0,
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
- hidden - if the server is to be hidden or obscured.
- temporary - if the server is to be removed for being unresponsive or offline.
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
- If a server is considered hidden it must not be visible to the public at all.
- If a server is considered temporary it must be removed upon being marked offline.