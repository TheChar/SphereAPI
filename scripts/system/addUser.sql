INSERT INTO Users (Username, HashedPassword, UserType)
VALUES (%(username), %(hashedpassword), (
    SELECT UT.UserTypeID
    FROM UserTypes UT
    WHERE UT.Type = %(usertype)
))
RETURNING UserID, Username;