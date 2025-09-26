INSERT INTO Users (Username, HashedPassword, ExpireMinutes)
VALUES (%(username)s, %(hashedpassword)s, %(expmins)s)
RETURNING UserID, Username;