DELETE FROM UserRole
WHERE
    UserID = (SELECT U.UserID FROM Users U WHERE U.Username = %(username)s) AND
    RoleID = (SELECT R.RoleID FROM Roles R WHERE R.Route = %(route)s AND R.Operation = %(operation)s);

--Return roles from UserRole table for inspection
SELECT *
FROM UserRole UR
LEFT JOIN Users U ON UR.UserID = U.UserID
LEFT JOIN Roles R ON R.RoleID = UR.RoleID
WHERE U.Username = %(username)s;