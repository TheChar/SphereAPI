SELECT R.Title
FROM Roles R
WHERE R.ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(Title)s);