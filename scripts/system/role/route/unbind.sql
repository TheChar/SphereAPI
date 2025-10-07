DELETE FROM RoleRoute
WHERE
    RoleID = (SELECT RoleID FROM Roles WHERE Title = %(RoleTitle)s AND ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s)) AND
    RouteID = (SELECT RouteID FROM Routes WHERE Operation = %(Operation)s AND RouteName = %(RouteName)s);