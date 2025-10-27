DO $$
DECLARE new_owner_cont BOOLEAN,
caller_owner BOOLEAN;
BEGIN

SELECT COUNT(ProjectContributorID) > 0
INTO new_owner_cont
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(NewOwnerID)s;

SELECT COUNT(ProjectContributorID) > 0
INTO caller_owner
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s and IsOwner = TRUE;

IF NOT new_owner_cont
THEN
RAISE EXCEPTION 'User cannot transfer ownership to a contributor not associated with the project';
END IF;

IF NOT caller_owner
THEN
RAISE EXCEPTION 'User cannot transfer ownership of a project they do not own';
END IF;

UPDATE ProjectContributor
SET IsOwner = TRUE
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(NewOwnerID)s;

UPDATE ProjectContributor
SET IsOwner = FALSE
WHERE ProejctID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

INSERT INTO TimeEntries(StartTime, ProjectContributorID, Description, Version)
VALUES (
    NOW(),
    (SELECT ProjectContributorID
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;    
    ),
    'Stepped down from ownership',
    (SELECT Version FROM Projects WHERE ProjectID = %(ProjectID)s)
);

INSERT INTO TimeEntries(StartTime, ProjectContributorID, Description, Version)
VALUES (
    NOW(),
    (SELECT ProjectContributorID
        FROM ProjectContributor
        WHERE ProjectID = %(ProjectID)s AND ContributorID = %(NewOwnerID)s;
    ),
    'Assumed ownership',
    (SELECT Version FROM Projects WHERE ProejctID = %(ProjectID)s)
);
END $$;