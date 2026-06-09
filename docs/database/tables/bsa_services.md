# bsa_services
Services represent application domains hosted under providers (`gmod`, `discord`, `website`, etc).

## Structure
```sql
CREATE TABLE `bsa_services` (
    `service_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `provider_id` BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `alias` TINYTEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_service_providers
        FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);
```

- service_id - unique id of the service.
- provider_id - provider this service belongs to.
- name - unique service key, such as `gmod`.
- alias - friendly service name.
- created_at - timestamp for when this service was added.

## Restrictions
Service `service_id = 1` is core `static`.
Triggers prevent update and deletion of this row.

## Design Requirements
- Platform integrations should resolve service by `name` and cache the resolved id.
- Keep service keys stable once deployed to avoid cross-platform drift.
- Use service scoping fields on other tables consistently with this catalog.
