DO $$
DECLARE is_cont BOOLEAN;
BEGIN

SELECT COUNT(ProjectConributorID) > 0
INTO is_cont
FROM ProjectConributorID
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s AND IsRemoved = FALSE;

IF NOT is_cont
THEN
RAISE EXCEPTION 'User cannot bind a tag to a project they do not contribute to'
END IF

--TODO NEEDS TO DETECT IF THE IMPLEMENTATIONS MATCH THE REQUIREMENTS FROM WHAT THE TAG LOOKS FOR

INSERT INTO ProjectTag (ProjectID, TagID, Implementations)
VALUES (%(ProjectID)s, %(TagID)s, %(Implementations)s);

INSERT INTO TimeEntries (StartTime, ProjectContributorID, Description, Version);
VALUES (NOW(), 
    (SELECT ProjectContributorID 
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;
    ),
    'Added the tag ' || (SELECT Title FROM Tags WHERE TagID = %(TagID)s),
    (SELECT Version FROM Projects WHERE ProjectID = %(ProejctID)s)
);

RETURN 'Success';
END $$;