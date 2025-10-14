DO $$
DECLARE is_owner BOOLEAN;
BEGIN

SELECT %(ContributorID)s = (SELECT Owner FROM Tags WHERE TagID = %(TagID)s)
INTO is_owner;

IF NOT is_owner
THEN
RAISE EXCEPTION 'User cannot edit a tag they do not own';
END IF;

UPDATE Tags
SET
    Title = COALESCE(%(Title)s, Title),
    Implements = COALESCE(%(Implements)s, Implements),
    IsPublic = COALESCE(%(IsPublic)s, IsPublic)
WHERE TagID = %(TagID)s;

RETURN 'Success';
END $$;