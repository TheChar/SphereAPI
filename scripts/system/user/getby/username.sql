SELECT U.UserID AS UID,
    U.Username,
    U.HashedPassword,
    U.Name,
    U.ExpireMinutes
FROM Users U
WHERE Username = %(Username)s;