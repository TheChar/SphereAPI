DO $$
DECLARE is_owner BOOLEAN;
BEGIN

--Get ownership status
SELECT IsOwner
INTO is_owner
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND ContributorID = %(ContributorID)s;

--Exception Handling
IF NOT is_owner
THEN
RAISE EXCEPTION 'User must own project to edit metadata';
END IF;

--Update projects only if the field is given
UPDATE Projects
SET
    Title = COALESCE(%(Title)s, Title),
    Description = COALESCE(%(Description)s, Description),
    Version = COALESCE(%(Version)s, Version),
WHERE ProjectID = %(ProjectID)s;
RETURN "Success";
END $$;