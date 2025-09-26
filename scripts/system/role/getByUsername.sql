SELECT R.Operation,
    R.Route
FROM Roles R
LEFT JOIN UserRole UR ON UR.RoleID = R.RoleID
LEFT JOIN Users U ON UR.UserID = U.UserID
WHERE U.Username = %(username)s