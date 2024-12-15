// Import required modules
import express from 'express';   // Import express for setting up the backend
import cors from 'cors';         // Import CORS for cross-origin requests
import dotenv from 'dotenv';     // Import dotenv to securely handle environment variables

// Initialize dotenv to read from .env file
dotenv.config();

// Create an instance of express
const app = express();

// Enable CORS for all routes
app.use(cors());

// Middleware to parse incoming JSON requests
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Define a simple route to test the server
app.get('/', (req, res) => {
    res.json({ message: 'Server is working!' });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
import { createPool } from 'mysql2';  // Import mysql2 for MySQL database connection

// Create a connection pool to the MySQL database
const pool = createPool({
    host: process.env.MYSQL_HOST,          // Database host
    user: process.env.MYSQL_USER,          // Database user
    password: process.env.MYSQL_PASSWORD,  // Database password
    database: process.env.MYSQL_DATABASE,  // Database name
    waitForConnections: true,              // Wait for connections
    connectionLimit: 10,                   // Max number of connections to allow
    queueLimit: 0                          // No limit for the connection queue
}).promise();

// Test the MySQL connection to ensure everything is set up correctly
pool.getConnection()
    .then((connection) => {
        console.log('Connected to MySQL!');
        connection.release();  // Release the connection when done
    })
    .catch((err) => {
        console.error('Error connecting to MySQL:', err);
    });
// Example function to get users from the database
const getUsers = async () => {
    try {
        const [rows] = await pool.query('SELECT * FROM users');
        return rows;  // Returns all rows from the "users" table
    } catch (error) {
        console.error('Error fetching users:', error);
    }
};
// Test route to fetch users from the database
app.get('/users', async (req, res) => {
    try {
        const users = await getUsers();  // Call the function to get users
        res.json(users);  // Return the users as a JSON response
    } catch (error) {
        res.status(500).json({ error: 'Error fetching users' });
    }
});
