import moment from 'moment';

export default {
    date(value) {
        return moment(value).format('MMMM Do, YYYY');
    },
};
