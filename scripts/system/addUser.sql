INSERT INTO Users (Username, HashedPassword, UserType)
VALUES (%(username)s, %(hashedpassword)s, (
    SELECT UT.UserTypeID
    FROM UserTypes UT
    WHERE UT.Type = %(usertype)s
))
RETURNING UserID, Username;