INSERT INTO Routes (Operation, RouteName)
VALUES (%(Operation)s, %(RouteName)s)
ON CONFLICT DO NOTHING;

INSERT INTO RoleRoute (RoleID, RouteID)
VALUES (
    (SELECT RoleID FROM Roles WHERE Title = %(RoleTitle)s AND ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s)),
    (SELECT RouteID FROM Routes WHERE Operation = %(Operation)s AND RouteName = %(RouteName)s)
)
ON CONFLICT DO NOTHING;