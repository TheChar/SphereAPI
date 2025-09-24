CREATE TABLE UserTypes (
    UserTypeID SERIAL PRIMARY KEY,
    Type Varchar(50) UNIQUE
);

CREATE TABLE Routes (
    RouteID SERIAL PRIMARY KEY,
    Pathname Varchar(50) UNIQUE
);

CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username Varchar(50) UNIQUE,
    HashedPassword Varchar(80),
    UserTypeID INTEGER,
    CONSTRAINT fk_users_usertypes
        FOREIGN KEY (UserTypeID)
        REFERENCES UserTypes (UserTypeID)
);

CREATE TABLE UserRoute (
    UserRouteID SERIAL PRIMARY KEY,
    UserID INTEGER,
    RouteID INTEGER,
    CONSTRAINT fk_users_userroute
        FOREIGN KEY (UserID)
        REFERENCES Users (UserID),
    CONSTRAINT fk_routes_userroute
        FOREIGN KEY (RouteID)
        REFERENCES Routes (RouteID)
);

-- List all tables in the current schema
SELECT tablename
FROM pg_catalog.pg_tables
WHERE datname = 'api_system';