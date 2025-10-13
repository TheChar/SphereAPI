INSERT INTO Contributors (Name)
VALUES (%(Name)s)
RETURNING ContributorID;