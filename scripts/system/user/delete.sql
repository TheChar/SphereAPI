DO $$
BEGIN
IF (
    SELECT COUNT(UA.UserApplicationID)
    FROM UserApplication UA
    LEFT JOIN Users U ON U.UserID = UA.UserID
    LEFT JOIN Applications A ON UA.ApplicationID = A.ApplicationID
    WHERE A.Title != 'System' AND U.Username = %(Username)s
) > 0 THEN
RAISE EXCEPTION 'User is registered to an application outside of the System';
END IF;

DELETE FROM UserApplication
WHERE UserID = (SELECT UserID FROM Users WHERE Username = %(Username)s);

DELETE FROM Users
WHERE Username = %(Username)s;
END $$;