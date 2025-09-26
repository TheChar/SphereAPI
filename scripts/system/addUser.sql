INSERT INTO Users (Username, HashedPassword)
VALUES (%(username)s, %(hashedpassword)s)
RETURNING UserID, Username;