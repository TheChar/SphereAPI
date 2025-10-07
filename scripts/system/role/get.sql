SELECT *
FROM Roles
WHERE Title = %(RoleTitle)s AND ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s);