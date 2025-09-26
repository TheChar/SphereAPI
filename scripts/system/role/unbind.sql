DELETE FROM UserRole
WHERE
    UserID = (SELECT U.UserID FROM Users U WHERE U.Username = %(username)s) AND
    RoleID = (SELECT R.RoleID FROM Roles R WHERE R.Route = %(route)s AND R.Operation = %(operation)s);

--Return roles from UserRole table for inspection
SELECT R.Operation,
    R.Route
FROM Roles R
LEFT JOIN UserRole UR ON UR.RoleID = R.RoleID
LEFT JOIN Users U ON UR.UserID = U.UserID
WHERE U.Username = %(username)s