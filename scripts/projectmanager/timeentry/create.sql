DO $$
DECLARE is_cont BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_cont
FROM ProjectContributor
WHERE ProjectID = %(ProjectID) AND ContributorID = %(ContributorID)s AND IsRemoved = FALSE;

IF NOT is_cont
THEN
RAISE EXCEPTION 'User cannot create time entry for project they do not contribute to';
END IF;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version)
VALUES (NOW(),
    (SELECT ProjectContributorID
    FROM ProjectContributor
    WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;
    ),
    %(Description)s,
    COALESCE(%(Version)s, (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s))
);

RETURN 'Success';
END $$;