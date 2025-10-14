DO $$
DECLARE is_cont BOOLEAN,
    tag_implemented BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO is_cont
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s AND IsRemoved = FALSE;

SELECT COUNT(ProjectTagID) > 0
INTO tag_implemented
FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;

IF NOT is_cont
THEN
RAISE EXCEPTION 'User cannot unbind a tag from a project user does not contribute to';
END IF;

IF NOT tag_implemented
THEN
RAISE EXCEPTION 'User cannot remove a tag that is not implemented';
END IF;

DELETE FROM ProjectTag
WHERE ProjectID = %(ProjectID)s AND TagID = %(TagID)s;

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version);
VALUES (NOW(), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;
    ),
    'Removed the tag ' || (SELECT Title FROM Tags WHERE TagID = %(TagID)s),
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);

RETURN 'Success';
END $$;
