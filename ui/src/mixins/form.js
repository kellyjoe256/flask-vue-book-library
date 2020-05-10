import _ from 'lodash';

export default {
    methods: {
        hasError(field) {
            return _.has(this.errors, field);
        },
        getError(field) {
            return _.get(this.errors, field);
        },
    },
};
