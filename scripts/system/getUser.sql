SELECT
    U.UserID AS UID,
    U.Username AS Username,
    U.HashedPassword AS HashedPassword,
    UT.Type AS Type
FROM Users U
LEFT JOIN UserType UT ON U.UserTypeID = UT.UserTypeID
WHERE Username=%(username)s