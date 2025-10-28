DO $$
DECLARE 
    num_projects_owned INT;
    num_orgs_owned INT;
BEGIN
--Get num projects
SELECT COUNT(ProjectContributorID)
INTO num_projects_owned
FROM ProjectContributor
WHERE ContributorID = %(contributorID)s AND IsOwner = True;
--Get num orgs
SELECT COUNT(ContributorOrganizationID)
INTO num_orgs_owned
FROM ContributorOrganization
WHERE ContributorID = %(contributorID)s AND  IsOwner = True;
--Exception handling for orgs
IF num_orgs_owned > 0
THEN
RAISE EXCEPTION 'User still owns at least one organization that must be deleted or transferred';
END IF;
--Exception handling for projects
IF num_projects_owned > 0
THEN RAISE EXCEPTION 'User still owns at least one project that must be deleted or transferred';
END IF;
--Remove user from orgs
DELETE FROM ContributorOrganization
WHERE ContributorID = %(contributorID)s;
--Remove tags owned by user
DELETE FROM Tags
WHERE Owner = %(contributorID)s;
--Remove ProjectContributor entries
DELETE FROM ProjectContributor
WHERE ContributorID = %(contributorID)s;
--Remove Contributor
DELETE FROM Contributors
WHERE ContributorID = %(contributorID)s;
END $$;