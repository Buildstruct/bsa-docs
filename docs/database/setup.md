# Setup

Before getting started, ensure you have **MySQL 8.0+** or **MariaDB 10.6+** already installed.\
We recommend that before starting that you understand some SQL basics and have OS-level access to your server.

Depending on your OS, you may be using package managers like `apt` or `yum`.\
For BSA it typically doesn't matter as long as you can run MySQL or MariaDB 10.6+.

!!! warning
	We highly recommend hosting this locally with your game servers.\
	Allowing external connections can put you at greater risk.

After installation, log in as root:

```bash
sudo mysql -u root -p
```

## Preliminary

You will need to create a schema and a dedicated user for it.

!!! warning
	For isolation purposes, grant the user access to the BSA schema only.

```sql
-- Create the database with BSA's required character set
CREATE DATABASE bsa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a user (use 'localhost' if your servers connect from the same host)
CREATE USER 'bsa'@'localhost' IDENTIFIED BY '<password>';

-- Grant full access to the BSA schema only
GRANT ALL ON `bsa`.* TO 'bsa'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
```

## Event Scheduler

BSA uses MySQL scheduled events to automatically clean up stale commands and temporary servers.\
Enable the event scheduler globally:

```sql
SET GLOBAL event_scheduler = ON;
```

To persist this across restarts, add the following to your MySQL config file (`my.cnf` on Linux, `my.ini` on Windows) under `[mysqld]`:

```ini
[mysqld]
event_scheduler=ON
```

!!! note
	If you skip this, the `bsa_command` and `bsa_servers` cleanup jobs will not run automatically.\
	You can call `CALL sp_cleanup_commands()` and `CALL sp_cleanup_servers()` manually, but enabling the scheduler is recommended.

## SQL Playbook

!!! warning
	You **must** import using the MySQL CLI, not phpMyAdmin's SQL editor or a GUI query box.\
	The playbook uses `DELIMITER` syntax for triggers and stored procedures that only works correctly via the CLI.

Import `bsa.sql` from the `bsa-core-database` repository:

```bash
mysql -u root -p bsa < bsa.sql
```

If your database server is remote:

```bash
mysql -h your.db.host -u root -p bsa < bsa.sql
```

After running this, you should see BSA tables, triggers, stored procedures, and scheduled events.

## Maintainer's Group

BSA reserves group ID 1 (`system`) for internal system-level operations.\
As the database maintainer, you will need to assign yourself to this group initially.\
It is required to manage groups, permissions, and other BSA entities through any platform interface.

!!! warning
	This group should only be held by the person responsible for the system itself.\
	Do not assign it to regular users.

Once your account exists in `bsa_accounts`, assign yourself:

```sql
SET @bsa_allow_reserved_group_assignment = 1;
UPDATE bsa_players SET group_id = 1 WHERE player_id = (SELECT player_id FROM bsa_accounts WHERE identifier = '<identifier>');
SET @bsa_allow_reserved_group_assignment = 0;
```

Replace `<identifier>` with your platform identifier (e.g. SteamID64 for Garry's Mod).\
Your account is created automatically the first time you connect through a platform.

This group is by default considered the highest authority.

## Granting Permissions

If required, you can grant permissions from within SQL:

```sql
INSERT INTO bsa_group_permissions (group_id, perm_id, service_id, provider_id, server_id)
SELECT g.group_id, p.perm_id, NULL, NULL, NULL
FROM bsa_groups g
CROSS JOIN bsa_permissions p
WHERE g.name = '<group_name>'
AND NOT EXISTS (
	SELECT 1
	FROM bsa_group_permissions gp
	WHERE gp.group_id = g.group_id
	  AND gp.perm_id = p.perm_id
	  AND gp.service_id IS NULL
	  AND gp.provider_id IS NULL
	  AND gp.server_id IS NULL
);
```

`NULL` on the scope columns means the permission applies community-wide across all services and servers.\
We recommend using this for groups that should have unrestricted access.
