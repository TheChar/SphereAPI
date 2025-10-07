CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE,
    HashedPassword VARCHAR(80),
    Name VARCHAR(50),
    ExpireMinutes INT
);

CREATE TABLE Applications (
    ApplicationID SERIAL PRIMARY KEY,
    Title VARCHAR(50) UNIQUE
);

CREATE TABLE Routes (
    RouteID SERIAL PRIMARY KEY,
    Operation VARCHAR(15),
    RouteName VARCHAR(100),
    CONSTRAINT uq_operation_routename
        UNIQUE (Operation, RouteName)
);

CREATE TABLE Roles (
    RoleID SERIAL PRIMARY KEY,
    Title VARCHAR(50),
    Description VARCHAR(300),
    ApplicationID INT,
    CONSTRAINT fk_roles_applications
        FOREIGN KEY (ApplicationID)
        REFERENCES Applications (ApplicationID),
    CONSTRAINT uq_title_applicationid
        UNIQUE (Title, ApplicationID)
);

CREATE TABLE RoleRoute (
    RoleRouteID SERIAL PRIMARY KEY,
    RoleID INT,
    RouteID INT,
    CONSTRAINT fk_roles_roleroute
        FOREIGN KEY (RoleID)
        REFERENCES Roles (RoleID),
    CONSTRAINT fk_routes_roleroute
        FOREIGN KEY (RouteID)
        REFERENCES Routes (RouteID),
    CONSTRAINT unique_roleid_routeid
        UNIQUE (RoleID, RouteID)
);

CREATE TABLE UserApplication (
    UserApplicationID SERIAL PRIMARY KEY,
    UserID INT,
    ApplicationID INT,
    RoleID INT,
    JoinDate DATE,
    Data JSON,
    CONSTRAINT fk_users_userapplication
        FOREIGN KEY (UserID)
        REFERENCES Users (UserID),
    CONSTRAINT fk_applications_userapplication
        FOREIGN KEY (ApplicationID)
        REFERENCES Applications (ApplicationID),
    CONSTRAINT fk_roles_userapplication
        FOREIGN KEY (RoleID)
        REFERENCES Roles (RoleID),
    CONSTRAINT uq_userid_applicationid
        UNIQUE (UserID, ApplicationID)
);

-- -- List all tables in the current schema
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'public';