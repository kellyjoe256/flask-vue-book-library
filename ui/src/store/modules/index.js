// @ts-nocheck
const requireModule = require.context('.', true, /\.js$/);
const modules = {};

/* eslint-disable no-useless-return */

requireModule.keys().forEach((filename) => {
    // Ignore current file
    if (filename === './index.js') {
        return;
    }

    const filenameWithoutDirectory = filename.split('./')[1];
    let filenameWithoutExtension = filenameWithoutDirectory.split('.')[0];
    filenameWithoutExtension = filenameWithoutExtension.toLocaleLowerCase();

    modules[filenameWithoutExtension] = requireModule(filename).default;
});

export default modules;
