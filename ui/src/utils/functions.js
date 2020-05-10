/* eslint-disable import/prefer-default-export */
export const appendQueryString = (baseURL, queryString) => {
    if (!queryString) {
        return baseURL;
    }
    return `${baseURL}?${queryString}`;
};
