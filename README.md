# ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'ODBC Driver 17 for SQL Server' : file not found (0) (SQLDriverConnect)")
Suive ce lien pour installation Microsoft ODBC 18 ou 17
https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16


# ('08001', '[08001] [Microsoft][ODBC Driver 18 for SQL Server]SSL Provider: [error:0A000086:SSL routines::certificate verify failed:self-signed certificate] (-1) (SQLDriverConnect)')
 Corriger en Ajoutant : `TrustServerCertificate=yes;` à la chaîne de connexion
 donc `"DRIVER={ODBC Driver 18 for SQL Server};SERVER=$url;DATABSE=$db;UID=$usr;TrustServerCertificate=yes;"`


