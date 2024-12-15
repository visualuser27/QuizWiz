const whisper = require('whisper-node');

const transcribeAudio = async (audioPath) => {
    try {
        const result = await whisper.transcribe(audioPath, { model: "base" });
        return result.text;
    } catch (error) {
        console.error('Error during transcription:', error);
        throw error;
    }
};

module.exports = transcribeAudio;
