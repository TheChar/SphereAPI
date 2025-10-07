WITH AppID AS (
    SELECT ApplicationID AID
    FROM Applications
    WHERE Title = %(AppTitle)s
)
UPDATE UserApplication
SET RoleID = (SELECT RoleID FROM Roles WHERE Title = %(RoleTitle)s AND ApplicationID = (SELECT AID FROM AppID))
WHERE UserID = (SELECT UserID FROM Users WHERE Username = %(Username)s);