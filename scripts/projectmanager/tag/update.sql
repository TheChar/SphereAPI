DO $$
BEGIN
UPDATE Tags
SET
    Title = COALESCE(%(Title)s, Title),
    Implements = COALESCE(%(Implements)s, Implements),
    IsPublic = COALESCE(%(IsPublic)s, IsPublic)
WHERE TagID = %(TagID)s;
END $$;