CREATE TABLE IF NOT EXISTS Organizations (
    OrganizationID SERIAL PRIMARY KEY,
    Title VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS Contributors (
    ContributorID SERIAL PRIMARY KEY,
    Name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ContributorOrganization (
    ContributorOrganizationID SERIAL PRIMARY KEY,
    ContributorID INT,
    OrganizationID INT,
    IsOwner BOOLEAN,
    CONSTRAINT fk_contributor_contributororganization
        FOREIGN KEY (ContributorID)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT fk_organization_contributororganization
        FOREIGN KEY (OrganizationID)
        REFERENCES Organizations (OrganizationID),
    CONSTRAINT unique_contributor_organization
        UNIQUE (ContributorID, OrganizationID)
);

CREATE TABLE IF NOT EXISTS Projects (
    ProjectID SERIAL PRIMARY KEY,
    Title VARCHAR(100),
    Version VARCHAR(30),
    Description VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS ProjectContributor (
    ProjectContributorID SERIAL PRIMARY KEY,
    ProjectID INT,
    ContributorID INT,
    IsOwner BOOLEAN,
    IsRemoved BOOLEAN,
    CONSTRAINT fk_project_projectcontributor
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_contributor_projectcontributor
        FOREIGN KEY (ContributorID)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT unique_project_contributor
        UNIQUE (ContributorID, ProjectID)
);

CREATE TABLE IF NOT EXISTS TimeEntries (
    TimeEntryID SERIAL PRIMARY KEY,
    StartTime DATE,
    EndTime DATE,
    ProjectContributorID INT,
    Description VARCHAR(300),
    Version VARCHAR(30),
    CONSTRAINT fk_timeentry_projectcontributor
        FOREIGN KEY (ProjectContributorID)
        REFERENCES ProjectContributor (ProjectContributorID)
);

CREATE TABLE IF NOT EXISTS Tags (
    TagID SERIAL PRIMARY KEY,
    Title VARCHAR(80),
    Implements JSON,
    IsPublic BOOLEAN,
    Owner INT,
    CONSTRAINT fk_tags_contributors
        FOREIGN KEY (Owner)
        REFERENCES Contributors (ContributorID),
    CONSTRAINT unique_title_owner
        UNIQUE (Title, Owner)
);

CREATE TABLE IF NOT EXISTS ProjectTag (
    ProjectTagID SERIAL PRIMARY KEY,
    ProjectID INT,
    TagID INT,
    Implementations JSON,
    CONSTRAINT fk_projects_projecttag
        FOREIGN KEY (ProjectID)
        REFERENCES Projects (ProjectID),
    CONSTRAINT fk_tags_projecttag
        FOREIGN KEY (TagID)
        REFERENCES Tags (TagID),
    CONSTRAINT unique_project_tag
        UNIQUE (ProjectID, TagID)
);

CREATE OR REPLACE FUNCTION is_contributor(contributor_ID INT, project_ID INT)
RETURNS BOOLEAN
AS $$
BEGIN
RETURN EXISTS (
    SELECT 1
    FROM ProjectContributor
    WHERE ProjectID = project_ID
    AND ContributorID = contributor_ID
    AND IsRemoved = FALSE
);
END; 
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_owner(contributor_ID INT, project_ID INT)
RETURNS BOOLEAN
AS $$
BEGIN
RETURN EXISTS (
    SELECT 1
    FROM ProjectContributor
    WHERE ProjectID = project_ID
    AND ContributorID = contributor_ID
    AND IsOwner = TRUE
);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_tag_owner(contributor_ID INT, tag_ID INT)
RETURNS BOOLEAN
AS $$
BEGIN
RETURN contributor_ID == (
    SELECT Owner
    FROM Tags
    WHERE TagID = tag_ID
);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_tag_public(tag_ID INT)
RETURNS BOOLEAN
AS $$
BEGIN
RETURN (
    SELECT IsPublic
    FROM Tags
    WHERE TagID = tag_ID
);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_timeentry_owner(contributor_ID INT, timeentry_ID INT)
RETURNS BOOLEAN
AS $$
BEGIN
RETURN contributor_ID == (
    SELECT PC.ContributorID
    FROM ProjectContributor PC
    LEFT JOIN TimeEntries TE ON TE.ProjectContributorID = PC.ProjectContributorID
);
END;
$$ LANGUAGE plpgsql;