UPDATE Users
SET HashedPassword = %(HashedPassword)s
WHERE Username = %(Username)s;