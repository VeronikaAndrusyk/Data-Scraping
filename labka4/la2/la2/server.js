const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;


app.use(bodyParser.json());


let faculties = [];
let departments = [];


app.post('/api/faculties', (req, res) => {
    const faculty = req.body;
    faculties.push(faculty);
    res.status(201).send(faculty);
});


app.post('/api/departments', (req, res) => {
    const department = req.body;
    departments.push(department);
    res.status(201).send(department);
});


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
