# bsa_providers
Providers represent identity backends (`steam`, `discord`, `minecraft`, etc).

## Structure
```sql
CREATE TABLE `bsa_providers` (
    `provider_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `alias` TINYTEXT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
```

- provider_id - unique provider id.
- name - unique provider key, such as `steam`.
- alias - friendly provider name, such as `Steam`.
- created_at - timestamp for when this provider was added.

## Restrictions
Provider `provider_id = 1` is the core `static` provider.
Triggers prevent update and deletion of this row.

## Design Requirements
- Platform integrations should bind to provider `name`, not hardcoded numeric IDs.
- Reserve provider `static` for internal/system identities and metadata workflows.
- Keep provider catalog stable; avoid renaming once integrations depend on it.
