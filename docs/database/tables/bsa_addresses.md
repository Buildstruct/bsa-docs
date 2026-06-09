# bsa_addresses
Tracks the 1:N relationship between accounts and observed IP addresses.

## Structure

```sql
CREATE TABLE IF NOT EXISTS `bsa_addresses` (
    `address_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `account_id` BIGINT UNSIGNED NOT NULL,
    `address` VARCHAR(46) NOT NULL,
    `occurrence` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),

    CONSTRAINT fk_address_account
        FOREIGN KEY (`account_id`) REFERENCES `bsa_accounts`(`account_id`)
            ON DELETE CASCADE
            ON UPDATE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

- address_id - unique row identifier.
- account_id - account this address belongs to.
- address - IPv4 or IPv6 address observed for the account.
- occurrence - first time the address was seen for this account.
- updated - last time this address was observed.

## Design Requirements
- Cascade on account delete, addresses have no independent meaning without an account.