# bsa_command_expected
Expected acknowledgements for each command and target server.\
Rows are created at command send time to define required recipients.

## Structure
```sql
CREATE TABLE `bsa_command_expected` (
    `command_id` BIGINT UNSIGNED NOT NULL,
    `server_id`  BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`command_id`, `server_id`),

    CONSTRAINT fk_cmdexp_command
        FOREIGN KEY (`command_id`) REFERENCES `bsa_command`(`command_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE,

    CONSTRAINT fk_cmdexp_server
        FOREIGN KEY (`server_id`) REFERENCES `bsa_servers`(`server_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- command_id - command id that expects acknowledgement.
- server_id - target server expected to acknowledge the command.

## Design Requirements
- Platform code should not write this table directly; use command send procedures.
- Expected rows should only include alive targets (`heartbeat_at` within 60 seconds) and exclude origin server.
- Command completion should be derived from `expected` minus `acknowledge`.
