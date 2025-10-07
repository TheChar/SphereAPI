WITH QueriedRole AS (
    SELECT RoleID
    FROM Roles
    WHERE Title = %(RoleTitle)s AND ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s)
)
SELECT RT.Operation,
    RT.RouteName
FROM Routes RT
LEFT JOIN RoleRoute RR ON RT.RouteID = RR.RouteID
WHERE RR.RoleID = (SELECT RoleID FROM QueriedRole)