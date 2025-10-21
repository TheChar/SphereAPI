DO $$
DECLARE is_owner BOOLEAN;
BEGIN

SELECT Owner == %(ContributorID)s
INTO is_owner
FROM Tags
WHERE TagID = %(TagID)s;

IF NOT is_owner
THEN
RAISE EXCEPTION "User must own a tag to delete it.";
END IF;

DELETE FROM Tags
WHERE TagID = %(TagID)s;

SELECT "Success";

END $$;