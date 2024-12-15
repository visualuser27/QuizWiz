const axios = require('axios');

const generateQuestions = async (text) => {
    try {
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: "gpt-4",
            messages: [
                { role: "system", content: "You are a helpful assistant that generates quiz questions." },
                { role: "user", content: `Create 5 multiple-choice questions based on this content: ${text}` }
            ]
        }, {
            headers: {
                Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        const questions = response.data.choices[0].message.content;
        return questions;
    } catch (error) {
        console.error('Error during question generation:', error);
        throw error;
    }
};

module.exports = generateQuestions;
