INSERT INTO Roles (Title, Description, ApplicationID)
VALUES (%(Title)s, %(Description)s, (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s))
RETURNING RoleID;