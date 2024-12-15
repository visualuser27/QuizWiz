const ytdl = require('ytdl-core');
const fs = require('fs');
const path = require('path');

const downloadAudio = async (url, outputFolder) => {
    const audioPath = path.join(outputFolder, 'audio.mp4');
    const audioStream = ytdl(url, { filter: 'audioonly' });
    
    await new Promise((resolve, reject) => {
        const writeStream = fs.createWriteStream(audioPath);
        audioStream.pipe(writeStream);
        writeStream.on('finish', resolve);
        writeStream.on('error', reject);
    });
    return audioPath;
};

module.exports = downloadAudio;
