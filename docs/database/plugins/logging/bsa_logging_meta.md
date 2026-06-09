# bsa_logging_meta
Stores key-value metadata pairs attached to log entries, used for searchable context such as invoker names, identifiers, and player IDs.

## Structure
```sql
CREATE TABLE `bsa_logging_meta` (
    `log_meta_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `log_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `value` TEXT NOT NULL,

    INDEX `idx_logging_meta_lookup` (`log_id`, `name`),

    CONSTRAINT `fk_logging_meta_logs`
        FOREIGN KEY (`log_id`) REFERENCES `bsa_logging`(`log_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- log_meta_id - unique id of the metadata row.
- log_id - references the owning `bsa_logging` entry.
- name - the metadata key (e.g. `invoker_name`, `invoker_identifier`, `invoker_player_id`).
- value - the metadata value for this key.

## Notes
Multiple meta rows per log entry are expected.\
The `idx_logging_meta_lookup` index supports fast retrieval of all metadata for a given log entry.

Full-text search over `value` is performed with a `LIKE '%term%'` query inside a joined subquery on `bsa_logging`.\
This is an O(n) scan; retention policies on `bsa_logging` are relied upon to bound the row count.

## Design Requirements
- Insert meta rows in the same bulk operation as the parent `bsa_logging` row.
- Use consistent, well-known `name` keys across log types to keep cross-type searches reliable.
- Rely on cascade delete from `bsa_logging` to remove meta rows; do not delete them independently.
