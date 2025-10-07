DELETE FROM UserApplication
WHERE ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = %(AppTitle)s)
AND UserID = (SELECT UserID FROM Users WHERE Username = %(Username)s);