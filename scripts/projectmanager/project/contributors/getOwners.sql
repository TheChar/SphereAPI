SELECT ContributorID
FROM ProjectContributor
WHERE ProjectID = %(ProjectID)s AND IsOwner = TRUE;