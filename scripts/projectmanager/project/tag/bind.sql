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

RETURN 'Success';
END $$;