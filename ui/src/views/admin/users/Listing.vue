<template>
    <b-row class="justify-content-md-center">
        <!-- prettier-ignore -->
        <b-col lg="10" md="auto">
            <b-row>
                <b-col>
                    <pagination-limit></pagination-limit>
                </b-col>
                <b-col class="text-right">
                    <b-link
                        :to="{ name: 'users.add' }"
                        class="btn btn-outline-secondary"
                    >Add User</b-link>
                </b-col>
            </b-row>
            <template v-if="!users.length">
                <h1>No users available</h1>
            </template>
            <template v-else>
                <b-table
                    :fields="fields"
                    :items="users"
                    striped
                >
                    <template v-slot:cell(username)="data">
                        {{ data.value }}
                    </template>
                    <template v-slot:cell(is_admin)="data">
                        {{ data.value ? 'True' : 'False' }}
                    </template>
                    <template v-slot:cell(created_at)="data">
                        {{ data.value | datetime }}
                    </template>
                    <template v-slot:cell(id)="data">
                        <b-link
                            :to="{
                                name: 'users.edit',
                                params: { id: data.value },
                            }"
                            class="text-info"
                        ><b-icon icon="pencil"></b-icon></b-link>
                        <a
                            class="text-danger"
                            href="#"
                            @click.prevent="erase(data.value)"
                        >
                            <b-icon icon="trash-fill"></b-icon>
                        </a>
                    </template>
                </b-table>
                <!-- prettier-ignore -->
                <pagination
                    :fetchMethod="getUsers"
                ></pagination>
            </template>
        </b-col>
    </b-row>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'UsersListing',
    metaInfo: {
        title: 'Users',
    },
    created() {
        this.getUsers();
    },
    data() {
        return {
            fields: [
                {
                    key: 'username',
                    label: 'Username',
                    sortable: true,
                },
                {
                    key: 'is_admin',
                    label: 'Is admin?',
                },
                {
                    key: 'created_at',
                    label: 'Created',
                },
                {
                    key: 'id',
                    label: '',
                },
            ],
        };
    },
    computed: {
        ...mapGetters({
            users: 'users/users',
        }),
    },
    methods: {
        ...mapActions({
            getUsers: 'users/getUsers',
            deleteUser: 'users/deleteUser',
        }),
        erase(id) {
            // eslint-disable-next-line
            if (!confirm('Are you sure?')) {
                return;
            }

            this.deleteUser(id)
                .then(() => {
                    this.getUsers();
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
};
</script>
