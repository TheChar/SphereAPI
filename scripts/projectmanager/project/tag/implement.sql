DO $$
BEGIN
UPDATE ProjectTag
SET
    Implementations = %(Implementations)s
WHERE TagID = %(TagID)s AND ProjectID = %(ProjectID)s;
END $$;