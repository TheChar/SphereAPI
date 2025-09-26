SELECT
    U.UserID AS UID,
    U.Username,
    U.HashedPassword
FROM Users U
WHERE U.Username=%(username)s