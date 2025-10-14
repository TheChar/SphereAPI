DO $$
BEGIN

IF %(ContributorID)s != (SELECT ContributorID FROM ProjectContributor WHERE ProjectContributorID = (SELECT ProjectContributorID FROM TimeEntries WHERE TimeEntryID = %(TimeEntryID)s))
THEN
RAISE EXCEPTION 'User cannot delete an entry they did not create'
END IF;

DELETE FROM TimeEntries
WHERE TimeEntryID = %(TimeEntryID)s;

RETURN 'Success';
END $$;