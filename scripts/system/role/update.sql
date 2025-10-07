UPDATE Roles
SET Description = %(Description)s
WHERE ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s) AND Title = %(RoleTitle)s;