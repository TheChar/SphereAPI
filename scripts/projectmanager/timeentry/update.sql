DO $$
BEGIN

--Error if trying to edit an entry that doesn't belong to user
IF %(ContributorID)s != (SELECT ContributorID FROM ProjectContributor WHERE ProjectContributorID = (SELECT ProjectContributorID FROM TimeEntries WHERE TimeEntryID = %(TimeEntryID)s))
THEN
RAISE EXCEPTION 'User cannot edit an entry they did not create'
END IF;

UPDATE TimeEntries
SET
    StartTime = COALESCE(%(StartTime)s, StartTime),
    EndTime = COALESCE(%(EndTime)s, EndTime),
    Description = COALESCE(%(Description)s, Description),
    Version = COALESCE(%(Version)s, Version)
WHERE TimeEntryID = %(TimeEntryID)s;

RETURN 'Success';
END $$;