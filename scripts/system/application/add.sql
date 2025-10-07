INSERT INTO Applications (Title)
VALUES (%(Title)s)
RETURNING ApplicationID;