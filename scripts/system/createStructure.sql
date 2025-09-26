CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username Varchar(50) UNIQUE,
    HashedPassword Varchar(80)
);

CREATE TABLE Roles (
    RoleID SERIAL PRIMARY KEY,
    Operation Varchar(10),
    Route Varchar(50)
);

CREATE TABLE UserRole (
    UserRoleID SERIAL PRIMARY KEY,
    UserID INT,
    RoleID INT,
    CONSTRAINT fk_users_userrole
        FOREIGN KEY (UserID)
        REFERENCES Users (UserID),
    CONSTRAINT fk_roles_userrole
        FOREIGN KEY (RoleID)
        REFERENCES Roles (RoleID)
);

-- -- List all tables in the current schema
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'public';