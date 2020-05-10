<template>
    <div class="overflow-auto">
        <!-- Use text in props -->
        <b-pagination
            v-if="pages > 1"
            v-model="currentPage"
            @change="changePage"
            :total-rows="pagination.meta.total"
            :per-page="pagination.meta.per_page"
            first-text="First"
            prev-text="Prev"
            next-text="Next"
            last-text="Last"
        ></b-pagination>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import eventBus from '@/eventBus';

export default {
    name: 'Pagination',
    props: {
        limit: {
            type: Number,
        },
        fetchMethod: {
            type: Function,
            required: true,
        },
    },
    data() {
        return {
            currentPage: 1,
            queryParams: {},
        };
    },
    computed: {
        ...mapGetters({
            pages: 'pages',
            pagination: 'pagination',
        }),
    },
    created() {
        eventBus.$on('change:limit', (limit) => {
            const currentQueryParams = this.queryParams;

            this.currentPage = 1;
            this.queryParams = {
                ...currentQueryParams,
                page: 1,
                limit,
            };
        });

        this.getLinkQueryParams();
    },
    watch: {
        queryParams: {
            deep: true,
            // eslint-disable-next-line
            handler: function(newValue, oldValue) {
                const queryString = this.stringifyQueryParams(newValue);

                this.fetchMethod(queryString);
            },
        },
    },
    methods: {
        parseQueryStringParams(url) {
            const index = String(url)
                .trim()
                .indexOf('?');

            if (!(index > -1)) {
                return {};
            }

            const queryString = url.substr(index + 1);

            if (!queryString) {
                return {};
            }

            const queryStringParts = queryString.split('&');
            const output = {};
            for (let i = 0, len = queryStringParts.length; i < len; i += 1) {
                const [key, value] = queryStringParts[i].split('=');
                output[key] = value;
            }

            return output;
        },
        getLinkQueryParams() {
            const { links } = this.pagination;
            const linkQueryParams = this.parseQueryStringParams(links.first);

            this.queryParams = { ...linkQueryParams };
        },
        stringifyQueryParams(params) {
            let output = '';

            Object.entries(params).forEach((entry) => {
                const [key, value] = entry;
                const queryString = key + (value ? `=${value}` : '');
                output += output ? `&${queryString}` : queryString;
            });

            return output;
        },
        changePage(page) {
            const currentQueryParams = this.queryParams;
            this.queryParams = {
                ...currentQueryParams,
                page,
            };
        },
    },
};
</script>