CREATE TABLE Roles(
					role_id  char(20) NOT NULL,
                    role_name char(50) NOT NULL
                    );
CREATE TABLE Users(
					user_id  char(20)  NOT NULL,
                    user_name char(50) NOT NULL,
                    user_passwd char(20) NOT NULL,
                    role_id char(20)  NOT NULL
                    );
ALTER TABLE Roles ADD PRIMARY KEY (role_id);
ALTER TABLE Users ADD PRIMARY KEY (user_id);
ALTER TABLE Users ADD CONSTRAINT FK_Users_Roles FOREIGN KEY (role_id) REFERENCES Roles (role_id);

