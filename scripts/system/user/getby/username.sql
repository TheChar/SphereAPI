SELECT U.UserID AS UID,
    U.Username,
    U.HashedPassword,
    U.ExpireMinutes
FROM Users U
WHERE Username = %(Username)s;