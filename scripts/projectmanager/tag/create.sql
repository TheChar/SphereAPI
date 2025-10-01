INSERT INTO Tags (Title, Implements, Owner)
VALUES (
    %(Title)s,
    %(Implements)s,
    %(OwnerContributorID)s
)
RETURNING TagID;