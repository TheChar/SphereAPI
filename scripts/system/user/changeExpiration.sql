UPDATE Users
SET ExpireMinutes = %(ExpMins)s
WHERE Username = %(Username)s;