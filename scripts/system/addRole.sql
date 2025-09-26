INSERT INTO Roles (Operation, Route)
VALUES (%(operation)s, %(route)s)
RETURNING RoleID;