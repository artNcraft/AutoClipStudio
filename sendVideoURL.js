// netlify/functions/sendVideoURL.js
exports.handler = async function (event, context) {
    if (event.httpMethod === 'POST') {
        const { videoURL } = JSON.parse(event.body);

        // Logic to process or log the video URL (can be replaced with DB or storage logic)
        console.log('Received video URL:', videoURL);

        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Video URL received successfully!', videoURL }),
        };
    } else {
        return {
            statusCode: 405,
            body: JSON.stringify({ message: 'Method Not Allowed' }),
        };
    }
};
