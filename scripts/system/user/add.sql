WITH NewUser AS (
    INSERT INTO Users (Username, HashedPassword, Name, ExpireMinutes)
    VALUES (%(Username)s, %(HashedPassword)s, %(Name)s, %(ExpMins)s)
    RETURNING UserID
)
INSERT INTO UserApplication (UserID, ApplicationID, RoleID, JoinDate, Data)
VALUES (
    (SELECT UserID FROM NewUser),
    (SELECT ApplicationID FROM Applications WHERE Title = 'System'),
    (SELECT RoleID FROM Roles WHERE ApplicationID = (SELECT ApplicationID FROM Applications WHERE Title = 'System') AND Title = 'Default'),
    %(JoinDate)s,
    NULL
)
RETURNING 'Success';