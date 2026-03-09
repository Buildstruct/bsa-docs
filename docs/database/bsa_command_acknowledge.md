# bsa_command_acknowledge
Acknowledgements from servers for processed commands.

## Structure
```sql
CREATE TABLE `bsa_command_acknowledge` (
    `command_id` BIGINT UNSIGNED NOT NULL,
    `server_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`command_id`, `server_id`),

    CONSTRAINT fk_cmdack_command
        FOREIGN KEY (`command_id`) REFERENCES `bsa_command`(`command_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_cmdack_server
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- command_id - command being acknowledged.
- server_id - server acknowledging the command.

## Design Requirements
- Write acknowledgements with `INSERT IGNORE` so retries are idempotent.
- Acknowledge only after command effects are committed locally.
- Keep polling logic tolerant of duplicate deliveries until ACK is written.
