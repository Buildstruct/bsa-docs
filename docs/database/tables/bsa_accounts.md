# bsa_accounts
Accounts link players to provider-specific identities.\
A player can have one account per provider.

!!! warning
    This table may incur high reads to the database due to its relevance!\
    Please ensure your platform isn't requesting information so often.

## Structure
```sql
CREATE TABLE `bsa_accounts` (
    `account_id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `provider_id` BIGINT UNSIGNED NOT NULL,
    `player_id` BIGINT UNSIGNED NOT NULL,
    `identifier` VARCHAR(255) NOT NULL,
    `username` VARCHAR(255) NULL,
    `time` BIGINT UNSIGNED NOT NULL DEFAULT 0,
    `heartbeat_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),

	CONSTRAINT uq_acct_type UNIQUE (`player_id`, `provider_id`),
	CONSTRAINT uq_acct_type_identifier UNIQUE (`provider_id`, `identifier`),

	CONSTRAINT fk_acct_player
		FOREIGN KEY (`player_id`) REFERENCES `bsa_players`(`player_id`)
			ON DELETE CASCADE
			ON UPDATE CASCADE,

	CONSTRAINT fk_acct_types
		FOREIGN KEY (`provider_id`) REFERENCES `bsa_providers`(`provider_id`)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);
```

- account_id - unique id of the account.
- provider_id - provider that owns this account identity.
- player_id - player that owns the account.
- identifier - unique provider identifier (`steamid64`, `snowflake`, etc) within a provider.
- username - provider username at time of record.
- time - generic time accumulator for the account.
- heartbeat_at - account heartbeat used for recent activity.
- created_at - timestamp for when the account was created.

## Restrictions
There are two core accounts with locked records.

- 1 - `SYSTEM`
- 2 - `CONSOLE`

Triggers prevent update or deletion of these rows.

## Design Requirements
- Do not run account-link lookups in a hot path per packet/tick; cache account-to-player mappings.
- When linking accounts, require provider-side proof of ownership before writing `identifier`.
- Update `heartbeat_at` only while a platform has a live, authenticated session for that account.
- Treat `uq_acct_type` as authoritative: one player per provider account type.
- Treat `uq_acct_type_identifier` as authoritative: one provider identifier can only belong to one player.

## Interlink Behavior
- Account presence and session ownership are coordinated with periodic `heartbeat_at` updates and `server_id` attach/detach writes.
- You must apply a `session_id` from `bsa_sessions` to the account data being networked.
- `database.players:connected(account, secondaries)`
- `database.players:disconnected(account, secondaries)`
- `database.players:timeset(account, time_seconds)`
