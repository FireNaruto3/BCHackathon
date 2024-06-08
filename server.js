// // const express = require('express');
// // const path = require('path');

// // const app = express();
// // const PORT = process.env.PORT || 3000;

// // // Serve static files
// // app.use(express.static(path.join(__dirname, 'public')));

// // app.get('/', (req, res) => {
// //     res.sendFile(path.join(__dirname, 'index.html'));
// // });

// // app.listen(PORT, () => {
// //     console.log(`Server is running on http://localhost:${PORT}`);
// // });

// const express = require('express');
// const axios = require('axios');
// const bodyParser = require('body-parser');
// const querystring = require('querystring');
// const { generateCodeVerifier, generateCodeChallenge } = require('./pkce');

// const app = express();
// app.use(bodyParser.json());

// const clientId = '23PHCT';
// const clientSecret = 'd40ac1b90bae7901816c8849fca2300b';
// const redirectUri = 'http://localhost:3000/callback';
// // const redirectUri = 'http://127.0.0.1:5500/'; // might be wrong

// let codeVerifier;

// app.get('/auth', (req, res) => {
//     // const authUrl = `https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=heartrate activity sleep&expires_in=604800`;
//     // res.redirect(authUrl);

//     codeVerifier = generateCodeVerifier();
//     const codeChallenge = generateCodeChallenge(codeVerifier);
//     const authUrl = `https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=activity%20heartrate%20sleep&code_challenge=${codeChallenge}&code_challenge_method=S256`;
//     res.redirect(authUrl);
// });

// app.get('/callback', async (req, res) => {
//     const { code } = req.query;

//     const tokenUrl = 'https://api.fitbit.com/oauth2/token';
//     const data = querystring.stringify({
//         client_id: clientId,
//         grant_type: 'authorization_code',
//         redirect_uri: redirectUri,
//         code: code,
//         code_verifier: codeVerifier
//     });

//     const headers = {
//         'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
//         'Content-Type': 'application/x-www-form-urlencoded'
//     };

//     try {
//         const response = await axios.post(tokenUrl, data, { headers });
//         const accessToken = response.data.access_token;
//         const refreshToken = response.data.refresh_token;
//         // Store access and refresh tokens
//         res.json({ accessToken });
//     } catch (error) {
//         res.status(500).send(error);
//     }
// });

// app.get('/fetch-data', async (req, res) => {
//     const accessToken = 'https://api.fitbit.com/oauth2/token'; // TODO: Fill In

//     const fitbitUrl = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json';
//     const headers = {
//         'Authorization': `Bearer ${accessToken}`
//     };

//     try {
//         const response = await axios.get(fitbitUrl, { headers });
//         const data = response.data;

//         // Send data to your website
//         await axios.post('https://yourwebsite.com/api/fitbitdata', data, { // TODO: Fill In?
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         });

//         res.json({ message: 'Data sent to website' });
//     } catch (error) {
//         res.status(500).send(error);
//     }
// });

// app.listen(3000, () => {
//     console.log('Server started on http://localhost:3000');
// });
const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const querystring = require('querystring');
const { generateCodeVerifier, generateCodeChallenge } = require('./pkce');

const app = express();
app.use(bodyParser.json());

const clientId = '23PHCT';
const clientSecret = 'd40ac1b90bae7901816c8849fca2300b';
const redirectUri = 'file:///C:/src/BCHackathon/index.html';

let codeVerifier;

app.get('/auth', (req, res) => {
    try {
        codeVerifier = generateCodeVerifier();
        const codeChallenge = generateCodeChallenge(codeVerifier);
        const authUrl = `https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=activity%20heartrate%20sleep&code_challenge=${codeChallenge}&code_challenge_method=S256`;
        res.redirect(authUrl);
    } catch (error) {
        console.error('Error generating auth URL:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/auth', (req, res) => {
    try {
        codeVerifier = generateCodeVerifier();
        const codeChallenge = generateCodeChallenge(codeVerifier);
        const authUrl = `https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=activity%20heartrate%20sleep&code_challenge=${codeChallenge}&code_challenge_method=S256`;
        res.redirect(authUrl);
    } catch (error) {
        console.error('Error generating auth URL:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/callback', async (req, res) => {
    const { code } = req.query;

    if (!code) {
        return res.status(400).send('Missing authorization code');
    }

    const tokenUrl = 'https://api.fitbit.com/oauth2/token';
    const data = querystring.stringify({
        client_id: clientId,
        grant_type: 'authorization_code',
        redirect_uri: redirectUri,
        code: code,
        code_verifier: codeVerifier
    });

    app.get('/callback', async (req, res) => {
    const { code } = req.query;

    if (!code) {
        return res.status(400).send('Missing authorization code');
    }

    const tokenUrl = 'https://api.fitbit.com/oauth2/token';
    const data = querystring.stringify({
        client_id: clientId,
        grant_type: 'authorization_code',
        redirect_uri: redirectUri,
        code: code,
        code_verifier: codeVerifier
    });

    const headers = {
        'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
    };

    try {
        const response = await axios.post(tokenUrl, data, { headers });
        const accessToken = response.data.access_token;
        const refreshToken = response.data.refresh_token;
        // Store access and refresh tokens securely
        res.json({ accessToken, refreshToken });
    } catch (error) {
        console.error('Error exchanging code for tokens:', error.response ? error.response.data : error.message);
        res.status(500).send('Internal Server Error');
    }
});


    const headers = {
        'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
    };

    try {
        const response = await axios.post(tokenUrl, data, { headers });
        const accessToken = response.data.access_token;
        const refreshToken = response.data.refresh_token;
        // Store access and refresh tokens securely
        res.json({ accessToken, refreshToken });
    } catch (error) {
        console.error('Error exchanging code for tokens:', error.response ? error.response.data : error.message);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/callback', async (req, res) => {
    const { code } = req.query;

    if (!code) {
        return res.status(400).send('Missing authorization code');
    }

    const tokenUrl = 'https://api.fitbit.com/oauth2/token';
    const data = querystring.stringify({
        client_id: clientId,
        grant_type: 'authorization_code',
        redirect_uri: redirectUri,
        code: code,
        code_verifier: codeVerifier
    });

    const headers = {
        'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
        'Content-Type': 'application/x-www-form-urlencoded'
    };

    try {
        const response = await axios.post(tokenUrl, data, { headers });
        const accessToken = response.data.access_token;
        const refreshToken = response.data.refresh_token;
        // Store access and refresh tokens securely
        res.json({ accessToken, refreshToken });
    } catch (error) {
        console.error('Error exchanging code for tokens:', error.response ? error.response.data : error.message);
        res.status(500).send('Internal Server Error');
    }
});

// app.get('/fetch-data', async (req, res) => {
//     const accessToken = 'YOUR_ACCESS_TOKEN';

//     const fitbitUrl = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json';
//     const headers = {
//         'Authorization': `Bearer ${accessToken}`
//     };

//     try {
//         const response = await axios.get(fitbitUrl, { headers });
//         const data = response.data;

//         // Send data to your website
//         await axios.post('https://yourwebsite.com/api/fitbitdata', data, {
//             headers: {
//                 'Content-Type': 'application/json'
//             }
//         });

//         res.json({ message: 'Data sent to website' });
//     } catch (error) {
//         console.error('Error fetching data from Fitbit:', error.response ? error.response.data : error.message);
//         res.status(500).send('Internal Server Error');
//     }
// });

app.get('/fetch-data', async (req, res) => {
    const accessToken = 'https://api.fitbit.com/oauth2/token';

    const fitbitUrl = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json';
    const headers = {
        'Authorization': `Bearer ${accessToken}`
    };

    try {
        const response = await axios.get(fitbitUrl, { headers });
        const data = response.data;

        // Send data to your website
        await axios.post('https://yourwebsite.com/api/fitbitdata', data, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        res.json({ message: 'Data sent to website' });
    } catch (error) {
        console.error('Error fetching data from Fitbit:', error.response ? error.response.data : error.message);
        res.status(500).send('Internal Server Error');
    }
});


app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});