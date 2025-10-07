WITH AppID AS (
    SELECT ApplicationID AID
    FROM Applications
    WHERE Title = %(AppTitle)s
)
INSERT INTO UserApplication (UserID, ApplicationID, RoleID, JoinDate, Data)
VALUES (
    (SELECT UserID FROM Users WHERE Username = %(Username)s),
    (SELECT AID FROM AppID),
    (SELECT RoleID FROM Roles WHERE Title = %(RoleTitle)s AND ApplicationID = (SELECT AID FROM AppID)),
    %(JoinDate)s,
    %(Data)s
);