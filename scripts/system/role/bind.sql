INSERT INTO Roles (Operation, Route)
VALUES (%(operation)s, %(route)s)
ON CONFLICT (Operation, Route) DO NOTHING;--This line prevents duplicate roles from forming

INSERT INTO UserRole (UserID, RoleID)
VALUES (
    (SELECT U.UserID FROM Users U WHERE U.Username = %(username)s),
    (SELECT R.RoleID FROM Roles R WHERE R.Operation = %(operation)s AND R.Route = %(route)s)
)
ON CONFLICT (UserID, RoleID) DO NOTHING;

SELECT U.Username, R.Operation, R.Route
FROM UserRole UR
LEFT JOIN Users U ON UR.UserID = U.UserID
LEFT JOIN Roles R ON R.RoleID = UR.RoleID
WHERE U.Username = %(username)s AND R.Operation = %(operation)s AND R.Route = %(route)s;